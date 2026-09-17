# Hezarfen — Podman stack'i PROJE-BAZLI ayağa kaldırır (all-in-one compose YOK).
#   1) Base imajları pre-pull (docker.io anonim-pull auth hatalarını önlemek için).
#   2) Her repoyu kendi compose'uyla, doğru sırada başlatır:
#        hezarfen_backend (db+backend, ağı yaratır) -> hezarfen_frontend -> chatbot bridge
#   3) Doğrular ve localhost adreslerini basar.
# Ön koşul: deploy/setup-podman-wsl.ps1 bir kez çalıştırılmış olmalı.
# Çalıştır:  pwsh -File deploy/run-stack.ps1
$ErrorActionPreference = "Stop"

function Find-Podman {
  $c = (Get-Command podman -ErrorAction SilentlyContinue).Source
  if ($c) { return $c }
  foreach ($p in @("$env:LOCALAPPDATA\Programs\Podman\podman.exe",
                   "$env:ProgramFiles\RedHat\Podman\podman.exe")) {
    if (Test-Path $p) { return $p }
  }
  throw "podman.exe bulunamadı."
}
$PODMAN = Find-Podman
$parent = Resolve-Path (Join-Path $PSScriptRoot "..\..")
$backend  = Join-Path $parent "hezarfen_backend"
$frontend = Join-Path $parent "hezarfen_frontend"
$chatbot  = Join-Path $parent "Hezarfen-Rule-Based-Chatbot"

& $PODMAN machine start *> $null 2>&1

Write-Host "[1/3] Base imajlar pre-pull ediliyor..."
$bases = @("docker.io/surrealdb/surrealdb:v3")
foreach ($cf in @((Join-Path $backend "Containerfile"),
                  (Join-Path $frontend "Containerfile"),
                  (Join-Path $chatbot "Containerfile"))) {
  if (Test-Path $cf) {
    Select-String -Path $cf -Pattern '^\s*FROM\s+(\S+)' | ForEach-Object {
      $bases += $_.Matches[0].Groups[1].Value
    }
  }
}
foreach ($img in ($bases | Sort-Object -Unique)) {
  Write-Host "    pull $img"; & $PODMAN pull $img *> $null 2>&1
}

Write-Host "`n[2/3] Proje-bazlı up (backend Rust ilk seferde uzun sürer)..."
function Compose-Up([string]$dir, [string[]]$extra) {
  Push-Location $dir
  try { & $PODMAN compose @extra up -d --build; if ($LASTEXITCODE -ne 0) { throw "compose up başarısız: $dir" } }
  finally { Pop-Location }
}
Compose-Up $backend  @()                                  # ağı (hezarfen_backend_default) yaratır
Compose-Up $frontend @()                                  # backend ağına bağlanır
Compose-Up $chatbot  @()                                  # yalnız bridge; backend ağına dial-in eder

Write-Host "`n[3/3] Doğrulama..."
Start-Sleep -Seconds 6
& $PODMAN ps --format "{{.Names}} {{.Status}}"
foreach ($p in 7656,5173) {
  try {
    $code = (Invoke-WebRequest -UseBasicParsing -Uri "http://localhost:$p/" -TimeoutSec 6).StatusCode
    Write-Host "    localhost:$p -> HTTP $code"
  } catch { Write-Host "    localhost:$p -> erişilemedi ($($_.Exception.Message))" }
}
Write-Host "`n✅ Hazır. Test: http://localhost:5173  (giriş: admin / admin123)"
