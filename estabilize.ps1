# Definir diretório dos vídeos - Altera apra o seu 
$videoDir = "D:\videos\ESTABILIZ-aqui"
$outputDir = Join-Path -Path $videoDir -ChildPath "stabilized"

# Criar diretório de saída se não existir
if (!(Test-Path -Path $outputDir)) {
    New-Item -ItemType Directory -Path $outputDir | Out-Null
}

# Extensões de vídeo suportadas
$videoExtensions = @("*.mov", "*.mp4", "*.avi", "*.mkv", "*.wmv", "*.flv")

# Obter lista de arquivos de vídeo
$videoFiles = Get-ChildItem -Path $videoDir -Include $videoExtensions -File

if ($videoFiles.Count -eq 0) {
    Write-Host "Nenhum vídeo encontrado em $videoDir"
    Write-Host "Formatos suportados: $($videoExtensions -join ', ')"
    exit
}

Write-Host "Encontrados $($videoFiles.Count) arquivos para processar."

# Processar cada vídeo
foreach ($videoFile in $videoFiles) {
    $inputPath = $videoFile.FullName
    $outputPath = Join-Path -Path $outputDir -ChildPath "stabilized_$($videoFile.Name)"
    $transformsFile = Join-Path -Path $videoDir -ChildPath "transforms.trf"

    Write-Host "`nProcessando: $($videoFile.Name)..."

    # Primeira etapa: Detectar movimento Shakiness acima de 25 não fica bom, regravar
    Write-Host "Primeira etapa - Detectando movimento..."
    $detectCmd = "ffmpeg -i `"$inputPath`" -vf `""vidstabdetect=shakiness=5:show=1`" -f null -"
    Start-Process -NoNewWindow -Wait -FilePath "cmd.exe" -ArgumentList "/c $detectCmd"

    # Segunda etapa: Aplicar estabilização Smoothing acima de 20 adiciona artefatos, tentar manter abaixo disso 
    Write-Host "Segunda etapa - Aplicando estabilização..."
    $transformCmd = "ffmpeg -i `"$inputPath`" -vf `""vidstabtransform=smoothing=20:input='$transformsFile'`" -y `"$outputPath`""
    Start-Process -NoNewWindow -Wait -FilePath "cmd.exe" -ArgumentList "/c $transformCmd"

    # Remover o arquivo de transformação após o processamento
    if (Test-Path -Path $transformsFile) {
        Remove-Item -Path $transformsFile -Force
    }

    Write-Host "Finalizado: $($videoFile.Name)"
}

Write-Host "`nTodos os vídeos foram processados!"
