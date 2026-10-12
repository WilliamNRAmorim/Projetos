param([Parameter(Mandatory=$true)][string]$Docx)

$ErrorActionPreference = 'Stop'
$docxPath = (Resolve-Path -LiteralPath $Docx).Path
$pdfPath = [System.IO.Path]::ChangeExtension($docxPath, '.pdf')
$word = $null
$doc = $null
try {
    $word = New-Object -ComObject Word.Application
    $word.Visible = $false
    $word.DisplayAlerts = 0
    $doc = $word.Documents.Open($docxPath, $false, $true)
    $doc.ExportAsFixedFormat($pdfPath, 17)
    $pages = $doc.ComputeStatistics(2)
    Write-Output "PDF: $pdfPath"
    Write-Output "Paginas: $pages"
}
finally {
    if ($doc -ne $null) { $doc.Close($false) | Out-Null }
    if ($word -ne $null) { $word.Quit() | Out-Null }
}
