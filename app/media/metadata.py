import re
import os

def extract_metadata(filepath):
    parts = filepath.replace('\\', '/').split('/')
    filename = os.path.splitext(parts[-1])[0]

    skip_words = {'Recorded Classes', 'Teaching Reels', 'Testimonials',
                  'Raw Videos', 'SelfCraft Media', 'home', 'davidowoh'}

    programme = next((p for p in parts
                      if p not in skip_words
                      and not p.startswith('Week')
                      and not p.startswith('Module')
                      and not p.startswith('Lesson')
                      and p != ''
                      and not p.startswith('/')), None)

    week = next((p for p in parts if p.startswith('Week')), None)
    module = next((p for p in parts if p.startswith('Module')), None)

    match = re.match(r'Lesson\s*(\d+)\s*-\s*(.+)', filename)
    lesson_number = match.group(1) if match else None
    lesson_title = match.group(2) if match else filename

    return {
        'programme': programme,
        'week': week,
        'module': module,
        'lesson_number': lesson_number,
        'lesson_title': lesson_title
    }