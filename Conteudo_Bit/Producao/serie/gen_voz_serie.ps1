# Gera a trilha de voz de um episodio da serie: le as narracoes de ep/<arquivo>.json (indice em ep/indice.json) e grava
# Producao\stems\serie\epXX\cenaN.mp3 com a voz Bit do ElevenLabs (mesmo tts.ps1 e velocidade 1.1 do gen_voz.ps1). Pula as que ja existem;
# para no primeiro erro (cota). Uma voz por cena (sem ffmpeg nao da pra juntar os mp3 num arquivo so; o motor posiciona cada um na cena).
# Uso: .\gen_voz_serie.ps1 -Ep 00      (cena com "voz": "Ficha" usa a voz Ficha)
param([Parameter(Mandatory)][string]$Ep)
$ErrorActionPreference = 'Stop'
$idx = Get-Content -LiteralPath "$PSScriptRoot\ep\indice.json" -Raw -Encoding UTF8 | ConvertFrom-Json
$arq = $idx.$Ep; if (-not $arq) { Write-Host "Episodio $Ep nao esta em ep/indice.json"; exit 1 }
$d = Get-Content -LiteralPath "$PSScriptRoot\ep\$arq" -Raw -Encoding UTF8 | ConvertFrom-Json
$dir = Join-Path $PSScriptRoot "..\stems\serie\ep$Ep"; New-Item -ItemType Directory -Force $dir | Out-Null
$i = 0
foreach ($c in $d.cenas) {
  $i++; if (-not $c.narracao) { continue }
  $mp3 = Join-Path $dir "cena$i.mp3"; if (Test-Path $mp3) { continue }
  $tmp = Join-Path $env:TEMP 'fala_serie_tmp.txt'; [IO.File]::WriteAllText($tmp, $c.narracao, (New-Object Text.UTF8Encoding($false)))
  $voz = if ($c.voz) { $c.voz } else { 'Bit' }
  try { & "$PSScriptRoot\..\tts.ps1" -Voz $voz -TextoArquivo $tmp -Saida $mp3 -Velocidade 1.1 | Out-Null } catch { Write-Host "ERRO cena $i : $($_.Exception.Message)"; exit 1 }
}
Write-Host "ok ep$Ep ($i cenas)"
