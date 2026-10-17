from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import anthropic
import logging
import os

app = FastAPI()
logger = logging.getLogger(__name__)

# Only allow requests from the Savana frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://savana-scribe.lovable.app"],
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "X-API-Key"],
)

# Anthropic client, key loaded from environment
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))


# Reject requests without a valid API key
def verify_api_key(x_api_key: str = Header(default=None)):
    expected_key = os.environ.get("SAVANA_API_KEY")
    if not expected_key or x_api_key != expected_key:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")


# Request body for /generate-grant
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


@app.post("/generate-grant", dependencies=[Depends(verify_api_key)])
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
        # Log the full error, return a generic message to the client
        logger.error(f"Grant generation failed: {e}")
        raise HTTPException(
            status_code=500,
            detail="Something went wrong generating the grant. Please try again."
        )
