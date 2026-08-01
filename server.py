import json
from pathlib import Path
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

BASE_DIR = Path(__file__).parent.resolve()
STATE_FILE = BASE_DIR / "checklist_state.json"

app = FastAPI(title="AI Engineer Roadmap Checklist Server")

CURRICULUM_FILE = BASE_DIR / "curriculum_data.json"

@app.get("/api/checklist")
def get_checklist_state():
    if not STATE_FILE.exists():
        return {"completed": {}, "outcomes": {}, "completedAt": {}, "reasons": {}}
    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading state file: {str(e)}")

@app.post("/api/checklist")
async def save_checklist_state(request: Request):
    try:
        data = await request.json()
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error writing state file: {str(e)}")

@app.get("/api/curriculum")
def get_curriculum_data():
    if not CURRICULUM_FILE.exists():
        raise HTTPException(status_code=404, detail="curriculum_data.json not found")
    try:
        with open(CURRICULUM_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading curriculum file: {str(e)}")

@app.get("/")
def read_root():
    index_path = BASE_DIR / "index.html"
    if index_path.exists():
        return HTMLResponse(content=index_path.read_text(encoding="utf-8"))
    checklist_path = BASE_DIR / "checklist.html"
    if checklist_path.exists():
        return HTMLResponse(content=checklist_path.read_text(encoding="utf-8"))
    return HTMLResponse(content="<h1>AI Engineer Roadmap</h1><p>index.html not found</p>")

app.mount("/", StaticFiles(directory=str(BASE_DIR), html=True), name="static")

if __name__ == "__main__":
    print("\n" + "="*60)
    print("[SERVER] AI Engineer Roadmap Checklist Server is running!")
    print("-> Open in browser: http://localhost:8000")
    print(f"-> Saving data to:  {STATE_FILE}")
    print("="*60 + "\n")
    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True)
