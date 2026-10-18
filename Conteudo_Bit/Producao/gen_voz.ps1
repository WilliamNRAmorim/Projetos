# Gera as falas (stems/<ep>/faltaN.mp3) de um JSON { ep: [textos] } com tts.ps1 (voz Bit, 1.1). Pula as que já existem; para no primeiro erro (cota).
param([Parameter(Mandatory)][string]$Json, [Parameter(Mandatory)][string[]]$Eps, [string]$Prefixo = '')
$d = Get-Content -LiteralPath $Json -Raw -Encoding UTF8 | ConvertFrom-Json
foreach ($e in $Eps) {
  $dir = Join-Path $PSScriptRoot "stems\$Prefixo$e"; New-Item -ItemType Directory -Force $dir | Out-Null
  $i = 0
  foreach ($t in $d.$e) {
    $i++; $mp3 = Join-Path $dir "fala$i.mp3"; if (Test-Path $mp3) { continue }
    $tmp = Join-Path $env:TEMP "fala_tmp.txt"; [IO.File]::WriteAllText($tmp, $t, (New-Object Text.UTF8Encoding($false)))
    try { & "$PSScriptRoot\tts.ps1" -Voz Bit -TextoArquivo $tmp -Saida $mp3 -Velocidade 1.1 | Out-Null } catch { Write-Host "ERRO $e fala$i : $($_.Exception.Message)"; exit 1 }
  }
  Write-Host "ok $e ($i falas)"
}
