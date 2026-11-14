# cap5.ps1 - Capitulo 5 (OS RESULTADOS, quadros 19 a 23 = 6 slides: 19, 20, 21a, 21b, 22, 23 = slides 36 a 41).
# NAO regera os capitulos anteriores: abre GMS_Defesa.pptx (35 slides), apaga o que houver alem do 35 (idempotente),
# acrescenta os 6 slides, salva (Save-GmsDeck reaplica o Morph) e exporta previa/cap5/.
# Uso (depois de cap1 a cap4):  powershell -NoProfile -ExecutionPolicy Bypass -File cap5.ps1 [-SemVideo]
# O quadro 21 tem dois passos (21a: o 8,3x sozinho; 21b: a barra de 74%). A barra de 74% passa ao quadro 22 pelo Morph (!!barra1),
# e objeto de Morph nao pode ter animacao de clique: por isso o "depois, uma barra" virou um passo (um clique = uma passagem).
# Slides 33 a 35 (plano B do cap4) continuam ocultos. A passagem de entrada tem duas origens: 32 (sem os ocultos) e 35 (oculto).
param([switch]$SemVideo)
$ErrorActionPreference='Stop'
. "$PSScriptRoot\gms_lib.ps1"
$root=(Resolve-Path "$PSScriptRoot\..").Path
$pptx=Join-Path $root 'GMS_Defesa.pptx'
$prev=Join-Path $root 'previa\cap5'
if(-not (Test-Path $pptx)){ throw 'GMS_Defesa.pptx nao existe: rode cap1 a cap4 antes.' }
$rot=Get-Roteiro (Join-Path $root 'roteiro.md')

$AMB=$script:CH[4]                  # ambar #F59E0B: so o que o sistema mediu
$AMBL='#FDE68A'
$MUT=Mix-Hex $script:TX 0.62        # numeros que sao estimativa da equipe: cinza claro, sem o ambar
$PAR=Mix-Hex $AMB 0.55              # funcao parcial (meio acesa)
$OFF=Mix-Hex $script:T2 0.6         # funcao fora do escopo (apagada)
$LAST=35                            # ultimo slide do capitulo 4
$TOTAL=6                            # slides do capitulo; o arco ambar cresce de 1/6 a 6/6, monotonico
$script:k=0
function Frac { $script:k++; [double]$script:k/$TOTAL }

# ---------- helpers ----------
function Txt2($s,[string]$name,[string]$text,[double]$x,[double]$top,[double]$size,[hashtable]$o){   # posiciona pelo TOPO da caixa (px)
  Add-Txt $s $name $text $x ($top+$size*$script:ASC) $size $o }
function Lines2($t){ $r=$t.TextFrame.TextRange.ParagraphFormat; $r.LineRuleWithin=-1; $r.SpaceWithin=0.9 }
function Center-Y($t,[double]$cy,[double]$h){ $t.Top=($cy+($h-$t.Height*2)/2)/2 }   # centraliza na vertical dentro de [cy, cy+h] (px)

# bloco de barra (rotulo grande + descricao + trilho + preenchimento). n=1 leva !!, n=2 nasce sem !!
function Add-BarraBloco($s,[int]$n,[double]$T,[string]$pct,[string]$desc,[double]$frac,[bool]$cinza2){
  $p= if($n -eq 1){'!!'}else{''}
  $null=Add-Box $s "${p}trilho$n" 1 96 ($T+180) 1728 44 $script:SF $script:LN 3
  $null=Add-Box $s "${p}barra$n" 1 96 ($T+180) (1728*$frac) 44 $AMB $null
  $null=Txt2 $s "${p}pct$n" $pct 96 $T 120 @{font=$script:F_COND;bold=$true;color=$AMB}
  $d=Txt2 $s "${p}desc$n" $desc 470 ($T+12) 56 @{color=$script:TX}
  Lines2 $d
  if($cinza2){ $d.TextFrame.TextRange.Paragraphs(2).Font.Color.RGB=(Get-Rgb $script:T2) }
  $d.Top=($T+(144-$d.Height*2)/2)/2 }

# anel de 11 arcos (MESA-11): 24 graus de arco em fatias de 32,7; nenhum arco cruza 0/360 (angulo monotonico no Morph).
# final=false: tocos de 1 grau na cor do fundo (nao aparecem); final=true: o anel pronto.
$RCX=450; $RCY=580; $RR=270; $RW=30
$ST=@{8='L';9='L';10='L';0='L';1='L';2='L';3='P';4='M';5='M';6='O';7='O'}   # seis acesas, uma em expansao, duas parciais, duas fora
function Add-Anel11($s,[bool]$final){
  for($j=0;$j -lt 11;$j++){
    $a0=[Math]::Round(32.7273*$j+4.3636,2)
    if($final){ $a1=$a0+24; $col= switch($ST[$j]){ 'L'{$AMB} 'P'{$AMB} 'M'{$PAR} default{$OFF} } } else { $a1=$a0+1; $col=$script:BG }
    $null=Add-FioArc $s "!!arcoM$($j+1)" $RCX $RCY $RR $RR $a0 $a1 $col $RW } }

