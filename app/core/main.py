from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.db import get_all_videos, get_video_by_id, update_status
from app.workflow.orchestrator import process_video

app = FastAPI(title="SME Local API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/videos")
def list_videos():
    rows = get_all_videos()
    return [
        {
            "id": r[0],
            "filepath": r[1],
            "programme": r[2],
            "week": r[3],
            "module": r[4],
            "lesson_number": r[5],
            "lesson_title": r[6],
            "status": r[7],
            "date_added": r[8]
        }
        for r in rows
    ]

@app.post("/process/{video_id}")
def trigger_process(video_id: int):
    video = get_video_by_id(video_id)
    if not video:
        return {"error": "Video not found"}
    update_status(video_id, "processing")
    try:
        output = process_video(video[1])
        update_status(video_id, "completed")
        return {"status": "completed", "output": output}
    except Exception as e:
        update_status(video_id, "failed")
        return {"status": "failed", "error": str(e)}