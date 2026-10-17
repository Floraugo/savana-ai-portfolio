# Savana AI – Grant Genius

A FastAPI backend that writes grant executive summaries for non-profits using the Anthropic Claude API.

I built this during my AI Developer placement at Legal Pythia. A teammate built the frontend, and this API handles the grant generation behind it.

## How it works

1. The frontend sends the non-profit's details (name, mission, location, budget, funder, amount requested and project description) to /generate-grant.
2. The request is validated with Pydantic.
3. The details go into a structured prompt, which is sent to Claude.
4. The executive summary comes back as JSON.

## Tech stack

- Python
- FastAPI and Uvicorn
- Anthropic Claude API
- Pydantic
- Render (deployment)

## Security

- CORS is restricted to the frontend domain
- /generate-grant requires an API key in the X-API-Key header
- API keys are stored as environment variables, not in the code
- Errors are logged on the server, and the client gets a generic message

## Running locally

Install the dependencies:


pip install -r requirements.txt


Set the environment variables:


export ANTHROPIC_API_KEY="your-anthropic-key"
export SAVANA_API_KEY="your-chosen-key"


Start the server:


uvicorn main:app --reload


Then, in a second terminal, run the test script:

```
