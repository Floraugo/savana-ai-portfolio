import requests

# Test that the backend is working
url = "http://localhost:8000/generate-grant"

test_data = {
    "nonprofit_name": "Savana Signatures Foundation",
    "mission": "We empower underserved communities through education and arts programs",
    "location": "New York, NY",
    "annual_budget": "$250,000",
    "funder_name": "Gates Foundation",
    "amount_requested": "$50,000",
    "project_description": "Youth literacy programme for children ages 8-14 in underserved communities"
}

print("Sending request to AI backend...")
response = requests.post(url, json=test_data)

if response.status_code == 200:
    result = response.json()
    print("\n✅ SUCCESS! Here's the generated grant text:\n")
    print(result["grant_text"])
else:
    print(f"\n❌ Error: {response.status_code}")
    print(response.json())
