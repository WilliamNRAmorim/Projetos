# cap2.ps1 - Capitulo 2 (O METODO, quadros 7 a 10 = slides 11 a 14). NAO regera o cap1: abre GMS_Defesa.pptx (10 slides),
# acrescenta os 4 slides, salva (Save-GmsDeck reaplica o Morph) e exporta previa/cap2/.
# Uso (depois de rodar cap1.ps1):  powershell -NoProfile -ExecutionPolicy Bypass -File cap2.ps1 [-SemVideo]
param([switch]$SemVideo)
$ErrorActionPreference='Stop'
. "$PSScriptRoot\gms_lib.ps1"
$root=(Resolve-Path "$PSScriptRoot\..").Path
$pptx=Join-Path $root 'GMS_Defesa.pptx'
$prev=Join-Path $root 'previa\cap2'
if(-not (Test-Path $pptx)){ throw 'GMS_Defesa.pptx nao existe: rode cap1.ps1 antes.' }
$rot=Get-Roteiro (Join-Path $root 'roteiro.md')

$CY=$script:CH[1]                 # ciano do capitulo 2
$CY_L='#67E8F9'; $CY_D='#0E7490'  # turno 1 (manha), turno 3 (noite); o turno 2 usa o proprio ciano
$FR=@(0.25,0.5,0.75,1.0)          # progresso do arco ciano nos 4 quadros
$CX=1000; $CYY=580; $R=270        # anel: centro e raio (px)

function Bead-Pos([int]$k){      # k=1..8: e1 na esquerda do anel, sentido horario
  $a=(180+45*($k-1))*[Math]::PI/180
  @{x=$CX+$R*[Math]::Cos($a); y=$CYY+$R*[Math]::Sin($a)} }
function Add-Beads($s,[string]$modo){
  for($k=1;$k -le 8;$k++){
    if($modo -eq 'anel'){ $p=Bead-Pos $k; $x=$p.x; $y=$p.y } else { $x=114+($k-1)*125; $y=580 }
    $m=Add-Box $s "!!e$k" 5 ($x-18) ($y-18) 36 36 '#0B1118' $CY 4 0.5
    $m.TextFrame.TextRange.Text='' } }
# anel de 24 h: tres arcos de 8 h (06-14, 14-22, 22-06), topo = 0 h. Mesmas caixas em todos os slides; angulos crus.
function Add-Anel($s,[bool]$colapsa){
  if($colapsa){ $T=@(@(179,180),@(179,180),@(179,180)) } else { $T=@(@(2,118),@(122,238),@(242,358)) }
  $cols=@($CY_L,$CY,$CY_D)
  for($i=0;$i -lt 3;$i++){ $null=Add-FioArc $s "!!arcoTurno$($i+1)" $CX $CYY $R $R $T[$i][0] $T[$i][1] $cols[$i] 14 } }
function Add-Seed($s){ $null=Add-FioLine $s '!!fioL1' ($CX-$R) $CYY ($CX-$R+2) $CYY $CY 6 }   # semente do fio (invisivel sob o arco do turno 2)
function Add-Ponta($s,[double]$x,[double]$y){ $null=Add-Box $s '!!pontaFio' 9 ($x-14) ($y-14) 28 28 $script:RED $null }
function Pol([double]$deg){ $a=$deg*[Math]::PI/180; @{x=$CX+$R*[Math]::Cos($a); y=$CYY+$R*[Math]::Sin($a)} }
function Add-Linha($s,$name,$num,$resto,[double]$y){
  $t=Add-Txt $s $name "$num $resto" 96 $y 96 @{font=$script:F_COND;bold=$true}
  $t.TextFrame.TextRange.Characters(1,"$num".Length).Font.Color.RGB=(Get-Rgb $CY); $t }
function Add-Rotulo2($s,$name,$t1,$t2,[double]$x,[double]$top,$cor){
  $t=Add-Txt $s $name "$t1`r$t2" $x ($top+72*$script:ASC) 72 @{font=$script:F_COND;bold=$true;color=$cor}
  $p2=$t.TextFrame.TextRange.Paragraphs(2); $p2.Font.Name=$script:F_LIGHT; $p2.Font.Bold=0; $p2.Font.Size=28; $p2.Font.Color.RGB=(Get-Rgb $script:T2); $t }

