import os
import glob

def get_output_path(original_path, edited_folder):
    base = os.path.splitext(os.path.basename(original_path))[0]
    candidate = os.path.join(edited_folder, f"{base} (Edited).mp4")
    version = 2
    while os.path.exists(candidate):
        candidate = os.path.join(edited_folder, f"{base} (Edited v{version}).mp4")
        version += 1
    return candidate

def get_next_version_label(original_path, edited_folder):
    """Returns a human-readable label for what the next run will produce."""
    base = os.path.splitext(os.path.basename(original_path))[0]
    pattern = os.path.join(edited_folder, f"{base} (Edited*).mp4")
    existing = glob.glob(pattern)
    if not existing:
        return "will create (Edited).mp4"
    return f"will create (Edited v{len(existing) + 1}).mp4"