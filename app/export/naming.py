import os

def get_output_path(original_path, edited_folder):
    base = os.path.splitext(os.path.basename(original_path))[0]
    candidate = os.path.join(edited_folder, f"{base} (Edited).mp4")
    version = 2
    while os.path.exists(candidate):
        candidate = os.path.join(edited_folder, f"{base} (Edited v{version}).mp4")
        version += 1
    return candidate