# Teste de elenco de vozes da série (ElevenLabs, vozes "premade" da conta). Gasta ~600 caracteres da cota.
# Uso: .\teste_vozes.ps1   -> grava mp3 em ..\serie\preview\vozes\
# A chave fica em C:\Users\willi\.elevenlabs (nunca imprimir).
$ErrorActionPreference = 'Stop'
$key = ((Get-Content -LiteralPath "$env:USERPROFILE\.elevenlabs" -Raw).Trim() -replace '^ELEVEN_API_KEY=', '').Trim()
$h = @{ 'xi-api-key' = $key }
$voices = (Invoke-RestMethod -Uri 'https://api.elevenlabs.io/v1/voices' -Headers $h).voices
$out = Join-Path $PSScriptRoot 'preview\vozes'
New-Item -ItemType Directory -Force $out | Out-Null

# papel | voz da conta (começa com) | texto | stability | style | speed
$t = @(
  @('narrador_george', 'George', 'A dona se chamava Dalva. Sorria demais. Piscava de menos.', 0.55, 0.25, 0.95),
  @('narrador_brian',  'Brian',  'A dona se chamava Dalva. Sorria demais. Piscava de menos.', 0.55, 0.25, 0.95),
  @('bia_jessica',     'Jessica','Oi, eu sou a Bia.', 0.40, 0.35, 1.0),
  @('bia_sarah',       'Sarah',  'Oi, eu sou a Bia.', 0.40, 0.35, 1.0),
  @('dalva_lily',      'Lily',   'Atende o sete, Bia. Meu bem, é só atender.', 0.60, 0.30, 0.88),
  @('dalva_matilda',   'Matilda','Atende o sete, Bia. Meu bem, é só atender.', 0.60, 0.30, 0.88),
  @('osmar_bill',      'Bill',   'Você disse o seu nome, menina.', 0.50, 0.30, 0.9)
)
foreach ($x in $t) {
  $id = ($voices | Where-Object { $_.name -like "$($x[1])*" } | Select-Object -First 1).voice_id
  if (-not $id) { "voz $($x[1]) nao encontrada"; continue }
  $cfg = @{ stability = $x[3]; similarity_boost = 0.8; style = $x[4]; speed = $x[5] }
  $body = @{ text = $x[2]; model_id = 'eleven_multilingual_v2'; voice_settings = $cfg } | ConvertTo-Json -Depth 4
  $bytes = [Text.Encoding]::UTF8.GetBytes($body)
  $f = Join-Path $out "$($x[0]).mp3"
  try {
    Invoke-WebRequest -Uri "https://api.elevenlabs.io/v1/text-to-speech/$id" -Method Post -Headers $h -ContentType 'application/json; charset=utf-8' -Body $bytes -OutFile $f -UseBasicParsing | Out-Null
    "ok $($x[0])"
  } catch { "falhou $($x[0]): " + $_.Exception.Message }
}
