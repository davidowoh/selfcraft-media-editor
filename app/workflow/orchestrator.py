import os
from app.ai.transcribe import transcribe, write_srt
from app.media.render import burn_captions, export_final
from app.export.naming import get_output_path
from app.logging.logger import get_logger

log = get_logger("orchestrator")

EDITED_FOLDER = "/home/davidowoh/SelfCraft Media/Edited Videos"
TEMP_FOLDER = "/home/davidowoh/SelfCraft Media/Temp"

def process_video(video_path):
    os.makedirs(EDITED_FOLDER, exist_ok=True)
    os.makedirs(TEMP_FOLDER, exist_ok=True)
    log.info(f"Starting: {video_path}")
    print(f"\n--- Processing: {video_path} ---")

    base_name = os.path.splitext(os.path.basename(video_path))[0]

    # Step 1: Transcribe — SRT goes in Temp, not beside the raw file
    print("Step 1: Transcribing audio...")
    result = transcribe(video_path)
    srt_path = os.path.join(TEMP_FOLDER, f"{base_name}.srt")
    write_srt(result, srt_path)

    # Step 2: Burn captions — captioned file goes in Temp
    print("Step 2: Burning captions...")
    captioned_path = os.path.join(TEMP_FOLDER, f"{base_name}_captioned.mp4")
    burn_captions(video_path, srt_path, captioned_path)

    # Step 3: Export final version into Edited Videos
    print("Step 3: Exporting final video...")
    output_path = get_output_path(video_path, EDITED_FOLDER)
    export_final(captioned_path, output_path, target='landscape')

    # Step 4: Clean up temp files
    os.remove(captioned_path)
    os.remove(srt_path)
    print("Step 4: Cleaned up temporary files.")

    log.info(f"Completed: {output_path}")
    print(f"\n✓ Done: {output_path}")
    return output_path