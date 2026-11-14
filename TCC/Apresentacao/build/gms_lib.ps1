# gms_lib.ps1 - funcoes reutilizaveis para montar a apresentacao de defesa por COM do PowerPoint.
# Convencao: todas as coordenadas e tamanhos de entrada estao em px de uma prancha 1920x1080
# (1 px = 0,5 pt; o slide tem 960x540 pt). Tamanhos de fonte tambem em px (fonte pt = px/2).
# Dot-source: . "$PSScriptRoot\gms_lib.ps1"

Add-Type -AssemblyName System.IO.Compression, System.IO.Compression.FileSystem

$script:BG='#07090D'; $script:SF='#10151C'; $script:LN='#232B36'; $script:TX='#F5F7FA'; $script:T2='#8B97A6'
$script:GR='#A9C7A0'; $script:SE='#C9B79A'; $script:RED='#E2231A'; $script:INK='#26386E'; $script:GD='#2F4A2A'
$script:CH=@('#3B82F6','#06B6D4','#6366F1','#8B5CF6','#F59E0B','#EF4444','#F97316','#10B981')
$script:F_COND='Bahnschrift Condensed'; $script:F_LIGHT='Bahnschrift SemiLight'; $script:F_SEMI='Bahnschrift SemiBold'
$script:F_MONO='Consolas'; $script:F_HAND='Ink Free'
$script:ASC=0.93   # distancia do topo da caixa de texto ate a linha de base, em fracao do corpo (calibrada)

function Get-Rgb([string]$h){ $h=$h.TrimStart('#'); [int]("0x"+$h.Substring(0,2)) + 256*[int]("0x"+$h.Substring(2,2)) + 65536*[int]("0x"+$h.Substring(4,2)) }
function Mix-Hex([string]$h,[double]$a){   # mistura a cor com o fundo (simula opacidade a)
  $h=$h.TrimStart('#'); $b=$script:BG.TrimStart('#'); $o=''
  for($i=0;$i -lt 6;$i+=2){ $c=[int]("0x"+$h.Substring($i,2)); $d=[int]("0x"+$b.Substring($i,2)); $o+=('{0:X2}' -f [int][Math]::Round($d+($c-$d)*$a)) }
  '#'+$o }

# ---------- deck ----------
function New-GmsDeck {
  $script:ownApp = (@(Get-Process POWERPNT -ErrorAction SilentlyContinue).Count -eq 0)
  $script:app = New-Object -ComObject PowerPoint.Application
  $script:pres = $script:app.Presentations.Add(0)
  $script:pres.PageSetup.SlideWidth=960; $script:pres.PageSetup.SlideHeight=540
  $m=$script:pres.SlideMaster.Background.Fill; $m.Solid(); $m.ForeColor.RGB=(Get-Rgb $script:BG)
  $script:slideN=0
  $script:pres
}
function New-GmsSlide {
  $script:slideN++
  $s=$script:pres.Slides.Add($script:slideN,12)   # ppLayoutBlank
  $s.FollowMasterBackground=-1
  while($s.Shapes.Count -gt 0){ $s.Shapes.Item(1).Delete() }
  $s
}
function Close-GmsDeck {
  try{ if($script:pres){ $script:pres.Saved=-1; $script:pres.Close() } }catch{}
  $script:pres=$null
  try{ if($script:ownApp -and $script:app){ $script:app.Quit() } }catch{}
  $script:app=$null
  [GC]::Collect(); [GC]::WaitForPendingFinalizers()
}

# ---------- formas ----------
function Set-Fill($sh,$hex,[double]$transp=0){
  if($hex){ $sh.Fill.Visible=-1; $sh.Fill.Solid(); $sh.Fill.ForeColor.RGB=(Get-Rgb $hex); $sh.Fill.Transparency=$transp } else { $sh.Fill.Visible=0 } }
function Set-Line($sh,$hex,[double]$wpx=2){
  if($hex){ $sh.Line.Visible=-1; $sh.Line.ForeColor.RGB=(Get-Rgb $hex); $sh.Line.Weight=$wpx/2 } else { $sh.Line.Visible=0 } }
