# Gera fala com o ElevenLabs para os personagens (vozes salvas na conta: "Bit" e "Ficha (GMS)").
# A chave fica em C:\Users\willi\.elevenlabs (fora do repositório), como "sk_..." ou "ELEVEN_API_KEY=sk_...". Nunca imprimir a chave.
# Uso: .\tts.ps1 -Voz Bit -Texto "Oi, eu sou o Bit!" -Saida C:\caminho\fala.mp3
param(
  [Parameter(Mandatory)][ValidateSet('Bit', 'Ficha')][string]$Voz,
  [Parameter(Mandatory)][string]$Texto,
  [Parameter(Mandatory)][string]$Saida,
  [string]$Modelo = 'eleven_multilingual_v2',
  [double]$Velocidade = 1.0  # 0.7 a 1.2 (ElevenLabs voice_settings.speed); 1.0 = como sempre foi
)
$ErrorActionPreference = 'Stop'
$key = ((Get-Content -LiteralPath "$env:USERPROFILE\.elevenlabs" -Raw).Trim() -replace '^ELEVEN_API_KEY=', '').Trim()
$h = @{ 'xi-api-key' = $key }
$nome = @{ Bit = 'Bit'; Ficha = 'Ficha (GMS)' }[$Voz]
$voices = (Invoke-RestMethod -Uri 'https://api.elevenlabs.io/v1/voices' -Headers $h).voices
$id = ($voices | Where-Object { $_.name -eq $nome } | Select-Object -First 1).voice_id
if (-not $id) { throw "Voz '$nome' não encontrada na conta" }
# estilo por personagem: o Bit é estável e animado; a Ficha varia mais (nervosa)
$cfg = @{ Bit = @{ stability = 0.45; similarity_boost = 0.8; style = 0.35 }; Ficha = @{ stability = 0.3; similarity_boost = 0.8; style = 0.6 } }[$Voz]
if ($Velocidade -ne 1.0) { $cfg = $cfg.Clone(); $cfg.speed = $Velocidade }
$body = @{ text = $Texto; model_id = $Modelo; voice_settings = $cfg } | ConvertTo-Json -Depth 4
$bytes = [Text.Encoding]::UTF8.GetBytes($body)
Invoke-WebRequest -Uri "https://api.elevenlabs.io/v1/text-to-speech/$id`?output_format=mp3_44100_128" -Method Post -Headers $h -ContentType 'application/json; charset=utf-8' -Body $bytes -OutFile $Saida -UseBasicParsing | Out-Null
"ok $Voz -> $Saida"