$null=Open-GmsDeckForAppend $pptx
try {
  if($script:pres.Slides.Count -lt $LAST){ throw "o deck tem menos de $LAST slides: rode cap1 a cap4." }
  while($script:pres.Slides.Count -gt $LAST){ $script:pres.Slides.Item($script:pres.Slides.Count).Delete() }   # idempotente
  $script:slideN=$LAST

  # ---- 36 (19): antes x depois. A ficha da abertura volta a esquerda; o tablet (!!no1 do 32 e do 35) vai a direita ----
  $s=New-GmsSlide
  $null=Add-Ficha $s 96 430 240
  $rowY=268,488,708; $RH=184
  $R=@(@{lab='Tempo';        ant="1 a 2 dias";                dep="no registro,`rna TV em até 2 min"},
       @{lab='Visibilidade'; ant="nenhuma etapa`rà vista";    dep="todas as etapas"},
       @{lab='Conexão';      ant="uma manhã`rpor OP";         dep="conferência diária`rcom o SAP"})
  for($i=0;$i -lt 3;$i++){ $null=Add-Box $s "!!lin$($i+1)" 1 384 $rowY[$i] 1152 $RH $script:SF $script:LN 3 }
  $null=Add-Box $s '!!no1' 5 1584 505 240 150 $script:SF $AMB 6 0.05
  $null=Add-Box $s 'tela_tab' 5 1602 523 204 114 (Mix-Hex $AMB 0.14) $null 1 0.04   # arredondado: um retangulo sem nome seria casado pelo Morph com a faixa do 37
  $tw=172,130,150; for($i=0;$i -lt 3;$i++){ $null=Add-Box $s "tela_l$($i+1)" 5 1620 (541+36*$i) $tw[$i] 18 (Mix-Hex $AMB 0.7) $null 1 0.5 }   # tres linhas: a fila por etapa na tela
  for($i=0;$i -lt 3;$i++){
    $n=$i+1; $cy=$rowY[$i]
    $t=Txt2 $s "!!lab$n" $R[$i].lab 416 0 56 @{font=$script:F_COND;bold=$true;color=$AMB}; Center-Y $t $cy $RH
    $t=Txt2 $s "ant$n" $R[$i].ant 710 0 56 @{font=$script:F_COND;color=$script:T2}; if($R[$i].ant -match "`r"){ Lines2 $t }; Center-Y $t $cy $RH
    $null=Add-Box $s "seta$n" 33 1010 ($cy+($RH-40)/2) 56 40 $AMB $null
    $t=Txt2 $s "dep$n" $R[$i].dep 1090 0 56 @{font=$script:F_COND;color=$script:TX}; if($R[$i].dep -match "`r"){ Lines2 $t }; Center-Y $t $cy $RH }
  Add-Moldura $s 'Os resultados' $AMB 'Os três planos, agora com {{evidência}}.' '19 / 28' 'seções 4.5 e 4.6'
  $null=Add-ReelCap $s 1800 985 62 5 (Frac); Set-Notes $s $rot['19']

  # ---- 37 (20): as tres linhas viram os tres numeros do dossie (estimativa da equipe, sem cronometragem) ----
  $s=New-GmsSlide
  $cxs=96,680,1264; $nums='36×','87,5%','97%'
  $labs='Resposta a reclamação','Escopo de contenção','Horas de consolidação'; $legs='mais rápida','menor','a menos'
  for($i=0;$i -lt 3;$i++){ $null=Add-Box $s "!!lin$($i+1)" 1 $cxs[$i] 288 560 450 $script:SF $script:LN 3 }
  for($i=0;$i -lt 3;$i++){
    $n=$i+1
    $null=Txt2 $s "!!num$n" $nums[$i] ($cxs[$i]+32) 318 190 @{font=$script:F_COND;bold=$true;color=$MUT}
    $null=Txt2 $s "!!lab$n" $labs[$i] ($cxs[$i]+32) 570 56 @{font=$script:F_COND;bold=$true;color=$script:TX}
    $null=Txt2 $s "leg$n" $legs[$i] ($cxs[$i]+32) 646 56 @{font=$script:F_COND;color=$script:T2} }
  $null=Add-Box $s 'faixa_est' 1 96 780 1728 88 $script:BG $script:SE 3   # preenchimento na cor do fundo: sem fill, o Morph pinta o estilo (fillRef) durante o fade
  $t=Txt2 $s 'txt_est' 'estimativas da equipe, sem cronometragem' 960 0 56 @{font=$script:F_COND;color=$script:SE;align='m'}; Center-Y $t 780 88
  Add-Moldura $s 'Os resultados' $AMB 'O que o dossiê do Kaizen {{estima}}.' '20 / 28' 'seção 4.5 e Quadro 6'
  $null=Add-ReelCap $s 1800 985 62 5 (Frac); Set-Notes $s $rot['20']

  # ---- 38 (21a): o 36x vira o 8,3x (numero-heroi, sem frase-guia); os outros dois saem ----
  $s=New-GmsSlide
  $h=Txt2 $s '!!num1' '8,3×' 960 247 400 @{font=$script:F_COND;bold=$true;color=$AMB;align='m'}
  $hb=($h.Top+$h.Height)*2
  $null=Txt2 $s '!!sub83' 'O volume da célula era contado 8,3 vezes.' 960 ($hb+40) 56 @{color=$script:TX;align='m'}
  Add-Moldura $s 'Os resultados' $AMB '' '21 / 28' 'seções 4.3 e 4.6'
  $null=Add-ReelCap $s 1800 985 62 5 (Frac); Set-Notes $s $rot['21a']

  # ---- 39 (21b): o 8,3x encolhe para a base; entra a barra de 74% (vira a de 96,4% no 40) ----
  $s=New-GmsSlide
  $LQ=[string][char]0x201C; $RQ=[string][char]0x201D   # aspas curvas: o PowerShell as trata como aspas de string, entao vao por codigo
  Add-BarraBloco $s 1 272 '74%' ("da ${LQ}parada${RQ} da Montagem`rera tempo excedido") 0.74 $false
  $h=Txt2 $s '!!num1' '8,3×' 96 556 200 @{font=$script:F_COND;bold=$true;color=$AMB}
  $null=Txt2 $s '!!sub83' 'O volume da célula era contado 8,3 vezes.' (96+$h.Width*2+48) 636 56 @{color=$script:TX}
  Add-Moldura $s 'Os resultados' $AMB 'Isto o sistema {{mediu}}.' '21 / 28' 'seções 4.3 e 4.6'
  $null=Add-ReelCap $s 1800 985 62 5 (Frac); Set-Notes $s $rot['21b']

  # ---- 40 (22): a barra de 74% vira a de 96,4% e nasce a segunda; tocos do anel de 11 arcos por baixo ----
  $s=New-GmsSlide
  Add-Anel11 $s $false
  Add-BarraBloco $s 1 272 '96,4%' "das OPs do GMS também estão no SAP`ranálise retrospectiva de um mês" 0.964 $true
  Add-BarraBloco $s 2 556 'até 6%' "de diferença no tempo parado dos turnos fechados`rsensor de uma máquina, quinze dias" 0.06 $true
  $null=Txt2 $s 'nota9' 'hora a hora, cerca de 9 min de erro' 96 812 56 @{color=$script:T2}
  Add-Moldura $s 'Os resultados' $AMB 'Conferi contra fontes que {{não controlo}}.' '22 / 28' 'Resumo; seção 4.4 e Tabela 2'
  $null=Add-ReelCap $s 1800 985 62 5 (Frac); Set-Notes $s $rot['22']

  # ---- 41 (23): as barras somem e os arcos do anel crescem: MESA-11 (6 acesas, 1 pulsando, 2 meio acesas, 2 apagadas) ----
  $s=New-GmsSlide
  Add-Anel11 $s $true
  $c=Txt2 $s 'ring_n' '11' $RCX 466 140 @{font=$script:F_COND;bold=$true;color=$script:TX;align='m'}
  $null=Txt2 $s 'ring_lbl' 'funções' $RCX (($c.Top+$c.Height)*2+8) 56 @{color=$script:T2;align='m'}
  $LG=@(@('6','implementadas',$AMB),@('1','em expansão',$AMB),@('2','parciais',$PAR),@('2','fora do escopo',$OFF))
  for($i=0;$i -lt 4;$i++){
    $top=290+160*$i
    $null=Txt2 $s "leg_n$($i+1)" $LG[$i][0] 900 $top 100 @{font=$script:F_COND;bold=$true;color=$LG[$i][2]}
    $null=Txt2 $s "leg_t$($i+1)" $LG[$i][1] 1020 ($top+27) 56 @{color=$script:TX} }
  $am=(32.7273*3+4.3636+12)*[Math]::PI/180
  $anel=Add-Box $s 'pulso_anel' 9 ($RCX+$RR*[Math]::Cos($am)-32) ($RCY+$RR*[Math]::Sin($am)-32) 64 64 $script:BG $AMBL 4
  $anel.Fill.Transparency=1   # fill explicito e invisivel (mesmo motivo)
  try{
    $e=$s.TimeLine.MainSequence.AddEffect($anel,59,0,2)   # 59 = Grow/Shrink; com o anterior: roda sozinho
    $e.Timing.Duration=1.2; $e.Timing.RepeatCount=60
  }catch{ Write-Host "animacao de pulso nao aplicada: $($_.Exception.Message)" }
  Add-Moldura $s 'Os resultados' $AMB 'Nenhuma função mudou. {{Mudou a prova.}}' '23 / 28' 'seção 4.7, Quadro 7 (MESA INTERNATIONAL, 1997)'
  $null=Add-ReelCap $s 1800 985 62 5 (Frac); Set-Notes $s $rot['23']

  foreach($sl in $script:pres.Slides){ $sl.SlideShowTransition.AdvanceOnClick=-1; $sl.SlideShowTransition.AdvanceOnTime=0 }
  Save-GmsDeck $pptx 1.2
  # pulsos (32 e 41): repeatCount numerico vira 'indefinite'; senao o CreateVideo estende o slide a 72 s
  $z=[IO.Compression.ZipFile]::Open($pptx,'Update'); $utf8=New-Object Text.UTF8Encoding($false)
  foreach($en in @($z.Entries | Where-Object { $_.FullName -match '^ppt/slides/slide\d+\.xml$' })){
    $r=New-Object IO.StreamReader($en.Open(),$utf8); $x=$r.ReadToEnd(); $r.Close()
    if($x -match 'repeatCount="\d+"'){
      $n=$en.FullName; $x=[regex]::Replace($x,'repeatCount="\d+"','repeatCount="indefinite"'); $en.Delete()
      $ne=$z.CreateEntry($n); $w=New-Object IO.StreamWriter($ne.Open(),$utf8); $w.Write($x); $w.Close(); "pulso: repeatCount=indefinite em $n" } }
  $z.Dispose()
  "salvo: $pptx"

  $null=Open-GmsDeck $pptx
  $idx=36..41
  Export-GmsSlides $prev 1920 1080 $idx
  "PNGs (slides 36 a 41, numeracao do deck): $prev"
  $famL=@('^(!!lin\d|!!lab\d|ant\d|dep\d|seta\d)$','^(!!lin\d|!!lab\d|!!num\d|leg\d)$','^(faixa_est|txt_est)$','^(!!no1|tela_tab|tela_l\d)$','^(ring_n|ring_lbl)$','^(!!trilho\d|trilho\d|!!barra\d|barra\d)$')
  $nviol=Test-GmsLayout -Slides $idx -Families $famL
  "violacoes de layout: $nviol"
  "pdf: $(Export-GmsPdf (Join-Path $prev 'cap5.pdf'))"
  if(-not $SemVideo){
    # video do slide 35 (ultimo oculto do plano B) ao 41: copia temporaria sem os slides 1 a 34; o oculto aparece so no video
    $tmp=Join-Path $env:TEMP 'gms_cap5_video.pptx'
    if(Test-Path $tmp){ Remove-Item $tmp -Force }
    $script:pres.SaveCopyAs($tmp)
    $orig=$script:pres
    $v=$script:app.Presentations.Open($tmp,0,0,0)
    for($i=1;$i -le 34;$i++){ $v.Slides.Item(1).Delete() }
    foreach($sl in $v.Slides){ $sl.SlideShowTransition.Hidden=0 }
    try{ $v.Slides.Item(1).SlideShowTransition.EntryEffect=0 }catch{}
    $script:pres=$v
    $ok=Export-GmsVideo (Join-Path $prev 'cap5.mp4') 3 720 900
    "video: $ok"
    $v.Saved=-1; $v.Close(); $script:pres=$orig
    Remove-Item $tmp -Force -ErrorAction SilentlyContinue
    # entrada pelo slide 32 (o show pula os ocultos 33 a 35): copia sem os slides 1 a 31, sem os ocultos e so ate o 37
    $tmp=Join-Path $env:TEMP 'gms_cap5_entrada32.pptx'
    if(Test-Path $tmp){ Remove-Item $tmp -Force }
    $script:pres.SaveCopyAs($tmp)
    $v=$script:app.Presentations.Open($tmp,0,0,0)
    for($i=1;$i -le 31;$i++){ $v.Slides.Item(1).Delete() }
    for($i=1;$i -le 3;$i++){ $v.Slides.Item(2).Delete() }
    while($v.Slides.Count -gt 3){ $v.Slides.Item($v.Slides.Count).Delete() }
    try{ $v.Slides.Item(1).SlideShowTransition.EntryEffect=0 }catch{}
    $script:pres=$v
    $ok=Export-GmsVideo (Join-Path $prev 'cap5_entrada32.mp4') 3 720 600
    "video da entrada pelo 32: $ok"
    $v.Saved=-1; $v.Close(); $script:pres=$orig
    Remove-Item $tmp -Force -ErrorAction SilentlyContinue
  }
} finally { Close-GmsDeck }