$null=Open-GmsDeckForAppend $pptx
try {
  if($script:pres.Slides.Count -lt 10){ throw 'o deck tem menos de 10 slides: rode cap1.ps1.' }
  while($script:pres.Slides.Count -gt 10){ $script:pres.Slides.Item($script:pres.Slides.Count).Delete() }   # idempotente
  $script:slideN=10

  # ---- 11 (quadro 7): relogio de 24 h ----
  $s=New-GmsSlide
  Add-Seed $s
  Add-Anel $s $false
  Add-Beads $s 'anel'
  $null=Add-Txt $s '!!centro' '24 h' $CX 612 96 @{font=$script:F_COND;bold=$true;align='m'}
  $null=Add-Linha $s 'num_semanas' '2' 'semanas' 440
  $null=Add-Linha $s 'num_turnos' '3' 'turnos' 600
  $null=Add-Linha $s 'num_proc' '12' 'processos' 760
  $p=Pol 270; Add-Ponta $s $p.x $p.y
  Add-Moldura $s 'O método' $CY 'Fui ver o trabalho {{onde ele acontece}}.' '7 / 28' 'seção 3.1 (IMAI, 2012; WOMACK; JONES, 1996)'
  $null=Add-ReelCap $s 1800 985 62 2 $FR[0]; Set-Notes $s $rot['7']

  # ---- 12 (quadro 8): o mesmo anel, tres trechos (anel na coluna esquerda; tres cartoes na direita) ----
  $CX=400                           # anel deslocado para a esquerda, alinhado a margem de 96 px (no slide 13 volta a 1000)
  $s=New-GmsSlide
  Add-Seed $s
  Add-Anel $s $false
  Add-Beads $s 'anel'
  $null=Add-Txt $s '!!centro' '24 h' $CX 612 96 @{font=$script:F_COND;bold=$true;align='m'}
  $cardY=@(260,485,710); $cardTxt=@(@('manhã','na estação',$CY_L),@('tarde','desenvolvendo',$CY),@('turno seguinte','versão nova','#22A5C4'))
  for($i=0;$i -lt 3;$i++){
    $null=Add-Box $s "cartao_trecho$($i+1)" 1 800 $cardY[$i] 880 190 $script:SF $script:LN 3
    $null=Add-Rotulo2 $s "trecho_$(@('manha','tarde','noite')[$i])" $cardTxt[$i][0] $cardTxt[$i][1] 840 ($cardY[$i]+22) $cardTxt[$i][2] }
  $p=Pol 60; Add-Ponta $s $p.x $p.y
  Add-Moldura $s 'O método' $CY 'Um {{ciclo}} por dia.' '8 / 28' 'seção 3.2 (DI RUSCIO et al., 2022)'
  $null=Add-ReelCap $s 1800 985 62 2 $FR[1]; Set-Notes $s $rot['8']
  $CX=1000

  # ---- 13 (quadro 9): o anel vira fio e bate no muro ----
  $s=New-GmsSlide
  $null=Add-FioLine $s '!!fioL1' 96 580 1660 580 $CY 6
  Add-Anel $s $true
  Add-Beads $s 'fio'
  # muro de blocos (governanca de TI): 2 colunas x 5 linhas, a linha do meio e a passagem
  for($r=0;$r -lt 5;$r++){ if($r -eq 2){ continue }; for($c=0;$c -lt 2;$c++){ $null=Add-Box $s "muro_$r$c" 1 (1180+120*$c) (380+80*$r) 120 80 $script:SF $script:LN 3 } }
  $pa=Add-Box $s '!!passagem' 1 1180 540 240 80 $CY $CY 4; $pa.Fill.Transparency=0.65
  $null=Add-Txt $s 'rotulo_muro' 'governança de TI' 1300 322 56 @{color=$script:T2;align='m'}
  $null=Add-Txt $s 'rotulo_passagem' 'plataforma homologada' 1300 872 56 @{color=$CY;align='m'}
  Add-Ponta $s 1660 580
  Add-Moldura $s 'O método' $CY '{{Low-code por restrição}}, não por preferência.' '9 / 28' 'seção 1 e 2.2 (DI RUSCIO et al., 2022)'
  $null=Add-ReelCap $s 1800 985 62 2 $FR[2]; Set-Notes $s $rot['9']

  # ---- 14 (quadro 10): a passagem vira a tela do tablet ----
  $s=New-GmsSlide
  $null=Add-FioLine $s '!!fioL1' 96 580 520 580 $CY 6
  $tb=Add-Box $s '!!tablet' 5 520 290 880 580 $script:SF $script:T2 4 0.06
  $pa=Add-Box $s '!!passagem' 1 548 318 824 524 '#0B1A22' $CY 4
  $bt=Add-Box $s 'botao' 1 685 520 340 120 $CY $null 2
  $r=$bt.TextFrame.TextRange; $r.Text='APONTAR'; $r.Font.Name=$script:F_COND; $r.Font.Bold=-1; $r.Font.Size=36; $r.Font.Color.RGB=(Get-Rgb $script:BG); $r.ParagraphFormat.Alignment=2; $bt.TextFrame.VerticalAnchor=3
  $l=Add-VLine $s 1065 520 120; $l.Name='cota_v'; Set-Line $l $CY 3
  $l=Add-FioLine $s 'cota_t1' 1045 520 1085 520 $CY 3
  $l=Add-FioLine $s 'cota_t2' 1045 640 1085 640 $CY 3
  $null=Add-Txt $s 'cota_txt' '48 px' 1095 598 56 @{font=$script:F_MONO;color=$CY}
  $lv=Add-Box $s 'luva' 5 805 635 110 230 '#1B2430' $script:T2 4 0.5; $lv.Rotation=-20
  Add-Ponta $s 821 650
  Add-Moldura $s 'O método' $CY 'Avisar, {{não bloquear}}.' '10 / 28' 'seção 2.5 e 3.4 (ATKIN et al., 2017)'
  $null=Add-ReelCap $s 1800 985 62 2 $FR[3]; Set-Notes $s $rot['10']

  foreach($sl in $script:pres.Slides){ $sl.SlideShowTransition.AdvanceOnClick=-1; $sl.SlideShowTransition.AdvanceOnTime=0 }
  Save-GmsDeck $pptx 1.2
  "salvo: $pptx"

  $null=Open-GmsDeck $pptx
  Export-GmsSlides $prev 1920 1080 @(11,12,13,14)
  "PNGs (slides 11 a 14, numeracao do deck): $prev"
  $nviol=Test-GmsLayout -Slides 11,12,13,14 -Families @('^(muro|!!passagem)','^(!!tablet|!!passagem|botao|cota|luva)','^(cartao_trecho|trecho_)')
  "violacoes de layout: $nviol"
  "pdf: $(Export-GmsPdf (Join-Path $prev 'cap2.pdf'))"
  if(-not $SemVideo){
    # video so do fim do cap1 (slide 10) ao slide 14: copia temporaria sem os slides 1 a 9
    $tmp=Join-Path $env:TEMP 'gms_cap2_video.pptx'
    if(Test-Path $tmp){ Remove-Item $tmp -Force }
    $script:pres.SaveCopyAs($tmp)
    $orig=$script:pres
    $v=$script:app.Presentations.Open($tmp,0,0,0)
    for($i=1;$i -le 9;$i++){ $v.Slides.Item(1).Delete() }
    try{ $v.Slides.Item(1).SlideShowTransition.EntryEffect=0 }catch{}
    $script:pres=$v
    $ok=Export-GmsVideo (Join-Path $prev 'cap2.mp4') 3 720 300
    "video: $ok"
    $v.Saved=-1; $v.Close(); $script:pres=$orig
    Remove-Item $tmp -Force -ErrorAction SilentlyContinue
  }
} finally { Close-GmsDeck }
