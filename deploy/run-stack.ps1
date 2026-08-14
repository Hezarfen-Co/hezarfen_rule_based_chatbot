# Hezarfen — Podman stack'i ayağa kaldırır.
#   1) Tüm Containerfile base imajlarını pre-pull eder (docker.io anonim-pull auth
#      hatalarını build sırasında yaşamamak için).
#   2) podman compose up -d --build.
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
$compose = Join-Path $PSScriptRoot "compose.yaml"
$parent  = Resolve-Path (Join-Path $PSScriptRoot "..\..")

& $PODMAN machine start *> $null 2>&1

Write-Host "[1/3] Base imajlar pre-pull ediliyor..."
$cfiles = @(
  (Join-Path $parent "hezarfen_backend\Containerfile"),
  (Join-Path $parent "hezarfen_frontend\Containerfile"),
  (Join-Path $parent "Hezarfen-Rule-Based-Chatbot\Containerfile")
)
$bases = @("docker.io/surrealdb/surrealdb:v3")
foreach ($cf in $cfiles) {
  if (Test-Path $cf) {
    Select-String -Path $cf -Pattern '^\s*FROM\s+(\S+)' | ForEach-Object {
      $bases += $_.Matches[0].Groups[1].Value
    }
  }
}
$bases = $bases | Sort-Object -Unique
foreach ($img in $bases) {
  Write-Host "    pull $img"
  & $PODMAN pull $img *> $null 2>&1
}

Write-Host "`n[2/3] podman compose up -d --build (backend Rust ilk seferde uzun sürer)..."
& $PODMAN compose -f $compose up -d --build
if ($LASTEXITCODE -ne 0) { throw "compose up başarısız (build log'una bak)." }

Write-Host "`n[3/3] Doğrulama..."
Start-Sleep -Seconds 6
& $PODMAN ps --format "{{.Names}} {{.Status}}"
foreach ($p in 8080,5173) {
  try {
    $code = (Invoke-WebRequest -UseBasicParsing -Uri "http://localhost:$p/" -TimeoutSec 6).StatusCode
    Write-Host "    localhost:$p -> HTTP $code"
  } catch { Write-Host "    localhost:$p -> erişilemedi ($($_.Exception.Message))" }
}
Write-Host "`n✅ Hazır. Test: http://localhost:5173  (giriş: admin / admin123)"
