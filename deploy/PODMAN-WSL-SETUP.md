# Hezarfen — Podman ile Çalıştırma (Windows / WSL2)

Tüm yığını (**surrealdb + backend + chatbot-bridge + frontend**) **Podman** ile ayağa
kaldırma rehberi. Windows/WSL2'de Podman'ın çalışması için MS'in varsayılan WSL
kernel'inde olmayan birkaç ağ özelliği gerekir; bu paket onu **kaynaktan** derleyip
kurar. **Linux/macOS** kullanıyorsan kernel adımına gerek yok — doğrudan
[Stack'i başlat](#3-stacki-başlat)'a geç.

## Neden özel kernel gerekiyor?
Podman 6 / netavark 2.0 konteyner ağı için şu çekirdek özelliklerini ister; MS'in
WSL kernel'i bunları **modül** bırakır ya da hiç açmaz (yüklenmedikleri için yok
sayılır) → `netavark ... nftables/bridge/tap` hataları:

| Özellik | Ne için |
|---|---|
| `NFT_FIB_IPV4/IPV6/INET` | netavark hostport DNAT (`fib daddr type local`) |
| `BRIDGE`, `VETH` | konteyner köprü ağı |
| `TUN` (`/dev/net/tun`) | **rootless** pasta ağı |

Ayrıca **rootful** podman machine'de yayınlanan portlar Windows host'a güvenilir
iletilmez (netavark DNAT'ın dinleyen socket'i yok). **Rootless** machine
(`rootlessport` gerçek socket açar) ile `localhost:5173/7656` **stabil** çalışır.

## Ön koşullar
1. **Podman Desktop** kurulu + **bir podman machine** oluşturulmuş ve çalışır
   (`podman machine list`). CLI yoksa: `winget install RedHat.Podman`.
2. Üç repo **yan yana** (sibling) klonlanmış:
   ```
   <parent>/
     ├─ hezarfen_backend/
     ├─ hezarfen_frontend/
     └─ Hezarfen-Rule-Based-Chatbot/   <- bu repo (compose + script'ler deploy/ içinde)
   ```

## Hızlı başlangıç (Windows, iki komut)
`Hezarfen-Rule-Based-Chatbot/` içinden PowerShell'de:
```powershell
# 1) Tek seferlik: kernel derle + kur, machine'i rootless yap, WSL'i yeniden başlat
pwsh -File deploy/setup-podman-wsl.ps1

# 2) Her seferinde: base'leri pre-pull + stack'i ayağa kaldır
pwsh -File deploy/run-stack.ps1
```
Bitince: **http://localhost:5173** (giriş `admin` / `admin123`) · backend **http://localhost:7656**.

---

## Manuel adımlar (script kullanmadan)
### 1. Kernel'i derle + kur (yalnız Windows/WSL2)
```powershell
$P = (Get-Command podman).Source     # ya da C:\Users\<sen>\AppData\Local\Programs\Podman\podman.exe
# Derle (RUN adımları makine ağını kullansın diye --network=host):
& $P build --network=host -t wslkernel-build -f deploy/wsl-kernel/Containerfile deploy/wsl-kernel
# bzImage'ı çıkar:
mkdir "$env:USERPROFILE\wsl-custom-kernel" -Force
& $P create --name kext localhost/wslkernel-build
& $P cp kext:/bzImage-fib "$env:USERPROFILE\wsl-custom-kernel\bzImage"
& $P rm kext
```
`%USERPROFILE%\.wslconfig` oluştur/güncelle (varsa yedekle):
```ini
[wsl2]
kernelCommandLine = cgroup_no_v1=all
kernel=C:\\Users\\<sen>\\wsl-custom-kernel\\bzImage
```

### 2. Machine'i rootless yap + yeniden başlat
```powershell
& $P machine stop
& $P machine set --rootful=false
wsl --shutdown
& $P machine start
# Doğrula:
& $P machine ssh "uname -r; ls /dev/net/tun"
& $P run --rm docker.io/surrealdb/surrealdb:v3 version   # netavark hatası OLMAMALI
```

### 3. Stack'i başlat (PROJE-BAZLI — all-in-one compose yok)
Tek komut (base pre-pull + 3 repoyu doğru sırada başlatır):
```powershell
pwsh -File deploy/run-stack.ps1
```
Ya da elle (her repo kendi compose'uyla; sıra önemli — backend ağı yaratır):
```powershell
cd ..\hezarfen_backend            ; & $P compose up -d --build   # postgres + backend (:7656,:8090)
cd ..\hezarfen_frontend           ; & $P compose up -d --build   # frontend (:5173)
cd ..\Hezarfen-Rule-Based-Chatbot ; & $P compose up -d --build   # yalnız chatbot köprüsü
```
> Chatbot compose yalnız ürün köprüsünü çalıştırır; demo web container'ı ve host port yayını yoktur.
> **Linux/macOS:** kernel/machine adımları gerekmez; sadece bu bölümü çalıştır. Portlar zaten host'a iletilir.

---

## Sorun giderme
| Belirti | Neden / Çözüm |
|---|---|
| `netavark ... "nft" ... while applying ruleset` | Kernel'de `NFT_FIB` yok → özel kernel'i kur (yukarıda). |
| `create bridge: Operation not supported` | `BRIDGE`/`VETH` modül → kernel'i yeniden derle (=y). |
| `Failed to set up tap device` (rootless) | `/dev/net/tun` yok (`TUN=m`) → kernel'i yeniden derle. |
| `localhost:5173/7656` aralıklı/erişilemez | Machine **rootful** → `podman machine set --rootful=false` + restart. |
| build: `unable to retrieve auth token ... unauthorized` | docker.io anonim-pull dalgalanması → base imajları önce `podman pull` ile çek, sonra build. |
| `Cgroups v1 not supported` | `.wslconfig`'e `kernelCommandLine = cgroup_no_v1=all` + `wsl --shutdown`. |

## Durdurma / temizlik (her repo kendi dizininde)
```powershell
cd ..\Hezarfen-Rule-Based-Chatbot ; & $P compose down
cd ..\hezarfen_frontend           ; & $P compose down
cd ..\hezarfen_backend            ; & $P compose down        # volume kalır
cd ..\hezarfen_backend            ; & $P compose down -v     # volume'ları da sil
```

## Notlar
- Kernel sürümü (`6.6.123.2`) WSL kernel'inle eşleşmek zorunda değil; sadece geçerli
  bir WSL2 kernel'i olması yeter. Farklı bir sürüm istersen `deploy/wsl-kernel/Containerfile`
  içindeki `--branch` etiketini değiştir (bkz. microsoft/WSL2-Linux-Kernel tag'leri).
- `AI_SHARED_TOKEN` ZORUNLUDUR: boş ya da `change-me` bırakılırsa köprü
  açılışta yapılandırma hatasıyla durur. Gerçek bir değer ver (`$env:AI_SHARED_TOKEN`).
