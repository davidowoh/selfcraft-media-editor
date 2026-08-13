import os
from app.ai.transcribe import transcribe, write_srt
from app.ai.silence import detect_silence
from app.ai.speaker import detect_speaker_name
from app.media.render import burn_captions, export_final
from app.export.naming import get_output_path
from app.logging.logger import get_logger
from database.db import update_progress

log = get_logger("orchestrator")

EDITED_FOLDER = "/home/davidowoh/SelfCraft Media/Edited Videos"
TEMP_FOLDER = "/home/davidowoh/SelfCraft Media/Temp"

def get_template(video_path):
    if "Teaching Reels" in video_path:
        return "reel"
    elif "Testimonials" in video_path:
        return "testimonial"
    else:
        return "lesson"

def process_video(video_path, video_id=None):
    os.makedirs(EDITED_FOLDER, exist_ok=True)
    os.makedirs(TEMP_FOLDER, exist_ok=True)
    log.info(f"Starting: {video_path}")

    def report(msg):
        print(msg)
        if video_id:
            update_progress(video_id, msg)

    base_name = os.path.splitext(os.path.basename(video_path))[0]
    template = get_template(video_path)

    report("Transcribing audio with Whisper AI…")
    result = transcribe(video_path)
    srt_path = os.path.join(TEMP_FOLDER, f"{base_name}.srt")
    write_srt(result, srt_path)

    if template == "testimonial":
        report("Detecting speaker name from transcript…")
        speaker_name, confidence = detect_speaker_name(result['text'])
        if speaker_name:
            report(f"Speaker identified: {speaker_name}")
        else:
            report("Speaker not detected — continuing without name overlay")

    report("Burning captions onto video…")
    captioned_path = os.path.join(TEMP_FOLDER, f"{base_name}_captioned.mp4")
    burn_captions(video_path, srt_path, captioned_path)

    report("Exporting final video in correct format…")
    target = 'landscape' if template == 'lesson' else 'reel'
    output_path = get_output_path(video_path, EDITED_FOLDER)
    export_final(captioned_path, output_path, target=target)

    report("Cleaning up temporary files…")
    os.remove(captioned_path)
    os.remove(srt_path)

    log.info(f"Completed: {output_path}")
    return output_path