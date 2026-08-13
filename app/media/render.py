import subprocess

def burn_captions(input_path, srt_path, output_path):
    subtitle_filter = (
        f"subtitles={srt_path}:force_style="
        "'FontName=Liberation Sans,FontSize=14,PrimaryColour=&H00FFFFFF,"
        "OutlineColour=&H00000000,Outline=2,Shadow=1,"
        "Alignment=2,MarginV=20'"
    )
    subprocess.run([
        'ffmpeg', '-y', '-i', input_path,
        '-vf', subtitle_filter,
        '-c:a', 'copy',
        output_path
    ], check=True)
    print(f"Captions burned: {output_path}")

def export_final(input_path, output_path, target='landscape'):
    scale = '1920:1080' if target == 'landscape' else '1080:1920'
    subprocess.run([
        'ffmpeg', '-y', '-i', input_path,
        '-vf', f'scale={scale}',
        '-c:v', 'libx264', '-preset', 'medium', '-crf', '23',
        '-c:a', 'aac', '-b:a', '192k',
        output_path
    ], check=True)
    print(f"Exported: {output_path}")