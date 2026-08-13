import re

def detect_speaker_name(transcript_text):
    patterns = [
        r"my name is ([A-Z][a-z]+ [A-Z][a-z]+)",
        r"I'm ([A-Z][a-z]+ [A-Z][a-z]+)",
        r"I am ([A-Z][a-z]+ [A-Z][a-z]+)",
    ]
    sample = transcript_text[:500]
    for pattern in patterns:
        match = re.search(pattern, sample)
        if match:
            return match.group(1), "high"
    return None, "low"