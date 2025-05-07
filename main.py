from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Tuple
import re
import os
from openai import OpenAI

app = FastAPI(title="SOXFlow API")

# === Pydantic Input Model ===
class ControlInput(BaseModel):
    control_id: str
    process_name: str
    control_objective: str
    risk_category: str
    frequency: str
    control_steps: str
    system_used: str

# === OpenAI Completion Function ===
def generate_narrative_and_test(control_fields: Dict[str, str]) -> Tuple[str, str]:
    client = OpenAI()

    prompt = f"""
    You are a SOX compliance and IT audit expert. Respond in two clearly labeled sections:

    Narrative:
    Provide a detailed control narrative that explains the control’s objective, frequency, scope, and how it operates in business terms.

    Test Script:
    Write an audit-ready test script using PCAOB standards including population, sample selection, evidence, and expected outcome. Format clearly using step-by-step numbering.

    Control ID: {control_fields['control_id']}
    Process Name: {control_fields['process_name']}
    Control Objective: {control_fields['control_objective']}
    Risk Category: {control_fields['risk_category']}
    Frequency: {control_fields['frequency']}
    Control Steps: {control_fields['control_steps']}
    System Used: {control_fields['system_used']}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a SOX audit and compliance assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        output = response.choices[0].message.content
        match = re.search(r"Narrative:\s*(.*?)\s*Test Script:\s*(.*)", output, re.DOTALL)
        return (match.group(1).strip(), match.group(2).strip()) if match else ("", "")
    except Exception as e:
        print("🔥 OpenAI request failed:", str(e))
        raise

# === Endpoint ===
@app.post("/generate-docs")
def api_generate_docs(input: ControlInput):
    try:
        narrative, script = generate_narrative_and_test(input.dict())
        return {"narrative": narrative, "test_script": script}
    except Exception as e:
        print("🔥 OpenAI Error:", str(e))
        return {"narrative": "", "test_script": f"OpenAI Error: {str(e)}"}