function Add-Box($s,$name,[int]$type,[double]$x,[double]$y,[double]$w,[double]$h,$fill,$line,[double]$lwpx=2,[double]$adj=-1){
  $sh=$s.Shapes.AddShape($type,10,10,[Math]::Max($w/2,1),[Math]::Max($h/2,1)); $sh.Name=$name; try{ $sh.Left=$x/2; $sh.Top=$y/2; $sh.Width=$w/2; $sh.Height=$h/2 }catch{ throw "Add-Box $name x=$x y=$y w=$w h=$h" }
  Set-Fill $sh $fill; Set-Line $sh $line $lwpx
  if($adj -ge 0){ $sh.Adjustments.Item(1)=$adj }
  $sh.Shadow.Visible=0; $sh }

# texto: y = linha de base (px). o: font, bold, color, align (l|m|r), wrap (largura px), glow (cor), round (usa forma arredondada), name
function Add-Txt($s,$name,[string]$text,[double]$x,[double]$y,[double]$size,[hashtable]$o=@{}){
  $pt=$size/2
  $tb=$s.Shapes.AddTextbox(1,$x/2,0,200,$pt*1.3); $tb.Name=$name
  $tf=$tb.TextFrame2; $tf.MarginLeft=0;$tf.MarginRight=0;$tf.MarginTop=0;$tf.MarginBottom=0
  $tf.VerticalAnchor=1
  if($o.wrap){ $tf.WordWrap=-1; $tb.Width=[single](([double]$o.wrap)/2) } else { $tf.WordWrap=0 }
  $tf.AutoSize=1
  $tb.TextFrame.TextRange.Text=$text
  $r=$tb.TextFrame.TextRange
  $fn= if($o.font){$o.font}else{$script:F_LIGHT}
  $r.Font.Name=$fn; $r.Font.Size=$pt; $r.Font.Bold= if($o.bold){-1}else{0}
  $r.Font.Color.RGB=(Get-Rgb $(if($o.color){$o.color}else{$script:TX}))
  $r.ParagraphFormat.Alignment= switch($o.align){ 'm'{2} 'r'{3} default{1} }
  if($o.spacing){ $tb.TextFrame2.TextRange.Font.Spacing=$o.spacing }
  if($o.glow){ $g=$tb.TextFrame2.TextRange.Font.Glow; $g.Radius=8; $g.Color.RGB=(Get-Rgb $o.glow); $g.Transparency=0.55 }
  if($o.round){ $tb.AutoShapeType=5; $tb.Adjustments.Item(1)=0; Set-Fill $tb $o.round 1 }
  if(-not $o.wrap){
    $w=$tb.Width
    switch($o.align){ 'm'{ $tb.Left=$x/2-$w/2 } 'r'{ $tb.Left=$x/2-$w } default{ $tb.Left=$x/2 } }
  }
  $tb.Top=$y/2-$pt*$script:ASC
  $tb }

# carretel: 8 arcos fantasmas + arco 1 aceso (frac 0..1) + ponto vermelho. cx,cy,r em px.
# Obs.: o arco nasce como o quadrante superior direito da elipse; ao ajustar os angulos o PowerPoint
# expande o quadro para a elipse inteira (esquerda e baixo). Por isso a caixa inicial e (cx, cy-r, r, r).
function Add-Reel($s,[double]$cx,[double]$cy,[double]$r,[double]$frac){
  $rp=$r/2; $lw=$r*18/82   # px
  for($k=0;$k -lt 8;$k++){
    $a0=(-86+45*$k+360)%360; $a1=(-86+45*$k+37+360)%360
    $sh=$s.Shapes.AddShape(25,$cx/2,$cy/2-$rp,$rp,$rp); $sh.Name="!!arco$($k+1)"
    $sh.Adjustments.Item(1)=$a0; $sh.Adjustments.Item(2)=$a1
    $sh.Fill.Visible=0; Set-Line $sh $script:LN ($lw*0.6); $sh.Shadow.Visible=0
  }
  $f=[Math]::Max($frac,0.004)
  $sh=$s.Shapes.AddShape(25,$cx/2,$cy/2-$rp,$rp,$rp); $sh.Name='!!arcoLuz'
  $sh.Adjustments.Item(1)=274; $sh.Adjustments.Item(2)=(274+37*$f)%360
  $sh.Fill.Visible=0; Set-Line $sh $script:CH[0] $lw; $sh.Shadow.Visible=0
  $ang= if($frac -gt 0){-86+37*$frac}else{-90}
  $px=$cx+$r*[Math]::Cos($ang*[Math]::PI/180); $py=$cy+$r*[Math]::Sin($ang*[Math]::PI/180)
  $d=$r*11.2/82*2
  $p=Add-Box $s '!!ponto' 9 ($px-$d/2) ($py-$d/2) $d $d $script:RED $null
  @{x=$px;y=$py}
}

