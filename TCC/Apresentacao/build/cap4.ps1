# cap4.ps1 - Capitulo 4 (A EXPANSAO, quadros 16 a 18 = 11 slides: 16a-16f, 17, 18, 18B1-18B3 = slides 25 a 35).
# NAO regera os capitulos anteriores: abre GMS_Defesa.pptx (24 slides), apaga o que houver alem do 24 (idempotente),
# acrescenta os 11 slides, salva (Save-GmsDeck reaplica o Morph) e exporta previa/cap4/.
# Uso (depois de cap1, cap2 e cap3):  powershell -NoProfile -ExecutionPolicy Bypass -File cap4.ps1 [-SemVideo]
# Slides 33 a 35 (18B1 a 18B3, plano B) ficam OCULTOS; so o ponto 'ligaPlanoB' do slide 32 leva ate o 33 (hiperlink).
param([switch]$SemVideo)
$ErrorActionPreference='Stop'
. "$PSScriptRoot\gms_lib.ps1"
$root=(Resolve-Path "$PSScriptRoot\..").Path
$pptx=Join-Path $root 'GMS_Defesa.pptx'
$prev=Join-Path $root 'previa\cap4'
$telas=Join-Path $root 'assets\telas'
if(-not (Test-Path $pptx)){ throw 'GMS_Defesa.pptx nao existe: rode cap1, cap2 e cap3 antes.' }
$rot=Get-Roteiro (Join-Path $root 'roteiro.md')

$VIO=$script:CH[3]; $VIOL='#C4B5FD'
$TOTAL=8                           # os 8 slides visiveis (25 a 32); o arco violeta cresce de 1/8 a 8/8, monotonico
$script:k=0
function Frac { $script:k++; [double]$script:k/$TOTAL }
$CIT_A='seção 4.1 e Quadro 4'
$FR16='{{O que nasceu numa célula}} e onde chegou.'

function Add-Pic($s,[string]$name,[string]$file,[double]$x,[double]$y,[double]$w,[double]$h){
  $p=$s.Shapes.AddPicture($file,0,-1,[single]($x/2),[single]($y/2),[single]($w/2),[single]($h/2)); $p.Name=$name; $p }

# ---------- quadro 16: nucleo no centro e cinco pontas ----------
$CX=960; $CY=580; $RN=140                      # nucleo (o carretel cresce ate aqui)
# ponta: nome, lado (L|R), linha (0..2), angulo do segmento do anel de onde nasce o fio, titulo, item1, item2
$PT=@(
  @{n=1; side='L'; row=0; ang=247.5; t='Manufatura';   a='8 etapas na estação';     b='Hora-Hora nas TVs'},
  @{n=2; side='R'; row=0; ang=292.5; t='Qualidade';    a='Inspeção e refugo';       b='Carta X̄-R da medida'},
  @{n=3; side='L'; row=1; ang=202.5; t='Planejamento'; a='OP escolhida no plano';   b='Exceção aprovada'},
  @{n=4; side='R'; row=1; ang=337.5; t='Logística';    a='Packing list por pallet'; b='Conferência com o SAP'},
  @{n=5; side='L'; row=2; ang=157.5; t='Engenharia';   a='Delineamento nas telas';  b='Ciclo e paradas no BI'})
$ROWTOP=@(260,492,724)
$TXL=96; $TXR=1210; $NXL=760; $NXR=1160; $DN=36; $DD=16
function Ring-Pt([double]$ang,[double]$r){ @(($CX+$r*[Math]::Cos($ang*[Math]::PI/180)),($CY+$r*[Math]::Sin($ang*[Math]::PI/180))) }

