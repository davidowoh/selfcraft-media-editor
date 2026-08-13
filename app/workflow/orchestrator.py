import os
from app.ai.transcribe import transcribe, write_srt
from app.ai.silence import detect_silence
from app.ai.speaker import detect_speaker_name
from app.media.render import burn_captions, export_final
from app.export.naming import get_output_path
from app.logging.logger import get_logger

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

def process_video(video_path):
    os.makedirs(EDITED_FOLDER, exist_ok=True)
    os.makedirs(TEMP_FOLDER, exist_ok=True)
    log.info(f"Starting: {video_path}")
    print(f"\n--- Processing: {video_path} ---")

    base_name = os.path.splitext(os.path.basename(video_path))[0]
    template = get_template(video_path)
    print(f"Template detected: {template}")

    # Step 1: Transcribe
    print("Step 1: Transcribing audio...")
    result = transcribe(video_path)
    srt_path = os.path.join(TEMP_FOLDER, f"{base_name}.srt")
    write_srt(result, srt_path)

    # Step 2: Speaker detection for testimonials
    speaker_name = None
    if template == "testimonial":
        print("Step 2: Detecting speaker name...")
        transcript_text = result['text']
        speaker_name, confidence = detect_speaker_name(transcript_text)
        if speaker_name:
            print(f"Speaker detected: {speaker_name} (confidence: {confidence})")
        else:
            print("Speaker not detected — will need manual review.")

    # Step 3: Burn captions
    print("Step 3: Burning captions...")
    captioned_path = os.path.join(TEMP_FOLDER, f"{base_name}_captioned.mp4")
    burn_captions(video_path, srt_path, captioned_path)

    # Step 4: Export in correct orientation
    print("Step 4: Exporting final video...")
    target = 'landscape' if template == 'lesson' else 'reel'
    output_path = get_output_path(video_path, EDITED_FOLDER)
    export_final(captioned_path, output_path, target=target)

    # Step 5: Clean up
    os.remove(captioned_path)
    os.remove(srt_path)
    print("Step 5: Cleaned up temporary files.")

    log.info(f"Completed: {output_path}")
    print(f"\n✓ Done: {output_path}")
    return output_path