# fio: path em px estilo SVG: "M x y L x y C x1 y1 x2 y2 x y ..." (so M, L e C)
function Add-Wire($s,$name,[string]$d,$color,[double]$wpx=6,[switch]$dash){
  $t=($d -replace '([MLC])',' $1 ').Trim() -split '\s+'; $i=0; $ff=$null
  while($i -lt $t.Count){
    $c=$t[$i]; $i++
    switch($c){
      'M' { $ff=$s.Shapes.BuildFreeform(1,[single]([double]$t[$i]/2),[single]([double]$t[$i+1]/2)); $i+=2 }
      'L' { $ff.AddNodes(0,0,[single]([double]$t[$i]/2),[single]([double]$t[$i+1]/2)); $i+=2 }
      'C' { $v=@(); for($k=0;$k -lt 6;$k++){ $v+=[single]([double]$t[$i+$k]/2) }; $ff.AddNodes(1,1,$v[0],$v[1],$v[2],$v[3],$v[4],$v[5]); $i+=6 }
    }
  }
  $sh=$ff.ConvertToShape(); $sh.Name=$name; $sh.Fill.Visible=0; Set-Line $sh $color $wpx; $sh.Shadow.Visible=0
  if($dash){ $sh.Line.DashStyle=4 }
  $sh }

function Add-VLine($s,[double]$x,[double]$y,[double]$len){ $l=$s.Shapes.AddLine(10,10,10,10+$len/2); $l.Left=$x/2; $l.Top=$y/2; $l }


# fio feito so de formas predefinidas (linhas e arcos, sem preenchimento): o Morph interpola sem preencher.
function Add-FioLine($s,$name,[double]$x1,[double]$y1,[double]$x2,[double]$y2,$color,[double]$wpx=6){
  $l=$s.Shapes.AddLine($x1/2,$y1/2,$x2/2,$y2/2); $l.Name=$name; $l.Fill.Visible=0; Set-Line $l $color $wpx; $l.Shadow.Visible=0; $l }
# arco de elipse (centro cx,cy; raios rx,ry; angulos em graus, sentido horario a partir das 3h)
function Add-FioArc($s,$name,[double]$cx,[double]$cy,[double]$rx,[double]$ry,[double]$a0,[double]$a1,$color,[double]$wpx=6){
  $sh=$s.Shapes.AddShape(25,$cx/2,$cy/2-$ry/2,[Math]::Max($rx/2,1),[Math]::Max($ry/2,0.5)); $sh.Name=$name
  $sh.Adjustments.Item(1)=$a0; $sh.Adjustments.Item(2)=$a1   # angulos crus (monotonicos) para o Morph interpolar em linha reta
  $sh.Fill.Visible=0; Set-Line $sh $color $wpx; $sh.Shadow.Visible=0; $sh }

