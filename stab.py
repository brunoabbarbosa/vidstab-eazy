import os
import subprocess
from pathlib import Path

# Mapeamento de codecs para encoders FFmpeg
CODEC_ENCODER_MAP = {
    "h264": "libx264",
    "hevc": "libx265",
    "vp8": "libvpx",
    "vp9": "libvpx-vp9",
    "mpeg4": "mpeg4",
    "mpeg2video": "mpeg2video",
    "av1": "libaom-av1"
}

def get_video_codec(filepath):
    cmd = [
        "ffprobe", "-v", "error",
        "-select_streams", "v:0",
        "-show_entries", "stream=codec_name",
        "-of", "default=noprint_wrappers=1:nokey=1",
        filepath
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    codec = result.stdout.strip()
    return CODEC_ENCODER_MAP.get(codec, "libx264")  # fallback se não souber o codec

def stabilize_video(input_path, output_path):
    video_dir = os.path.dirname(input_path)
    transforms_file = os.path.join(video_dir, "transforms.trf")

    # Etapa 1: detectar movimento
    print(f"First pass - Detecting motion for {os.path.basename(input_path)}...")
    detect_cmd = [
        "ffmpeg", "-i", input_path,
        "-vf", f"vidstabdetect=shakiness=5:show=1:result={transforms_file}",
        "-f", "null", "-"
    ]
    subprocess.run(detect_cmd, check=True, capture_output=True)

    # Descobrir o codec original e escolher o encoder apropriado
    encoder = get_video_codec(input_path)
    print(f"Using encoder: {encoder}")

    # Etapa 2: aplicar estabilização
    print(f"Second pass - Applying stabilization for {os.path.basename(input_path)}...")
    transform_cmd = [
        "ffmpeg", "-i", input_path,
        "-vf", f"vidstabtransform=smoothing=20:input={transforms_file}",
        "-c:v", encoder,
        "-preset", "medium",  # opcional: define velocidade/qualidade do encoder
        "-crf", "15",         # opcional: qualidade do vídeo (para x264/x265)
        "-c:a", "copy",
        "-y", output_path
    ]
    subprocess.run(transform_cmd, check=True)

    if os.path.exists(transforms_file):
        os.remove(transforms_file)

def main():
    video_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(video_dir, "stabilized")
    os.makedirs(output_dir, exist_ok=True)

    video_extensions = ('.mov', '.mp4', '.avi', '.mkv', '.wmv', '.flv')
    video_files = [f for f in os.listdir(video_dir) if f.lower().endswith(video_extensions)]

    if not video_files:
        print(f"No video files found in {video_dir}")
        print("Supported formats:", ", ".join(video_extensions))
        return

    print(f"Found {len(video_files)} video files to process.")

    for video_file in video_files:
        input_path = os.path.join(video_dir, video_file)
        output_path = os.path.join(output_dir, f"stabilized_{video_file}")

        print(f"\nProcessing {video_file}...")
        try:
            stabilize_video(input_path, output_path)
            print(f"Successfully stabilized {video_file}")
        except subprocess.CalledProcessError as e:
            print(f"Error processing {video_file}: {e.stderr}")
        except Exception as e:
            print(f"Unexpected error processing {video_file}: {str(e)}")

    print("\nAll videos have been processed.")

if __name__ == "__main__":
    main()
