from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import openai
import os

# -------------------
# CONFIG
# -------------------
openai.api_key = os.getenv("OPENAI_API_KEY")  # Make sure you set this in your environment

app = FastAPI()

# Serve static files (script.js)
app.mount("/static", StaticFiles(directory="static"), name="static")

# -------------------
# Request Model
# -------------------
class JobRequest(BaseModel):
    job_title: str

# -------------------
# Routes
# -------------------
@app.get("/", response_class=HTMLResponse)
async def serve_home():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.post("/explain_job_role")
async def explain_job_role(req: JobRequest):
    prompt = f"Explain the role, responsibilities, and required skills for the job title: {req.job_title}."

    try:
        completion = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful career advisor."},
                {"role": "user", "content": prompt}
            ]
        )

        # ✅ Correct way for new SDK
        result_text = completion.choices[0].message.content

        return {"result_markdown": result_text}

    except Exception as e:
        return {"error": str(e)}
