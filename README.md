# vidstab-eazy
Video-stabilizer para quando todos os arquivos estão tremidos

# 🎥 Video Stabilization Script (PowerShell)

Este script usa **FFmpeg** para estabilizar vídeos automaticamente em um diretório. Ele:
- Detecta os movimentos no vídeo.
- Aplica estabilização usando o filtro `vidstab`.
- Salva os vídeos estabilizados em uma pasta separada.

## 📥 Instalação

1. **Baixe e instale o FFmpeg** (se ainda não tiver).  
   - [Baixar FFmpeg](https://ffmpeg.org/download.html)
   - Certifique-se de que `ffmpeg.exe` está no PATH do sistema.

2. **Clone este repositório:**
   ```powershell
   git clone https://github.com/seu-usuario/stabilize-videos.git
   cd stabilize-videos