function Add-Quadro16($s,[int]$lit,[bool]$dashed){   # lit = quantas pontas acesas (0..5, ordem 1..5)
  # fios: nascem de um toco de 2 px sob o anel e esticam ate o no
  foreach($q in $PT){
    $nx= if($q.side -eq 'L'){$NXL}else{$NXR}; $ny=$ROWTOP[$q.row]+36
    $st=Ring-Pt $q.ang $RN
    if($q.n -le $lit){ $x2=$nx; $y2=$ny } else { $u=Ring-Pt $q.ang ($RN+2); $x2=$u[0]; $y2=$u[1] }
    $col= if($q.n -le $lit){$VIO}else{Mix-Hex $VIO 0.5}
    $null=Add-FioLine $s "!!fio$($q.n)" $st[0] $st[1] $x2 $y2 $col 6 }
  if($dashed){   # 16f: tres nos tracejados novos (entram por fade), com fios tracejados
    $NT=@(@(1060,850),@(1290,850),@(1520,850))
    for($i=0;$i -lt 3;$i++){
      $st=Ring-Pt @(112.5,67.5,67.5)[$i] $RN
      $l=Add-FioLine $s "fioT$($i+1)" $st[0] $st[1] $NT[$i][0] $NT[$i][1] (Mix-Hex $VIO 0.6) 4; $l.Line.DashStyle=4 } }
  # pontas
  foreach($q in $PT){
    $on=($q.n -le $lit)
    $tx= if($q.side -eq 'L'){$TXL}else{$TXR}; $nx= if($q.side -eq 'L'){$NXL}else{$NXR}
    $bt=$ROWTOP[$q.row]; $ny=$bt+36
    $tc= if($on){$script:TX}else{Mix-Hex $script:T2 0.55}
    $t=Add-Txt $s "!!pt$($q.n)" $q.t $tx ($bt+64*$script:ASC) 64 @{font=$script:F_COND;bold=$true;color=$tc}
    if($on){
      $it=Add-Txt $s "it$($q.n)" "$($q.a)`r$($q.b)" $tx ($bt+76+56*$script:ASC) 56 @{color=(Mix-Hex $script:TX 0.78)}
      $r=$it.TextFrame.TextRange.ParagraphFormat; $r.LineRuleWithin=-1; $r.SpaceWithin=0.9 }
    # no (!!nd): circulo de 18 pt, preenchimento violeta (apagado: 8 pt cinza); o 31 cria os cartoes com outro nome (!!no)
    if($on){ $null=Add-Box $s "!!nd$($q.n)" 5 ($nx-$DN/2) ($ny-$DN/2) $DN $DN $VIO $null 1 0.5 }
    else   { $null=Add-Box $s "!!nd$($q.n)" 5 ($nx-$DD/2) ($ny-$DD/2) $DD $DD (Mix-Hex $script:T2 0.45) $null 1 0.5 } }
  if($dashed){
    $NT=@(@(1060,850),@(1290,850),@(1520,850))
    for($i=0;$i -lt 3;$i++){
      $b=Add-Box $s "!!nt$($i+1)" 5 ($NT[$i][0]-$DN/2) ($NT[$i][1]-$DN/2) $DN $DN $null (Mix-Hex $VIO 0.6) 4 0.5; $b.Line.DashStyle=4 } }
}

# ---------- quadro 17: mosaico 4 x 2 ----------
$CW=408; $CH2=255; $GX=440; $GY=287; $Y0=305
function Card-Pos([int]$col,[int]$row){ @((96+$GX*$col),($Y0+$GY*$row)) }
$ACESOS=@(@(1,'cartao_fila_etapa.png',0,0),@(2,'cartao_paradas.png',1,0),@(3,'cartao_hora_hora.png',2,0),@(4,'cartao_montagem.png',3,0),@(5,'cartao_extrusora.png',0,1))
$TRACE=@(@(1,'cartao_oee_hora.png',1,1),@(2,'cartao_simulador.png',2,1),@(3,'cartao_genealogia.png',3,1))

# ---------- quadro 18 ----------
$TBX=880; $TBY=285; $TBW=944; $TBH=590
$PASSOS=@('1  apontar uma etapa','2  ver o painel reagir','3  achar uma OP')
$PASSY=@(330,440,550)
function Add-Passo($s,[int]$i,[string]$cor){ $null=Add-Txt $s "!!passo$i" $PASSOS[$i-1] 96 ($PASSY[$i-1]+56*$script:ASC) 56 @{color=$cor} }