# ficha de papel (dado ficticio fica nos objetos !!n1..!!n4, fora do grupo). Retorna o grupo.
# op: opacidade 0..1 (simulada por mistura com o fundo). Textos so se w >= 300 px.
function Add-Ficha($s,[double]$x,[double]$y,[double]$w,[double]$op=1,[string]$name='!!ficha'){
  $h=1.25*$w; $sw=[Math]::Max(1.5,$w*0.003); $names=@()
  $cGR=Mix-Hex $script:GR $op; $cHD=Mix-Hex '#94B58A' $op; $cLN=Mix-Hex '#5E7F57' $op; $cGD=Mix-Hex $script:GD $op
  $mk={ param($nm,$sh) $sh.Name="$name`_$nm"; $script:names2+=@("$name`_$nm") }
  $script:names2=@()
  $b=Add-Box $s "$name`_papel" 1 $x $y $w $h $cGR $null; $script:names2+=$b.Name
  $b=Add-Box $s "$name`_topo" 1 $x $y $w ($h*0.12) $cHD $null; $script:names2+=$b.Name
  $txt=($w -ge 300)
  if($txt){ $t=Add-Txt $s "$name`_titulo" 'CONTROLE DE ETAPAS · CÉLULA' ($x+0.06*$w) ($y+$h*0.08) ($w*0.04) @{font=$script:F_MONO;color=$cGD}; $script:names2+=$t.Name }
  $lab='OP','METRAGEM','OPERADOR','TURNO'
  for($i=0;$i -lt 4;$i++){
    $ry=$y+$h*(0.16+0.14*$i)
    $b=Add-Box $s "$name`_linha$i" 1 ($x+0.04*$w) $ry (0.92*$w) ($h*0.14) $null $cLN $sw; $script:names2+=$b.Name
    $l=Add-VLine $s ($x+0.45*$w) $ry ($h*0.14); $l.Name="$name`_div$i"; Set-Line $l $cLN $sw; $script:names2+=$l.Name
    if($txt){ $t=Add-Txt $s "$name`_rot$i" $lab[$i] ($x+0.07*$w) ($ry+$h*0.085) ($w*0.045) @{font=$script:F_MONO;color=$cGD}; $script:names2+=$t.Name }
  }
  $gy=$y+$h*0.74
  $b=Add-Box $s "$name`_grade" 1 ($x+0.04*$w) $gy (0.92*$w) ($h*0.13) $null $cLN $sw; $script:names2+=$b.Name
  for($j=1;$j -lt 3;$j++){ $xx=($x+0.04*$w+$j*0.3067*$w)/2; $l=Add-VLine $s ($xx*2) $gy ($h*0.13); $l.Name="$name`_gdiv$j"; Set-Line $l $cLN $sw; $script:names2+=$l.Name }
  if($txt){
    $et='TRANÇAGEM','DEBANDAGEM','EXTR./TESTE'
    for($j=0;$j -lt 3;$j++){ $t=Add-Txt $s "$name`_et$j" $et[$j] ($x+0.06*$w+$j*0.3067*$w) ($gy+$h*0.04+$w*0.028*0.4) ($w*0.028) @{font=$script:F_MONO;color=$cGD}; $script:names2+=$t.Name }
    $t=Add-Txt $s "$name`_sup" 'SUPERVISÃO: ____________' ($x+0.06*$w) ($y+$h*0.95) ($w*0.035) @{font=$script:F_MONO;color=$cGD}; $script:names2+=$t.Name
  }
  $g=$s.Shapes.Range([object[]]$script:names2).Group(); $g.Name=$name; $g }

# notas do apresentador
function Set-Notes($s,[string]$text){
  $s.NotesPage.Shapes.Placeholders.Item(2).TextFrame.TextRange.Text=$text }

# anima entrada (fade) por clique de uma forma que NAO participa do Morph
function Add-ClickFade($s,$shapes){
  $first=$true
  foreach($sh in $shapes){
    $e=$s.TimeLine.MainSequence.AddEffect($sh,10,0, $(if($first){1}else{2}))   # 10=Fade; 1=on click, 2=with previous
    $first=$false } }

# le o roteiro.md: devolve hashtable id -> texto de notas ("[tempo · acumulado]" + fala)
function Get-Roteiro([string]$path){
  $lines=[IO.File]::ReadAllLines($path,[Text.Encoding]::UTF8); $res=[ordered]@{}; $id=$null; $buf=@()
  $flush={ if($id){ $res[$id]=($buf -join "`r").Trim() } }
  foreach($ln in $lines){
    if($ln -match '^### (\S+) · (\S+)(?: · [^·]*?)? · acumulado (\S+)\s*$'){ & $flush; $id=$Matches[1]; $buf=@("[$($Matches[2]) · $($Matches[3])]"); continue }
    if($ln -match '^## '){ & $flush; $id=$null; continue }
    if($id){ if($ln -match '^Na tela:'){ continue }; if($ln.Trim() -eq ''){ continue }; $buf+=($ln -replace '\*\*','') }
  }
  & $flush; $res }

