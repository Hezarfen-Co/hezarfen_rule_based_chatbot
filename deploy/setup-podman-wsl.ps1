# Hezarfen — Podman on WSL2 tek seferlik kurulum.
# Ne yapar:
#   1) Özel WSL2 kernel'ini derler (nft_fib + bridge + veth + tun) — podman build ile.
#   2) bzImage'ı %USERPROFILE%\wsl-custom-kernel\bzImage'a çıkarır.
#   3) %USERPROFILE%\.wslconfig'i (cgroups v2 + custom kernel) yazar (varsa yedekler).
#   4) Podman machine'i ROOTLESS yapar (host port iletimi rootless'ta güvenilir).
#   5) WSL'i yeniden başlatır ve ağı doğrular.
#
# Ön koşul: Podman Desktop + çalışan bir "podman machine" (podman machine list).
# Çalıştır:  pwsh -File deploy/setup-podman-wsl.ps1
$ErrorActionPreference = "Stop"

function Find-Podman {
  $c = (Get-Command podman -ErrorAction SilentlyContinue).Source
  if ($c) { return $c }
  foreach ($p in @("$env:LOCALAPPDATA\Programs\Podman\podman.exe",
                   "$env:ProgramFiles\RedHat\Podman\podman.exe")) {
    if (Test-Path $p) { return $p }
  }
  throw "podman.exe bulunamadı. Önce Podman'ı kur (winget install RedHat.Podman) ve bir machine oluştur."
}
$PODMAN = Find-Podman
Write-Host "[podman] $PODMAN"

# Machine çalışıyor mu?
& $PODMAN machine inspect podman-machine-default *> $null
if ($LASTEXITCODE -ne 0) { throw "podman machine 'podman-machine-default' yok. Podman Desktop'tan oluştur." }
& $PODMAN machine start *> $null 2>&1  # zaten çalışıyorsa zararsız

$kdir = Join-Path $PSScriptRoot "wsl-kernel"
$dest = Join-Path $env:USERPROFILE "wsl-custom-kernel"
New-Item -ItemType Directory -Force -Path $dest | Out-Null

Write-Host "`n[1/5] Kernel derleniyor (podman build --network=host, ~10-20 dk)..."
& $PODMAN build --network=host -t wslkernel-build -f (Join-Path $kdir "Containerfile") $kdir
if ($LASTEXITCODE -ne 0) { throw "Kernel derlemesi başarısız." }

Write-Host "`n[2/5] bzImage çıkarılıyor..."
& $PODMAN rm -f wslkernel-extract *> $null 2>&1
& $PODMAN create --name wslkernel-extract localhost/wslkernel-build | Out-Null
& $PODMAN cp "wslkernel-extract:/bzImage-fib" (Join-Path $dest "bzImage")
& $PODMAN rm wslkernel-extract | Out-Null
$bz = Join-Path $dest "bzImage"
if (-not (Test-Path $bz)) { throw "bzImage çıkarılamadı." }
Write-Host "    -> $bz  ($([math]::Round((Get-Item $bz).Length/1MB,1)) MB)"

Write-Host "`n[3/5] .wslconfig yazılıyor..."
$wslcfg = Join-Path $env:USERPROFILE ".wslconfig"
if (Test-Path $wslcfg) {
  Copy-Item $wslcfg "$wslcfg.hezarfen.bak" -Force
  Write-Host "    (mevcut .wslconfig -> .wslconfig.hezarfen.bak olarak yedeklendi; içeriği değiştiriliyor)"
}
$kernelPath = $bz -replace '\\','\\'
@"
# Hezarfen podman: cgroups v2 + nft_fib/bridge/veth/tun içeren özel WSL2 kernel.
[wsl2]
kernelCommandLine = cgroup_no_v1=all
kernel=$kernelPath
"@ | Set-Content -Path $wslcfg -Encoding utf8
Write-Host "    -> $wslcfg"

Write-Host "`n[4/5] Machine ROOTLESS yapılıyor + WSL yeniden başlatılıyor..."
& $PODMAN machine stop *> $null 2>&1
& $PODMAN machine set --rootful=false *> $null 2>&1
wsl --shutdown
& $PODMAN machine start

Write-Host "`n[5/5] Doğrulama..."
& $PODMAN machine ssh "uname -r; echo -n 'TUN: '; ls /dev/net/tun" 2>&1 | Select-Object -First 3
Write-Host "    Ağ testi (netavark hatası olmamalı):"
& $PODMAN run --rm docker.io/surrealdb/surrealdb:v3 version 2>&1 | Select-Object -First 1

Write-Host "`n✅ Kurulum tamam. Stack'i başlatmak için:  pwsh -File deploy/run-stack.ps1"
