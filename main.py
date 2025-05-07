# === SOXFlow FastAPI App (Deployable) ===
# This version adds deployment-ready scaffolding, routing, and Docker config for a hosted API.

import openai
import re
import os
from typing import Dict, Tuple
from fastapi import FastAPI, UploadFile, Form
from pydantic import BaseModel

openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI(title="SOXFlow AI Engine")

# === Data Models ===
class ControlInput(BaseModel):
    control_id: str
    process_name: str
    control_objective: str
    risk_category: str
    frequency: str
    control_steps: str
    system_used: str

class EvidenceInput(BaseModel):
    approver: str = ""
    form_attached: bool = False
    date: str = ""
    deadline: str = ""

# === GPT Narrative/Test Script Generator ===
def generate_narrative_and_test(control_fields: Dict[str, str]) -> Tuple[str, str]:
    prompt = f"""
    You are a SOX compliance and IT audit expert. Respond in two clearly labeled sections:

    Narrative:
    Provide a detailed control narrative...

    Test Script:
    Write an audit-ready test script...

    Control ID: {control_fields['control_id']}
    ...
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a SOX audit and compliance assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        output = response['choices'][0]['message']['content']
        match = re.search(r"Narrative:\\s*(.*?)\\s*Test Script:\\s*(.*)", output, re.DOTALL)
        return (match.group(1).strip(), match.group(2).strip()) if match else ("", "")
    except Exception as e:
        print("🔥 OpenAI request failed:", str(e))
        raise
# === Dockerfile for Deployment ===
# This is assumed to be placed in the same project root as main.py
#
# FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10
# COPY . /app
# RUN pip install openai
# ENV MODULE_NAME=main
# ENV VARIABLE_NAME=app

# === Run Locally ===
# uvicorn main:app --reload

# === Deployment Targets ===
# - Render.com: point to GitHub repo with above Dockerfile
# - Vercel: with ASGI wrapper
# - Railway.app: drop-in container deploy

# === Manual Input Needed ===
# ✅ You must now create a GitHub repo named `soxflow-core` and upload this file + a `Dockerfile`.
# Once done, tell me the repo URL and I will:
# - auto-deploy it to Render or Railway
# - begin integrating file upload & dashboard logic