$null=Open-GmsDeckForAppend $pptx
try {
  if($script:pres.Slides.Count -lt 24){ throw 'o deck tem menos de 24 slides: rode cap1, cap2 e cap3.' }
  while($script:pres.Slides.Count -gt 24){ $script:pres.Slides.Item($script:pres.Slides.Count).Delete() }   # idempotente
  $script:slideN=24
  $fam=@()

  # ---- 25 a 30 (16a a 16f): o carretel vira o nucleo e acende uma ponta por passo ----
  $ids='16a','16b','16c','16d','16e','16f'
  for($j=0;$j -lt 6;$j++){
    $s=New-GmsSlide
    Add-Quadro16 $s $j ($j -eq 5)
    Add-Moldura $s 'A expansão' $VIO $FR16 '16 / 28' $CIT_A
    $null=Add-ReelCap $s $CX $CY $RN 4 (Frac); Set-Notes $s $rot[$ids[$j]] }

  # ---- 31 (17): as pontas viram um mosaico de cartoes ----
  $s=New-GmsSlide
  foreach($c in $ACESOS){ $p=Card-Pos $c[2] $c[3]; $null=Add-Box $s "!!no$($c[0])" 5 $p[0] $p[1] $CW $CH2 $script:SF $VIO 4 0.04 }
  foreach($c in $TRACE){ $p=Card-Pos $c[2] $c[3]; $b=Add-Box $s "!!nt$($c[0])" 5 $p[0] $p[1] $CW $CH2 $null (Mix-Hex $VIO 0.6) 4 0.04; $b.Line.DashStyle=4 }
  foreach($c in $ACESOS){ $p=Card-Pos $c[2] $c[3]; $null=Add-Pic $s ("img_"+$c[1].Replace('.png','')) (Join-Path $telas $c[1]) $p[0] $p[1] $CW $CH2 }
  $TRT=@('OEE por hora',('Simulador de demanda × pessoas' -replace ' × ',([string][char]0xA0+'×'+[char]0xA0)),'Genealogia entre lotes')
  foreach($c in $TRACE){ $p=Card-Pos $c[2] $c[3]   # titulo em texto do PowerPoint, centrado na moldura tracejada
    $t=Add-Txt $s "tt$($c[0])" $TRT[$c[0]-1] ($p[0]+24) ($p[1]+$CH2/2) 40 @{font=$script:F_COND;bold=$true;color=(Mix-Hex $VIOL 0.6);align='m';wrap=($CW-48)}
    $t.Left=($p[0]+$CW/2)/2-$t.Width/2; $t.Top=($p[1]+$CH2/2)/2-$t.Height/2 }
  Add-Moldura $s 'A expansão' $VIO 'O que o dado {{já responde}} e o que falta.' '17 / 28' 'seção 4.3 e Quadro 4'
  $null=Add-ReelCap $s 1800 985 62 4 (Frac); Set-Notes $s $rot['17']

  # ---- 32 (18): o cartao da fila por etapa cresce e vira o tablet ----
  $s=New-GmsSlide
  for($i=1;$i -le 3;$i++){ Add-Passo $s $i $script:TX }
  $null=Add-Txt $s 'nota_tablet' 'No tablet, na mão.' 96 (700+56*$script:ASC) 56 @{color=$script:T2}
  $null=Add-Box $s '!!no1' 5 $TBX $TBY $TBW $TBH $script:SF $VIO 6 0.05
  $anel=Add-Box $s 'pulso_anel' 9 ($TBX+$TBW/2-60) ($TBY+$TBH/2-60) 120 120 $null $script:RED 6
  $pt=Add-Box $s 'pulso_ponto' 9 ($TBX+$TBW/2-24) ($TBY+$TBH/2-24) 48 48 $script:RED $null
  $efs=@()
  try{
    $e=$s.TimeLine.MainSequence.AddEffect($anel,59,0,2)   # 59 = Grow/Shrink; com o anterior: roda sozinho
    $e.Timing.Duration=1.2; $e.Timing.RepeatCount=60; $efs+=$e
  }catch{ Write-Host "animacao de pulso nao aplicada: $($_.Exception.Message)" }
  $dot=Add-Box $s 'ligaPlanoB' 9 96 920 24 24 $script:LN '#8B97A6' 1
  $dot.Line.Transparency=0.5
  Add-Moldura $s 'A expansão' $VIO '{{Agora, ao vivo.}}' '18 / 28' 'demonstração'
  $null=Add-ReelCap $s 1800 985 62 4 (Frac); Set-Notes $s $rot['18']
  $s32=$s; $dot32=$dot

  # ---- 33 a 35 (18B1 a 18B3, OCULTOS): telas recriadas na moldura do tablet ----
  $B=@(@{id='18B1';i=1;f='tela_apontamento.png';h=590},@{id='18B2';i=2;f='tela_painel_celula.png';h=531},@{id='18B3';i=3;f='tela_consulta_op.png';h=590})
  foreach($b in $B){
    $s=New-GmsSlide
    Add-Passo $s $b.i $VIOL
    $ty=$TBY+($TBH-$b.h)/2
    $null=Add-Box $s '!!no1' 5 $TBX $ty $TBW $b.h $script:SF $VIO 6 0.05
    $null=Add-Pic $s ('img_'+$b.f.Replace('.png','')) (Join-Path $telas $b.f) ($TBX+8) ($ty+8) ($TBW-16) ($b.h-16)
    Add-Moldura $s 'A expansão' $VIO 'Agora, {{plano B}}.' '18 / 28' 'telas recriadas, dado fictício'
    $null=Add-ReelCap $s 1800 985 62 4 1.0; Set-Notes $s $rot[$b.id]
    $s.SlideShowTransition.Hidden=-1 }

  # hiperlink do ponto 'ligaPlanoB' (32) -> slide 33
  $s33=$script:pres.Slides.Item(33)
  $as=$dot32.ActionSettings.Item(1)
  $as.Action=7
  $as.Hyperlink.SubAddress=("{0},{1},{2}" -f $s33.SlideID,$s33.SlideIndex,'Plano B')

  foreach($sl in $script:pres.Slides){ $sl.SlideShowTransition.AdvanceOnClick=-1; $sl.SlideShowTransition.AdvanceOnTime=0 }
  Save-GmsDeck $pptx 1.2
  # pulso do 32: repeatCount numerico vira 'indefinite' (ate o fim do slide); senao o CreateVideo estende o slide a 72 s
  $z=[IO.Compression.ZipFile]::Open($pptx,'Update'); $utf8=New-Object Text.UTF8Encoding($false)
  foreach($en in @($z.Entries | Where-Object { $_.FullName -match '^ppt/slides/slide\d+\.xml$' })){
    $r=New-Object IO.StreamReader($en.Open(),$utf8); $x=$r.ReadToEnd(); $r.Close()
    if($x -match 'repeatCount="\d+"'){
      $n=$en.FullName; $x=[regex]::Replace($x,'repeatCount="\d+"','repeatCount="indefinite"'); $en.Delete()
      $ne=$z.CreateEntry($n); $w=New-Object IO.StreamWriter($ne.Open(),$utf8); $w.Write($x); $w.Close(); "pulso: repeatCount=indefinite em $n" } }
  $z.Dispose()
  "salvo: $pptx"

  $null=Open-GmsDeck $pptx
  $idx=25..35
  Export-GmsSlides $prev 1920 1080 $idx
  "PNGs (slides 25 a 35, numeracao do deck): $prev"
  $famL=@('^(!!no|!!nt|img_|tt\d)','^(pulso_|!!no1)','^(!!pt1|it1)$','^(!!pt2|it2)$','^(!!pt3|it3)$','^(!!pt4|it4)$','^(!!pt5|it5)$','^(nucleo|!!barra|!!card)')
  $nviol=Test-GmsLayout -Slides $idx -ExceptAll @('^fioT') -Families $famL
  "violacoes de layout: $nviol"
  "pdf: $(Export-GmsPdf (Join-Path $prev 'cap4.pdf'))"
  if(-not $SemVideo){
    # video do slide 24 (ultimo do cap3) ao 35: copia temporaria sem os slides 1 a 23; os ocultos aparecem so no video
    $tmp=Join-Path $env:TEMP 'gms_cap4_video.pptx'
    if(Test-Path $tmp){ Remove-Item $tmp -Force }
    $script:pres.SaveCopyAs($tmp)
    $orig=$script:pres
    $v=$script:app.Presentations.Open($tmp,0,0,0)
    for($i=1;$i -le 23;$i++){ $v.Slides.Item(1).Delete() }
    foreach($sl in $v.Slides){ $sl.SlideShowTransition.Hidden=0 }
    try{ $v.Slides.Item(1).SlideShowTransition.EntryEffect=0 }catch{}
    $script:pres=$v
    $ok=Export-GmsVideo (Join-Path $prev 'cap4.mp4') 3 720 900
    "video: $ok"
    $v.Saved=-1; $v.Close(); $script:pres=$orig
    Remove-Item $tmp -Force -ErrorAction SilentlyContinue
  }
} finally { Close-GmsDeck }
