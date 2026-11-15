# cap8.ps1 - Capitulo 8 (A TESE, quadros 27 e 28 = 2 slides = slides 47 e 48).
# NAO regera os capitulos anteriores: abre GMS_Defesa.pptx (46 slides), apaga o que houver alem do 46 (idempotente), acrescenta os 2 slides, salva e exporta previa/cap8/.
# Uso (depois de cap1 a cap7):  powershell -NoProfile -ExecutionPolicy Bypass -File cap8.ps1 [-SemVideo]
# Mangueira: o COM nao insere modelo 3D; as pontas sao as imagens de assets/pecas/pc_terminal_on.png (a da direita espelhada)
# e o corpo e uma LINHA GROSSA (!!fio1, a mesma linha que sai do nucleo no 46) mais uma linha clara fina (!!fio2) para dar volume.
param([switch]$SemVideo)
$ErrorActionPreference='Stop'
. "$PSScriptRoot\gms_lib.ps1"
$root=(Resolve-Path "$PSScriptRoot\..").Path
$pptx=Join-Path $root 'GMS_Defesa.pptx'
$prev=Join-Path $root 'previa\cap8'
$pecas=Join-Path $root 'assets\pecas'
if(-not (Test-Path $pptx)){ throw 'GMS_Defesa.pptx nao existe: rode cap1 a cap7 antes.' }
$rot=Get-Roteiro (Join-Path $root 'roteiro.md')

# ATENCAO: nomes de variavel nao diferenciam maiusculas; nao use $BG, $RED, $GR, $TX, $T2, $CH, $LN, $SF (colidem com a lib).
$VRD=$script:CH[7]                 # verde #10B981 (capitulo 8)
$ORG=$script:CH[6]                 # laranja do 46 (fio e nos)
$LAST=46
$CAPN='A tese'
$HOSE='#18202A'                    # borracha escura (um pouco acima do fundo para aparecer)
$HOSEL='#5E6E82'                   # linha clara de volume
$HY=480                            # altura do centro da mangueira (px)
$HW=120                            # espessura do corpo da mangueira
$HX1=250; $HX2=1670                # extremos do traco (a ponta redonda vai +60 px, sob as imagens das pontas)
$RN=140; $CX=960; $CY=580          # nucleo do 46

# ponta da mangueira: terminal de assets/pecas, escalado para o corpo ter ~120 px de altura; $flip espelha (ponta direita)
$SC=0.65; $PAD=45; $CROPH=340; $AXIS=170; $PW=443
function Add-Ponta($s,[string]$name,[double]$xvis,[bool]$flip){
  # xvis = borda externa visivel da ponta (a rosca fica nessa borda)
  $w=$PW*$SC; $h=$CROPH*$SC
  $x= if($flip){ $xvis-($PW-$PAD)*$SC }else{ $xvis-$PAD*$SC }
  $p=$s.Shapes.AddPicture((Join-Path $pecas 'pc_terminal_on.png'),0,-1,[single]($x/2),[single](($HY-$AXIS*$SC)/2),[single]($w/2),[single]($h/2)); $p.Name=$name
  if($flip){ $p.Flip(0) }
  $p }

# nos do 46 (!!nd1..5, circulos de 36 px) e onde ficam no 47 (alinhados no fio, sob o corpo) e no 48 (sob o anel, um em cada segmento)
$NDX47=@{1=560;2=1160;3=760;4=1360;5=960}
$RR=210; $RCX=960; $RCY=470        # carretel final (slide 48)
$NDANG=@{1=-67.5;2=-22.5;3=22.5;4=67.5;5=112.5}

