import whisper
from app.core.config import get_whisper_model

_model = None

def get_model():
    global _model
    if _model is None:
        model_name = get_whisper_model()
        print(f"Loading Whisper model ({model_name})...")
        _model = whisper.load_model(model_name)
        print("Model loaded.")
    return _model

def transcribe(video_path):
    model = get_model()
    print(f"Transcribing: {video_path}")
    result = model.transcribe(video_path, fp16=False)
    print("Transcription complete.")
    return result

def format_timestamp(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds % 60
    return f"{h:02}:{m:02}:{s:06.3f}".replace('.', ',')

def write_srt(result, output_path):
    with open(output_path, 'w', encoding='utf-8') as f:
        for i, seg in enumerate(result['segments'], start=1):
            f.write(f"{i}\n")
            f.write(f"{format_timestamp(seg['start'])} --> {format_timestamp(seg['end'])}\n")
            f.write(f"{seg['text'].strip()}\n\n")
    print(f"SRT written: {output_path}")