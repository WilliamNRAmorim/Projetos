# Servidor estático mínimo com suporte a Range (seek em <video>) e POST /save (grava o render)
$root = 'C:\Users\willi\Downloads\Projetos\Conteudo_Bit'
$work = 'C:\Users\willi\Downloads\Projetos\Conteudo_Bit\Producao'
# ?dir=semana-AAAA-MM-DD no POST /save grava dentro dessa subpasta de Semanal
$out  = Join-Path $root 'Semanal'
$types = @{ '.html'='text/html; charset=utf-8'; '.mp4'='video/mp4'; '.js'='text/javascript'; '.css'='text/css'; '.png'='image/png'; '.jpg'='image/jpeg'; '.wav'='audio/wav'; '.svg'='image/svg+xml'; '.webp'='image/webp'; '.ttf'='font/ttf'; '.woff2'='font/woff2' }
$l = New-Object System.Net.HttpListener
$l.Prefixes.Add('http://127.0.0.1:5179/')
$l.Start()
Write-Host 'listening on http://127.0.0.1:5179/'
while ($l.IsListening) {
  $ctx = $l.GetContext(); $req = $ctx.Request; $res = $ctx.Response
  try {
    $path = [Uri]::UnescapeDataString($req.Url.AbsolutePath)
    if ($req.HttpMethod -eq 'POST' -and $path -eq '/save') {
      $name = [IO.Path]::GetFileName($req.QueryString['name'])
      $dest = $out; $sub = $req.QueryString['dir']
      if ($sub) { $dest = Join-Path $out ([IO.Path]::GetFileName($sub)) }
      New-Item -ItemType Directory -Force $dest | Out-Null
      $fs = [IO.File]::Create((Join-Path $dest $name)); $req.InputStream.CopyTo($fs); $fs.Close()
      Write-Host "saved $name"
      $res.StatusCode = 200; $res.Close(); continue
    }
    # /w/... serve a pasta de trabalho (render.html), o resto serve a pasta do projeto
    if ($path.StartsWith('/w/')) { $base = $work; $rel = $path.Substring(3) } else { $base = $root; $rel = $path.TrimStart('/') }
    $p = [IO.Path]::GetFullPath((Join-Path $base $rel.Replace('/','\')))
    if (-not $p.StartsWith($base) -or -not (Test-Path $p -PathType Leaf)) { $res.StatusCode = 404; $res.Close(); continue }
    $size = (Get-Item $p).Length
    $t = $types[[IO.Path]::GetExtension($p)]; if (-not $t) { $t = 'application/octet-stream' }
    $res.ContentType = $t; $res.AddHeader('Accept-Ranges','bytes'); $res.AddHeader('Cache-Control','no-store')
    $s = 0; $e = $size - 1
    $range = $req.Headers['Range']
    if ($range -match 'bytes=(\d*)-(\d*)') {
      if ($Matches[1]) { $s = [int64]$Matches[1] }
      if ($Matches[2]) { $e = [int64]$Matches[2] }
      $res.StatusCode = 206; $res.AddHeader('Content-Range', "bytes $s-$e/$size")
    }
    $len = $e - $s + 1; $res.ContentLength64 = $len
    $fs = [IO.File]::OpenRead($p); $fs.Seek($s, 'Begin') | Out-Null
    $buf = New-Object byte[] 65536; $left = $len
    while ($left -gt 0) { $n = $fs.Read($buf, 0, [Math]::Min($buf.Length, $left)); if ($n -le 0) { break }; $res.OutputStream.Write($buf, 0, $n); $left -= $n }
    $fs.Close()
  } catch { Write-Host $_ } finally { try { $res.Close() } catch { } }
}

