# Soma tokens e custo por dia, por agente e por modelo, lendo as transcricoes locais do Claude Code.
# Uso: powershell -NoProfile -ExecutionPolicy Bypass -File uso.ps1 [AAAA-MM-DD]   (padrao: hoje, hora local)
# Nada sai da maquina. Gera relatorios\uso_AAAA-MM-DD.md
param([string]$Dia = (Get-Date -Format 'yyyy-MM-dd'))
$ErrorActionPreference = 'Stop'
$aqui = Split-Path -Parent $MyInvocation.MyCommand.Path
$raiz = Join-Path $env:USERPROFILE '.claude\projects'
$precos = (Get-Content (Join-Path $aqui 'precos.json') -Raw -Encoding UTF8 | ConvertFrom-Json).modelos

$msgs = @{}   # chave = id da mensagem: a mesma resposta aparece em varias linhas e em sessoes retomadas; vale a de maior saida
$pastas = Get-ChildItem $raiz -Directory | Where-Object { $_.Name -like 'C--Users-willi-Downloads-Projetos*' }
foreach ($p in $pastas) {
  Get-ChildItem $p.FullName -Recurse -Filter *.jsonl | ForEach-Object {
    $arq = $_.FullName
    $ag = 'principal'
    if ($arq -like '*\subagents\*') {
      if ($_.Name -like 'agent-acompact-*') { $ag = 'compactacao' }
      else {
        $meta = $arq -replace '\.jsonl$', '.meta.json'
        $ag = 'subagente'
        if (Test-Path $meta) { try { $ag = (Get-Content $meta -Raw -Encoding UTF8 | ConvertFrom-Json).agentType } catch {} }
      }
    }
    Select-String -Path $arq -Pattern '"type":"assistant"' -SimpleMatch -Encoding UTF8 | ForEach-Object {
      try { $o = $_.Line | ConvertFrom-Json } catch { return }
      if (-not $o.message -or -not $o.message.usage -or -not $o.message.id) { return }
      if (([datetimeoffset]$o.timestamp).ToLocalTime().ToString('yyyy-MM-dd') -ne $Dia) { return }
      $u = $o.message.usage
      $w1h = 0L; if ($u.cache_creation -and $u.cache_creation.ephemeral_1h_input_tokens) { $w1h = [long]$u.cache_creation.ephemeral_1h_input_tokens }
      $w5m = [long]$u.cache_creation_input_tokens - $w1h; if ($w5m -lt 0) { $w5m = 0 }
      $buscas = 0L; if ($u.server_tool_use -and $u.server_tool_use.web_search_requests) { $buscas = [long]$u.server_tool_use.web_search_requests }
      $d = [pscustomobject]@{ ag = $ag; mod = [string]$o.message.model; i = [long]$u.input_tokens; cw = $w5m; cw1 = $w1h; cr = [long]$u.cache_read_input_tokens; o = [long]$u.output_tokens; b = $buscas }
      $k = [string]$o.message.id
      if (-not $msgs.ContainsKey($k) -or $d.o -ge $msgs[$k].o) { $msgs[$k] = $d }
    }
  }
}

$tab = @{}; $semPreco = $false; $buscasTotal = 0L
foreach ($d in $msgs.Values) {
  $k = "$($d.ag)|$($d.mod)"
  if (-not $tab.ContainsKey($k)) { $tab[$k] = @{ ag = $d.ag; mod = $d.mod; n = 0; i = 0L; cw = 0L; cw1 = 0L; cr = 0L; o = 0L; usd = 0.0; sp = $false } }
  $t = $tab[$k]; $t.n++; $t.i += $d.i; $t.cw += $d.cw; $t.cw1 += $d.cw1; $t.cr += $d.cr; $t.o += $d.o; $buscasTotal += $d.b
  $p = $precos.($d.mod)
  if ($p) { $t.usd += ($d.i * $p.input + $d.cw * $p.cache_write + $d.cw1 * $p.cache_write_1h + $d.cr * $p.cache_read + $d.o * $p.output) / 1e6 } else { $t.sp = $true; $semPreco = $true }
}

$l = New-Object System.Collections.Generic.List[string]
$l.Add("# Uso de tokens em $Dia"); $l.Add('')
$l.Add('Fonte: transcricoes locais do Claude Code (todas as pastas do projeto). Custo em USD pelos precos de `precos.json` (lista, sem desconto).'); $l.Add('')
$l.Add('| Agente | Modelo | Respostas | Entrada | Cache escrita 5m | Cache escrita 1h | Cache leitura | Saida | USD |')
$l.Add('|---|---|---|---|---|---|---|---|---|')
$total = 0.0
foreach ($t in ($tab.Values | Sort-Object { -$_.usd })) {
  $total += $t.usd
  $usd = if ($t.sp) { 'sem preco' } else { '{0:N4}' -f $t.usd }
  $l.Add(('| {0} | {1} | {2} | {3:N0} | {4:N0} | {5:N0} | {6:N0} | {7:N0} | {8} |' -f $t.ag, $t.mod, $t.n, $t.i, $t.cw, $t.cw1, $t.cr, $t.o, $usd))
}
$l.Add('')
if ($tab.Count) { $l.Add(('**Total do dia: US$ {0:N4}**' -f $total)) } else { $l.Add('Nenhum uso encontrado neste dia.') }
if ($semPreco) { $l.Add(''); $l.Add('**ATENCAO: ha modelo sem preco em `precos.json`; o total esta incompleto.**') }
if ($buscasTotal -gt 0) { $l.Add(''); $l.Add(('Buscas na web no dia: {0} (US$ 10 por mil, fora do total acima).' -f $buscasTotal)) }
New-Item -ItemType Directory -Force (Join-Path $aqui 'relatorios') | Out-Null
$saida = Join-Path $aqui "relatorios\uso_$Dia.md"
$l | Set-Content $saida -Encoding UTF8
$saida
