# Servidor LOCAL da sala (127.0.0.1:5191): página + API para entregas, avaliações, memória e gestão de agentes.
# Só escuta no seu computador. Escritas exigem o cabeçalho X-Sala e Origin local (barra sites externos).
$root  = Split-Path -Parent $MyInvocation.MyCommand.Path
$proj  = Split-Path -Parent $root
$agDir = Join-Path $proj '.claude\agents'
$memDir = Join-Path $proj '.claude\agent-memory'
$avalFile = Join-Path $root 'data\avaliacoes.json'
$enc = New-Object Text.UTF8Encoding($false)
$types = @{ '.html'='text/html; charset=utf-8'; '.json'='application/json; charset=utf-8'; '.js'='text/javascript; charset=utf-8'; '.css'='text/css; charset=utf-8' }
$textExt = '.md', '.txt', '.json', '.html', '.js', '.css', '.csv', '.srt', '.yaml', '.yml', '.ps1', '.py', '.xml'
$nomeOk = '^[a-z0-9][a-z0-9-]{0,40}$'

function Send($res, $obj, $code = 200) {
  $b = $enc.GetBytes((ConvertTo-Json -InputObject $obj -Depth 6 -Compress))
  $res.StatusCode = $code; $res.ContentType = 'application/json; charset=utf-8'; $res.AddHeader('Cache-Control', 'no-store')
  $res.ContentLength64 = $b.Length; $res.OutputStream.Write($b, 0, $b.Length)
}
function Body($req) { $sr = New-Object IO.StreamReader($req.InputStream, [Text.Encoding]::UTF8); $t = $sr.ReadToEnd(); $sr.Close(); if ($t) { ConvertFrom-Json -InputObject $t } else { $null } }
function AppendLinha($file, $json) {   # array JSON com um objeto por linha
  $lines = New-Object System.Collections.Generic.List[string]
  if (Test-Path $file) { foreach ($ln in [IO.File]::ReadAllLines($file, [Text.Encoding]::UTF8)) { $t = $ln.Trim().TrimEnd(','); if ($t.StartsWith('{')) { $lines.Add($t) } } }
  $lines.Add($json)
  [IO.File]::WriteAllText($file, "[`n  " + ($lines -join ",`n  ") + "`n]", $enc)
}
function CaminhoSeguro($rel) {
  $p = [IO.Path]::GetFullPath((Join-Path $proj ($rel -replace '/', '\')))
  if (-not $p.StartsWith($proj, [StringComparison]::OrdinalIgnoreCase)) { return $null }
  if ($p -match '\\\.git(\\|$)' -or $p -match 'nuvem\.json$' -or $p -match '\.env$' -or $p -match '\.key$') { return $null }
  return $p
}
function MemFile($ag) { Join-Path $memDir ($ag + '.md') }
function LerAgentes {
  $out = @()
  foreach ($f in (Get-ChildItem $agDir -Filter *.md -ErrorAction SilentlyContinue)) {
    $txt = Get-Content $f.FullName -Raw -Encoding UTF8
    $m = [regex]::Match($txt, '(?s)^---\s*\r?\n(.*?)\r?\n---'); $fm = if ($m.Success) { $m.Groups[1].Value } else { '' }
    $g = { param($k) $x = [regex]::Match($fm, "(?m)^$k\s*:\s*(.+)$"); if ($x.Success) { $x.Groups[1].Value.Trim() } else { '' } }
    $out += [ordered]@{ nome = $f.BaseName; modelo = (& $g 'model'); descricao = (& $g 'description'); ativo = $true }
  }
  $ap = Join-Path $agDir '_aposentados'
  foreach ($f in (Get-ChildItem $ap -Filter *.md -ErrorAction SilentlyContinue)) { $out += [ordered]@{ nome = $f.BaseName; modelo = ''; descricao = ''; ativo = $false } }
  return $out
}

$l = New-Object System.Net.HttpListener
$l.Prefixes.Add('http://127.0.0.1:5191/')
$l.Start()
while ($l.IsListening) {
  $ctx = $l.GetContext(); $req = $ctx.Request; $res = $ctx.Response
  try {
    $path = [Uri]::UnescapeDataString($req.Url.AbsolutePath)
    if ($path.StartsWith('/api/')) {
      if ($req.HttpMethod -eq 'POST') {
        $origin = $req.Headers['Origin']
        if ($req.Headers['X-Sala'] -ne '1' -or ($origin -and $origin -notmatch '^http://(localhost|127\.0\.0\.1):5191$')) { Send $res @{ erro = 'bloqueado' } 403; continue }
      }
      switch ($path) {
        '/api/arquivo' {
          $p = CaminhoSeguro $req.QueryString['p']
          if (-not $p -or -not (Test-Path $p -PathType Leaf) -or ($textExt -notcontains [IO.Path]::GetExtension($p).ToLower())) { Send $res @{ erro = 'arquivo indisponível' } 404; break }
          if ((Get-Item $p).Length -gt 400KB) { Send $res @{ erro = 'arquivo grande demais' } 413; break }
          Send $res @{ nome = [IO.Path]::GetFileName($p); texto = [IO.File]::ReadAllText($p, [Text.Encoding]::UTF8) }
        }
        '/api/memoria' {
          $ag = $req.QueryString['agente']; if ($ag -notmatch $nomeOk) { Send $res @{ erro = 'nome inválido' } 400; break }
          if ($req.HttpMethod -eq 'POST') {
            $b = Body $req; New-Item -ItemType Directory -Force $memDir | Out-Null
            [IO.File]::WriteAllText((MemFile $ag), [string]$b.texto, $enc); Send $res @{ ok = $true }
          } else {
            $f = MemFile $ag; Send $res @{ agente = $ag; texto = $(if (Test-Path $f) { [IO.File]::ReadAllText($f, [Text.Encoding]::UTF8) } else { '' }) }
          }
        }
        '/api/avaliacoes' { Send $res @{ texto = $(if (Test-Path $avalFile) { [IO.File]::ReadAllText($avalFile, [Text.Encoding]::UTF8) } else { '[]' }) } }
        '/api/avaliar' {
          $b = Body $req; $ag = [string]$b.agente
          if ($ag -notmatch $nomeOk -or @('up', 'down') -notcontains [string]$b.nota) { Send $res @{ erro = 'dados inválidos' } 400; break }
          $com = [string]$b.comentario; if ($com.Length -gt 500) { $com = $com.Substring(0, 500) }
          $tagsOk = @('atendeu', 'sem_problemas', 'retrabalho', 'errou', 'nao_atendeu'); $tags = @(@($b.tags) | Where-Object { $tagsOk -contains [string]$_ } | ForEach-Object { [string]$_ }); $ctx = [string]$b.contexto; if ($ctx.Length -gt 200) { $ctx = $ctx.Substring(0, 200) }
          $reg = [ordered]@{ t = (Get-Date).ToUniversalTime().ToString('o'); agente = $ag; run = [string]$b.run; arquivo = [string]$b.arquivo; nota = [string]$b.nota; tags = $tags; comentario = $com; contexto = $ctx }
          AppendLinha $avalFile (ConvertTo-Json -InputObject $reg -Compress)
          # a avaliação vira lição na memória do agente (ele lê isso ao começar)
          New-Item -ItemType Directory -Force $memDir | Out-Null
          $marca = if ($b.nota -eq 'up') { 'APROVADO' } else { 'REPROVADO' }
          $linha = "- [$((Get-Date).ToString('yyyy-MM-dd'))] $marca" + $(if ($ctx) { " em '$ctx'" } else { '' }) + $(if ($tags.Count) { " [" + ($tags -join ', ') + "]" } else { '' }) + $(if ($com) { ": $com" } else { '' })
          if (-not (Test-Path (MemFile $ag))) { [IO.File]::WriteAllText((MemFile $ag), "# Memória do agente $ag`n`n## Lições (avaliações do William)`n", $enc) }
          [IO.File]::AppendAllText((MemFile $ag), $linha + "`n", $enc)
          Send $res @{ ok = $true }
        }
        '/api/agentes' { Send $res @{ itens = @(LerAgentes) } }
        '/api/arquivar' {
          $b = Body $req; $ag = [string]$b.agente
          $src = Join-Path $agDir ($ag + '.md')
          if ($ag -notmatch $nomeOk -or -not (Test-Path $src)) { Send $res @{ erro = 'agente não encontrado' } 404; break }
          $ap = Join-Path $agDir '_aposentados'; New-Item -ItemType Directory -Force $ap | Out-Null
          Move-Item $src (Join-Path $ap ($ag + '.md')) -Force; Send $res @{ ok = $true }
        }
        '/api/clonar' {
          $b = Body $req; $de = [string]$b.de; $para = [string]$b.para
          $src = Join-Path $agDir ($de + '.md'); $dst = Join-Path $agDir ($para + '.md')
          if ($de -notmatch $nomeOk -or $para -notmatch $nomeOk -or -not (Test-Path $src) -or (Test-Path $dst)) { Send $res @{ erro = 'nomes inválidos ou destino já existe' } 400; break }
          $txt = [IO.File]::ReadAllText($src, [Text.Encoding]::UTF8)
          $txt = [regex]::Replace($txt, '(?m)^name\s*:.*$', "name: $para", 1)
          $var = ([string]$b.variacao).Trim()
          if ($var) { $txt = $txt.TrimEnd() + "`n`n## Variação (experimento da semana, clone de $de)`n$var`n" }
          [IO.File]::WriteAllText($dst, $txt, $enc)
          if (Test-Path (MemFile $de)) { Copy-Item (MemFile $de) (MemFile $para) -Force }
          Send $res @{ ok = $true }
        }
        '/api/historico' {
          # eventos dos últimos N dias (lê os arquivos mensais; devolve o JSON cru, sem reprocessar)
          $dias = 7; [void][int]::TryParse([string]$req.QueryString['dias'], [ref]$dias); if ($dias -lt 1) { $dias = 1 }; if ($dias -gt 62) { $dias = 62 }
          $corte = (Get-Date).ToUniversalTime().AddDays(-$dias).ToString('o')
          $out = New-Object System.Collections.Generic.List[string]
          foreach ($m in @((Get-Date).AddMonths(-2), (Get-Date).AddMonths(-1), (Get-Date))) {
            $f = Join-Path $root ('data\historico-' + $m.ToString('yyyy-MM') + '.jsonl')
            if (Test-Path $f) { foreach ($ln in [IO.File]::ReadAllLines($f, [Text.Encoding]::UTF8)) { if ($ln.Length -gt 40 -and $ln.Substring(6, 27) -ge $corte.Substring(0, 27)) { $out.Add($ln) } } }
          }
          $b = $enc.GetBytes('[' + ($out -join ',') + ']'); $res.ContentType = 'application/json; charset=utf-8'; $res.AddHeader('Cache-Control', 'no-store'); $res.ContentLength64 = $b.Length; $res.OutputStream.Write($b, 0, $b.Length)
        }
        '/api/relatorio' {
          $b = Body $req; $nome = [string]$b.nome; $txt = [string]$b.texto
          if ($nome -notmatch '^semana-\d{4}-\d{2}-\d{2}\.md$' -or $txt.Length -lt 20 -or $txt.Length -gt 300000) { Send $res @{ erro = 'dados inválidos' } 400; break }
          $dir = Join-Path $root 'relatorios'; New-Item -ItemType Directory -Force $dir | Out-Null
          [IO.File]::WriteAllText((Join-Path $dir $nome), $txt, $enc); Send $res @{ ok = $true; arquivo = ('Sala_Agentes/relatorios/' + $nome) }
        }
        '/api/relatorios' {
          $dir = Join-Path $root 'relatorios'
          Send $res @{ itens = @(Get-ChildItem $dir -Filter 'semana-*.md' -ErrorAction SilentlyContinue | Sort-Object Name -Descending | ForEach-Object { $_.Name }) }
        }
        default { Send $res @{ erro = 'rota desconhecida' } 404 }
      }
      continue
    }
    $rel = $path.TrimStart('/'); if (-not $rel) { $rel = 'index.html' }
    $p = [IO.Path]::GetFullPath((Join-Path $root $rel.Replace('/', '\')))
    if (-not $p.StartsWith($root) -or $p.StartsWith((Join-Path $root 'hooks')) -or $p -match 'nuvem\.json$' -or -not (Test-Path $p -PathType Leaf)) { $res.StatusCode = 404; $res.Close(); continue }
    $t = $types[[IO.Path]::GetExtension($p)]; if (-not $t) { $t = 'application/octet-stream' }
    $res.ContentType = $t; $res.AddHeader('Cache-Control', 'no-store')
    $b = [IO.File]::ReadAllBytes($p); $res.ContentLength64 = $b.Length
    $res.OutputStream.Write($b, 0, $b.Length)
  } catch { try { Send $res @{ erro = 'falha interna' } 500 } catch { } } finally { try { $res.Close() } catch { } }
}
