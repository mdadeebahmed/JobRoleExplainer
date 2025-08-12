from fastapi import FastAPI, Request, Header, HTTPException, Response
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import openai
import os

# -------------------
# CONFIG
# -------------------
openai.api_key = os.getenv("OPENAI_API_KEY")  # Make sure you set this in your environment
API_TOKEN = "abc123"  # Replace with a strong token you create

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
# MCP endpoint (POST only)
# -------------------
@app.post("/mcp")
async def mcp_endpoint(request: Request, authorization: str = Header(None)):
    if authorization != f"Bearer {API_TOKEN}":
        raise HTTPException(status_code=401, detail="Unauthorized")

    try:
        body = await request.json()
    except Exception:
        return JSONResponse(content={"error": "Invalid JSON body"}, status_code=400)

    tool = body.get("tool")

    if tool == "validate":
        # Return your phone number in required format (country_code + number)
        return JSONResponse(content={"result": "91XXXXXXXXXX"})

    return JSONResponse(content={"error": "Unknown tool"}, status_code=400)

# -------------------
# MCP endpoint GET handler to respond with 405 Method Not Allowed
# -------------------
@app.get("/mcp")
async def mcp_get():
    return Response(
        content="GET method not allowed on /mcp endpoint. Please use POST.",
        status_code=405,
        headers={"Allow": "POST"},
    )
