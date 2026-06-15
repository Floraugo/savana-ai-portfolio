from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import anthropic
import os

app = FastAPI()

# Allow the frontend (Joy's UI) to talk to this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to Joy's frontend URL in production
    allow_methods=["*"],
    allow_headers=["*"],
)

# Claude client — reads your API key from environment variable
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))


# This is the shape of data we expect from the frontend
class GrantRequest(BaseModel):
    nonprofit_name: str
    mission: str
    location: str
    annual_budget: str
    funder_name: str
    amount_requested: str
    project_description: str


@app.get("/")
def root():
    return {"status": "Grant Genius AI is running"}


@app.post("/generate-grant")
def generate_grant(data: GrantRequest):
    try:
        prompt = f"""You are an expert nonprofit grant writer with 20 years of experience 
writing successful grant proposals. Write a compelling executive summary for the following:

Nonprofit: {data.nonprofit_name}
Mission: {data.mission}
Location: {data.location}
Annual Budget: {data.annual_budget}
Funder: {data.funder_name}
Amount Requested: {data.amount_requested}
Project: {data.project_description}

Write a professional 2-3 paragraph executive summary that:
- Opens with the nonprofit's mission and impact
- Clearly states the funding request and purpose
- Explains why this project matters and what outcomes it will achieve
- Ends with a strong closing statement

Be specific, compelling, and professional."""

        message = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}],
        )

        return {
            "success": True,
            "grant_text": message.content[0].text
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
