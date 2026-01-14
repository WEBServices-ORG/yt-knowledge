from fastapi import FastAPI, BackgroundTasks
import subprocess
import os
from typing import Optional

app = FastAPI(title="yt-knowledge API", description="REST API for yt-knowledge tool")


@app.post("/download_subs")
async def download_subs(channel_url: str, background_tasks: BackgroundTasks):
    # Run download in background
    background_tasks.add_task(run_command, ["bash", "scripts/download_subs.sh"])
    return {"message": "Download started"}


@app.post("/extract_text")
async def extract_text():
    result = run_command(["python3", "scripts/extract_text.py"])
    return {"output": result}


@app.post("/translate_text")
async def translate_text():
    result = run_command(["python3", "scripts/translate_text.py"])
    return {"output": result}


@app.post("/summarize")
async def summarize_text():
    result = run_command(["python3", "scripts/summarize.py"])
    return {"output": result}


@app.post("/export")
async def export_text(format: str, input_file: Optional[str] = "data/english_subs.txt"):
    result = run_command(["python3", "scripts/export.py", format, input_file])
    return {"output": result}


@app.get("/status")
async def get_status():
    # Get recent logs or status
    try:
        with open("logs/latest.log", "r") as f:
            logs = f.read()[-1000:]  # Last 1000 chars
    except:
        logs = "No logs available"
    return {"status": "Running", "logs": logs}


def run_command(cmd):
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=os.getcwd())
    return result.stdout + result.stderr
