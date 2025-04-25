# vidstab-eazy
Video-stabilizer para quando todos os arquivos estão tremidos

# 🎥 Video Stabilization Script (Linux WSL2)



Este script usa **FFmpeg** para estabilizar vídeos automaticamente em um diretório. Ele:
- Detecta os movimentos no vídeo.
- Aplica estabilização usando o filtro `vidstab`.
- Salva os vídeos estabilizados em uma pasta separada.

## 📥 Instalação

1. **Clone este repositório**
git clone https://github.com/georgmartius/vid.stab.git
  
2. **Baixe e instale o FFmpeg** (se ainda não tiver).  
   - [Baixar FFmpeg](https://ffmpeg.org/download.html)
   - Certifique-se de que `ffmpeg.exe` está no PATH do sistema.
  
3. **instale o python**
  - 3.2 é o suficiente

5. **Copie o stab.py para sua pasta**
   - Copie e rode no WSL o arquivo stab.py