# ---------- salvar, pos-processar XML, exportar ----------
function Save-GmsDeck([string]$path,[double]$morphDur=1.2){
  if(Test-Path $path){ Remove-Item $path -Force }
  $script:pres.SaveAs($path,24)
  $script:pres.Close(); $script:pres=$null
  $z=[IO.Compression.ZipFile]::Open($path,'Update')
  $utf8=New-Object Text.UTF8Encoding($false)
  $rd={ param($e) $r=New-Object IO.StreamReader($e.Open(),$utf8); $t=$r.ReadToEnd(); $r.Close(); $t }
  $wr={ param($n,$t) $z.GetEntry($n).Delete(); $en=$z.CreateEntry($n); $w=New-Object IO.StreamWriter($en.Open(),$utf8); $w.Write($t); $w.Close() }
  $dur=[int]($morphDur*1000)
  $tr='<mc:AlternateContent xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006"><mc:Choice xmlns:p159="http://schemas.microsoft.com/office/powerpoint/2015/09/main" xmlns:p14="http://schemas.microsoft.com/office/powerpoint/2010/main" Requires="p159"><p:transition spd="slow" p14:dur="'+$dur+'"><p159:morph option="byObject"/></p:transition></mc:Choice><mc:Fallback><p:transition spd="slow"><p:fade/></p:transition></mc:Fallback></mc:AlternateContent>'
  $names=@($z.Entries | ForEach-Object { $_.FullName } | Where-Object { $_ -match '^ppt/slides/slide\d+\.xml$' })
  foreach($nm in $names){
    $num=[int]($nm -replace '\D','')
    $x=& $rd $z.GetEntry($nm)
    # ponta redonda no traco dos arcos e dos fios
    $x=[regex]::Replace($x,'<p:(sp|cxnSp)>.*?</p:\1>',{ param($m)
      $v=$m.Value
      if($v -match 'name="!!(arco|fio)'){ $v=$v -replace '<a:ln( w="\d+")?>','<a:ln$1 cap="rnd">' ; $v=$v -replace '<a:ln( w="\d+")? cap="rnd">','<a:ln$1 cap="rnd">' }
      if($v -match 'name="!!(arco|fio)'){
        # sem preenchimento de verdade: noFill no spPr e fillRef 0 no estilo (senao o Morph pinta o arco)
        if($v -notmatch '</a:prstGeom><a:noFill/>' -and $v -match '</a:prstGeom>'){ $v=$v -replace '</a:prstGeom>','</a:prstGeom><a:noFill/>' }
        $v=$v -replace '<a:fillRef idx="\d+">','<a:fillRef idx="0">' }
      $v },'Singleline')
    if($num -ge 2){
      $x=$x -replace '<p:transition[^>]*/>',''
      $x=$x -replace '</p:clrMapOvr>',('</p:clrMapOvr>'+$tr)
    }
    & $wr $nm $x
  }
  # propriedades do arquivo: sem autor nem empresa
  $c=& $rd $z.GetEntry('docProps/core.xml')
  $c=$c -replace '<dc:creator>.*?</dc:creator>','<dc:creator></dc:creator>' -replace '<cp:lastModifiedBy>.*?</cp:lastModifiedBy>','<cp:lastModifiedBy></cp:lastModifiedBy>'
  & $wr 'docProps/core.xml' $c
  $a=& $rd $z.GetEntry('docProps/app.xml')
  $a=$a -replace '<Company>.*?</Company>','<Company></Company>' -replace '<Manager>.*?</Manager>',''
  & $wr 'docProps/app.xml' $a
  $z.Dispose()
}
function Open-GmsDeck([string]$path){
  if(-not $script:app){ $script:ownApp=(@(Get-Process POWERPNT -ErrorAction SilentlyContinue).Count -eq 0); $script:app=New-Object -ComObject PowerPoint.Application }
  $script:pres=$script:app.Presentations.Open($path,0,0,0); $script:pres }
function Export-GmsSlides([string]$dir,[int]$w=1920,[int]$h=1080){
  New-Item -ItemType Directory -Force $dir | Out-Null
  foreach($s in $script:pres.Slides){ $s.Export((Join-Path $dir ('slide_{0:D2}.png' -f $s.SlideIndex)),'PNG',$w,$h) } }
function Export-GmsVideo([string]$mp4,[int]$secPerSlide=3,[int]$vres=720,[int]$timeoutSec=300){
  New-Item -ItemType Directory -Force (Split-Path $mp4) | Out-Null
  if(Test-Path $mp4){ Remove-Item $mp4 -Force }
  $script:pres.CreateVideo($mp4,0,$secPerSlide,$vres,30,85)
  $t0=Get-Date
  while($true){
    $st=$script:pres.CreateVideoStatus   # 0 nao iniciado, 1 em curso, 2 na fila, 3 concluido, 4 falhou
    if($st -eq 3){ return $true }
    if($st -eq 4){ return $false }
    if(((Get-Date)-$t0).TotalSeconds -gt $timeoutSec){ return $false }
    Start-Sleep -Seconds 2 } }
