import json
import os

CONFIG_PATH = os.path.join(
    os.path.dirname(__file__), '..', '..', 'config', 'settings.json'
)

def load_config():
    with open(CONFIG_PATH, 'r') as f:
        return json.load(f)

def get_folders():
    return load_config()['folders']

def get_caption_style():
    return load_config()['captions']

def get_file_manager():
    return load_config().get('file_manager', 'nautilus')

def get_whisper_model():
    return load_config().get('whisper_model', 'base')

#def get_max_parallel_jobs():
#    return load_config().get('max_parallel_jobs', 1)

def get_video_player():
    return load_config().get('video_player', 'browser')