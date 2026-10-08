# Hook do Claude Code -> acrescenta um evento em ..\data\events.json
# LOCAL guarda: evento, sessão, agente, tipo, pasta, ferramenta usada, alvo (arquivo/comando/busca) e resumo final.
# NUVEM (se configurada) recebe só: evento, sessão, agente, tipo, pasta e NOME da ferramenta. Nunca alvo nem resumo.
# Nunca falha: qualquer erro é engolido para não atrapalhar a sessão.
$ErrorActionPreference = 'SilentlyContinue'
try {
  $raw = [Console]::In.ReadToEnd()
  if (-not $raw) { exit 0 }
  $in = ConvertFrom-Json -InputObject $raw

  $root = Split-Path -Parent $PSScriptRoot
  $proj = Split-Path -Parent $root                     # raiz do projeto (Projetos)
  $file = Join-Path $root 'data\events.json'
  $max  = 1500

  $leaf = ''
  if ($in.cwd) { $leaf = Split-Path -Leaf ([string]$in.cwd) }
  $cut = { param($s, $n) $s = [string]$s; if ($s.Length -gt $n) { $s.Substring(0, $n) + '…' } else { $s } }

  $evName = [string]$in.hook_event_name
  $tool = ''; $alvo = ''; $arquivo = ''; $resumo = ''
  if ($evName -eq 'PostToolUse' -or $evName -eq 'PreToolUse') {
    $tool = [string]$in.tool_name
    $ti = $in.tool_input
    if ($ti) {
      if ($ti.file_path) {
        $alvo = [string]$ti.file_path
        if ($tool -eq 'Write' -or $tool -eq 'Edit' -or $tool -eq 'NotebookEdit') {
          $p = ($alvo -replace '\\', '/'); $pr = ($proj -replace '\\', '/')
          if ($p.StartsWith($pr, [StringComparison]::OrdinalIgnoreCase)) { $arquivo = $p.Substring($pr.Length).TrimStart('/') } else { $arquivo = $p }
        }
      }
      elseif ($ti.command) { $alvo = & $cut $ti.command 120 }
      elseif ($ti.pattern) { $alvo = & $cut $ti.pattern 120 }
      elseif ($ti.query)   { $alvo = & $cut $ti.query 120 }
      elseif ($ti.url)     { $alvo = & $cut $ti.url 120 }
    }
  }
  if ($evName -eq 'SubagentStop' -and $in.last_assistant_message) { $resumo = & $cut $in.last_assistant_message 600 }

  $ev = [ordered]@{
    t       = (Get-Date).ToUniversalTime().ToString('o')
    ev      = $evName
    session = [string]$in.session_id
    agent   = [string]$in.agent_id
    type    = [string]$in.agent_type
    project = $leaf
    reason  = [string]$in.reason
    tool    = $tool
    alvo    = $alvo
    arquivo = $arquivo
    resumo  = $resumo
  }
  $evJson = ConvertTo-Json -InputObject $ev -Compress
  # versão para a nuvem: sem alvo, arquivo nem resumo
  $evCloud = [ordered]@{ t = $ev.t; ev = $evName; session = $ev.session; agent = $ev.agent; type = $ev.type; project = $leaf; tool = $tool }
  $cloudJson = ConvertTo-Json -InputObject $evCloud -Compress

  $mutex = New-Object System.Threading.Mutex($false, 'Global\SalaAgentesHook')
  [void]$mutex.WaitOne(3000)
  try {
    # Um evento por linha: não depende do ConvertFrom/To-Json de arrays (bugado no PowerShell 5.1)
    $lines = New-Object System.Collections.Generic.List[string]
    if (Test-Path $file) {
      foreach ($ln in [IO.File]::ReadAllLines($file, [Text.Encoding]::UTF8)) {
        $t = $ln.Trim().TrimEnd(',')
        if ($t.StartsWith('{')) { $lines.Add($t) }
      }
    }
    $lines.Add($evJson)
    if ($lines.Count -gt $max) { $lines.RemoveRange(0, $lines.Count - $max) }
    $out = "[`n  " + ($lines -join ",`n  ") + "`n]"
    [IO.File]::WriteAllText($file, $out, (New-Object Text.UTF8Encoding($false)))
  } finally { [void]$mutex.ReleaseMutex() }

  # Nuvem (opcional): se existir hooks\nuvem.json, envia a versão reduzida ao Firebase Realtime Database.
  # nuvem.json = { "url": "https://SEU-PROJETO-default-rtdb.firebaseio.com", "id": "<sala-secreta>", "secret": "<database secret>" }
  # Esse arquivo fica só na sua máquina (está no .gitignore). O segredo NUNCA vai para a página.
  $cfgNuvem = Join-Path $PSScriptRoot 'nuvem.json'
  if ((Test-Path $cfgNuvem) -and $evName -ne 'PostToolUse' -and $evName -ne 'PreToolUse') {
    $n = Get-Content $cfgNuvem -Raw -Encoding UTF8 | ConvertFrom-Json
    if ($n.url -and $n.id -and $n.secret) {
      $uri = ($n.url.TrimEnd('/')) + '/salas/' + $n.id + '/eventos.json?auth=' + $n.secret
      $req = [Net.WebRequest]::Create($uri)
      $req.Method = 'POST'; $req.ContentType = 'application/json'; $req.Timeout = 4000
      $bytes = [Text.Encoding]::UTF8.GetBytes($cloudJson)
      $req.ContentLength = $bytes.Length
      $st = $req.GetRequestStream(); $st.Write($bytes, 0, $bytes.Length); $st.Close()
      $resp = $req.GetResponse(); $resp.Close()
    }
  }
} catch { }
exit 0
