# cap6.ps1 - Capitulo 6 (AS LIMITACOES, quadro 24 = 1 slide = slide 42).
# NAO regera os capitulos anteriores: abre GMS_Defesa.pptx (41 slides), apaga o que houver alem do 41 (idempotente), acrescenta o slide 42, salva e exporta previa/cap6/.
# Uso (depois de cap1 a cap5):  powershell -NoProfile -ExecutionPolicy Bypass -File cap6.ps1 [-SemVideo]
param([switch]$SemVideo)
$ErrorActionPreference='Stop'
. "$PSScriptRoot\gms_lib.ps1"
$root=(Resolve-Path "$PSScriptRoot\..").Path
$pptx=Join-Path $root 'GMS_Defesa.pptx'
$prev=Join-Path $root 'previa\cap6'
if(-not (Test-Path $pptx)){ throw 'GMS_Defesa.pptx nao existe: rode cap1 a cap4 antes.' }
$rot=Get-Roteiro (Join-Path $root 'roteiro.md')

$AMB=$script:CH[4]; $PAR=Mix-Hex $AMB 0.55
$OFF=Mix-Hex $script:T2 0.6          # igual ao do cap5 (funcao fora do escopo / anel apagado)
$CRV=$script:CH[5]                    # vermelho #EF4444 do capitulo 6 (nao chame de $RED: colide com $script:RED da lib, #E2231A, o ponto do carretel)
$LAST=41


function Txt2($s,[string]$name,[string]$text,[double]$x,[double]$top,[double]$size,[hashtable]$o){
  Add-Txt $s $name $text $x ($top+$size*$script:ASC) $size $o }

$null=Open-GmsDeckForAppend $pptx
try {
  if($script:pres.Slides.Count -lt $LAST){ throw "o deck tem menos de $LAST slides: rode cap1 a cap5." }
  while($script:pres.Slides.Count -gt $LAST){ $script:pres.Slides.Item($script:pres.Slides.Count).Delete() }   # idempotente
  $script:slideN=$LAST

  # ---- 42 (24): o anel do MESA-11 recua para a esquerda, apagado; quatro marcadores vermelhos saem dele ----
  $s=New-GmsSlide
  # anel: mesmos 11 arcos (mesmos angulos, mesmos nomes do 41), so a caixa e a cor mudam; centro na coluna 1 a 3 da grade
  $g=Get-Grade 1 3; $cx=$g.x+$g.w/2; $cy=580; $R2=185; $W2=18
  for($j=0;$j -lt 11;$j++){
    $a0=[Math]::Round(32.7273*$j+4.3636,2)
    $null=Add-FioArc $s "!!arcoM$($j+1)" $cx $cy $R2 $R2 $a0 ($a0+24) $OFF $W2 }
  # quatro linhas iguais na grade (colunas 4 a 12): marcador vermelho + titulo + linha secundaria
  $g4=Get-Grade 4 9
  $TX4=@(@('Caso único','uma célula, de uma planta'),
       @('Eu desenvolvi e avaliei','SAP e sensor como fontes externas'),
       @('Pilha proprietária','risco low-code; migração ao Dataverse pedida'),
       @('Acurácia numa máquina','quinze dias; o 3º turno registra menos'))
  $RH=136; $PIT=168
  for($i=0;$i -lt 4;$i++){
    $top=260+$PIT*$i; $n=$i+1
    $null=Add-Box $s "!!marc$n" 5 $g4.x $top 14 $RH $CRV $null 1 0.5
    $xt=$g4.x+14+32
    $null=Txt2 $s "tit$n" $TX4[$i][0] $xt $top 64 @{font=$script:F_COND;bold=$true;color=$script:TX}
    $null=Txt2 $s "sub$n" $TX4[$i][1] $xt ($top+$RH-60) 56 @{color=$script:T2} }
  Add-Moldura $s 'As limitações' $CRV 'O que isto {{não prova}}.' '24 / 28' 'seção 4.10'
  $null=Add-ReelCap $s 1800 985 62 6 1; Set-Notes $s $rot['24']

  foreach($sl in $script:pres.Slides){ $sl.SlideShowTransition.AdvanceOnClick=-1; $sl.SlideShowTransition.AdvanceOnTime=0 }
  Save-GmsDeck $pptx 1.2
  "salvo: $pptx"

  $null=Open-GmsDeck $pptx
  $idx=,42
  Export-GmsSlides $prev 1920 1080 $idx
  "PNGs (slide 42, numeracao do deck): $prev"
  $famL=@('^(tit\d|sub\d|marc\d)$')
  $nviol=Test-GmsLayout -Slides $idx -Families $famL
  "violacoes de layout: $nviol"
  "pdf: $(Export-GmsPdf (Join-Path $prev 'cap6.pdf'))"
  if(-not $SemVideo){
    # video do slide 41 ao 42: copia temporaria sem os slides 1 a 40
    $tmp=Join-Path $env:TEMP 'gms_cap6_video.pptx'
    if(Test-Path $tmp){ Remove-Item $tmp -Force }
    $script:pres.SaveCopyAs($tmp)
    $orig=$script:pres
    $v=$script:app.Presentations.Open($tmp,0,0,0)
    for($i=1;$i -le 40;$i++){ $v.Slides.Item(1).Delete() }
    foreach($sl in $v.Slides){ $sl.SlideShowTransition.Hidden=0 }
    try{ $v.Slides.Item(1).SlideShowTransition.EntryEffect=0 }catch{}
    $script:pres=$v
    $ok=Export-GmsVideo (Join-Path $prev 'cap6.mp4') 3 720 600
    "video: $ok"
    $v.Saved=-1; $v.Close(); $script:pres=$orig
    Remove-Item $tmp -Force -ErrorAction SilentlyContinue
  }
} finally { Close-GmsDeck }
