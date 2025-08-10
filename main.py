from fastapi import FastAPI, Request, Header, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import openai
import os

# -------------------
# CONFIG
# -------------------
openai.api_key = os.getenv("OPENAI_API_KEY")  # Make sure you set this in your environment
API_TOKEN = "7f3a9b2d-e1c4-4d9f-8a62-3bcf0d5e7a1b"  # Replace with a strong token you create

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

        result_text = completion.choices[0].message.content

        return {"result_markdown": result_text}

    except Exception as e:
        return {"error": str(e)}

# -------------------
# MCP endpoint
# -------------------
@app.post("/")
async def mcp_endpoint(request: Request, authorization: str = Header(None)):
    if authorization != f"Bearer {API_TOKEN}":
        raise HTTPException(status_code=401, detail="Unauthorized")

    body = await request.json()
    tool = body.get("tool")

    if tool == "validate":
        # Return your phone number in required format
        return JSONResponse(content={"result": "+916300670761"})

    return JSONResponse(content={"error": "Unknown tool"}, status_code=400)

@app.post("/mcp")
async def mcp_endpoint_alias(request: Request, authorization: str = Header(None)):
    return await mcp_endpoint(request, authorization)