$null=Open-GmsDeckForAppend $pptx
try {
  if($script:pres.Slides.Count -lt $LAST){ throw "o deck tem menos de $LAST slides: rode cap1 a cap7." }
  while($script:pres.Slides.Count -gt $LAST){ $script:pres.Slides.Item($script:pres.Slides.Count).Delete() }   # idempotente
  $script:slideN=$LAST

  # ---- 47 (27): a mangueira atravessa a tela; o fio engrossa; a tese entra no clique ----
  $s=New-GmsSlide
  for($n=1;$n -le 5;$n++){ $null=Add-Box $s "!!nd$n" 5 ($NDX47[$n]-18) ($HY-18) 36 36 $ORG $null 1 0.5 }   # sob o corpo
  $null=Add-FioLine $s '!!fio1' $HX1 $HY $HX2 $HY $HOSE $HW
  $null=Add-FioLine $s '!!fio2' $HX1 ($HY-26) $HX2 ($HY-26) $HOSEL 10
  $null=Add-Ponta $s 'mgEsq' 96 $false
  $null=Add-Ponta $s 'mgDir' 1824 $true
  Add-Moldura $s $CAPN $VRD '{{Não criamos}} o dado.' '27 / 28' 'seção 5'
  $teseT='Zeramos o custo de acessá-lo.'
  $tese=Add-Txt $s 'tese' $teseT 960 (670+120*$script:ASC) 120 @{font=$script:F_COND;bold=$true;color=$script:TX;align='m'}
  $i0=$teseT.IndexOf('acessá-lo')+1
  $tese.TextFrame.TextRange.Characters($i0,9).Font.Color.RGB=(Get-Rgb $VRD)
  $null=Add-ReelCap $s 1800 985 62 8 0.5; Set-Notes $s $rot['27']
  Add-ClickFade $s @($tese)

  # ---- 48 (28): o arco fecha, o carretel vai ao centro e assina GMS; a mangueira se enrola no fio ----
  $s=New-GmsSlide
  for($n=1;$n -le 5;$n++){
    $a=$NDANG[$n]*[Math]::PI/180
    $null=Add-Box $s "!!nd$n" 5 ($RCX+$RR*[Math]::Cos($a)-18) ($RCY+$RR*[Math]::Sin($a)-18) 36 36 $ORG $null 1 0.5 }
  $a=-67.5*[Math]::PI/180
  $px=$RCX+$RR*[Math]::Cos($a); $py=$RCY+$RR*[Math]::Sin($a)
  $null=Add-FioLine $s '!!fio1' $px $py ($px+2) ($py+0.5) $ORG 6      # toco de 2 px escondido sob o anel (meio de um segmento)
  $null=Add-ReelCap $s $RCX $RCY $RR 8 1.0
  $null=Add-Txt $s 'gms' 'GMS' $RCX ($RCY-70+130*$script:ASC) 130 @{font='Bahnschrift';bold=$true;color=$script:TX;align='m'}
  $null=Add-Txt $s 'obrigado' 'Obrigado.' $RCX (760+72*$script:ASC) 72 @{font=$script:F_SEMI;color='#B7C1CE';align='m'}
  Set-Notes $s $rot['28']

  foreach($sl in $script:pres.Slides){ $sl.SlideShowTransition.AdvanceOnClick=-1; $sl.SlideShowTransition.AdvanceOnTime=0 }
  Save-GmsDeck $pptx 1.2
  "salvo: $pptx"

  $null=Open-GmsDeck $pptx
  $idx=47..48
  Export-GmsSlides $prev 1920 1080 $idx
  "PNGs (slides 47 e 48, numeracao do deck): $prev"
  $nviol=Test-GmsLayout -Slides $idx -ExceptAll @('^(mgEsq|mgDir)$')
  "violacoes de layout: $nviol"
  "pdf: $(Export-GmsPdf (Join-Path $prev 'cap8.pdf'))"
  if(-not $SemVideo){
    # video do slide 46 (ultimo do cap7) ao 48: copia temporaria sem os slides 1 a 45
    $tmp=Join-Path $env:TEMP 'gms_cap8_video.pptx'
    if(Test-Path $tmp){ Remove-Item $tmp -Force }
    $script:pres.SaveCopyAs($tmp)
    $orig=$script:pres
    $v=$script:app.Presentations.Open($tmp,0,0,0)
    for($i=1;$i -le 45;$i++){ $v.Slides.Item(1).Delete() }
    foreach($sl in $v.Slides){ $sl.SlideShowTransition.Hidden=0 }
    try{ $v.Slides.Item(1).SlideShowTransition.EntryEffect=0 }catch{}
    $script:pres=$v
    $ok=Export-GmsVideo (Join-Path $prev 'cap8.mp4') 3 720 1200
    "video: $ok"
    $v.Saved=-1; $v.Close(); $script:pres=$orig
    Remove-Item $tmp -Force -ErrorAction SilentlyContinue
  }
} finally { Close-GmsDeck }
