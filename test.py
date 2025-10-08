import pytest
from fastapi.testclient import TestClient
from app import app  # Assume app is defined in app.py from previous context
from pydantic import BaseModel, Field
from typing import List

client = TestClient(app)

# Test data
test_data_1 = {
    "client": {"name": "Gulf Eng.", "contact": "omar@client.com", "lang": "en"},
    "currency": "SAR",
    "items": [
        {"sku": "ALR-SL-90W", "qty": 120, "unit_cost": 240.0, "margin_pct": 22},
        {"sku": "ALR-OBL-12V", "qty": 40, "unit_cost": 95.5, "margin_pct": 18}
    ],
    "delivery_terms": "DAP Dammam, 4 weeks",
    "notes": "Client asked for spec compliance with Tarsheed."
}

test_data_2 = {
    "client": {"name": "Desert Corp", "contact": "ahmed@desert.com", "lang": "ar"},
    "currency": "USD",
    "items": [
        {"sku": "ALR-SL-50W", "qty": 50, "unit_cost": 150.0, "margin_pct": 20},
        {"sku": "ALR-OBL-24V", "qty": 30, "unit_cost": 80.0, "margin_pct": 15}
    ],
    "delivery_terms": "EXW Riyadh, 3 weeks",
    "notes": "Urgent delivery required."
}

test_data_3 = {
    "client": {"name": "Oasis Ltd.", "contact": "sara@oasis.com", "lang": "en"},
    "currency": "SAR",
    "items": [
        {"sku": "ALR-SL-90W", "qty": 200, "unit_cost": 240.0, "margin_pct": 25}
    ],
    "delivery_terms": "DAP Jeddah, 6 weeks",
    "notes": "Include warranty details."
}



class QuoteResponse(BaseModel):
    subject: str = Field(..., example="subject of the email")
    body: str = Field(..., example="body of the email")
    grand_total: float
    line_totals: List[float]

@pytest.mark.parametrize("test_data", [test_data_1, test_data_2, test_data_3])
def test_generate_quote(test_data):
    response = client.post("/quote", json=test_data)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data["grand_total"], float)
    assert isinstance(data["line_totals"], list)
    assert len(data["line_totals"]) == len(test_data["items"])
    assert "subject" in data
    assert "body" in data

def test_invalid_input():
    invalid_data = {
        "client": {"name": "", "contact": "invalid@", "lang": "en"},  # Invalid email
        "currency": "SAR",
        "items": [],
        "delivery_terms": "DAP Dammam, 4 weeks",
        "notes": "Invalid test case"
    }
    response = client.post("/quote", json=invalid_data)
    assert response.status_code == 422  # Unprocessable Entity for invalid input

def test_missing_required_field():
    incomplete_data = {
        "client": {"name": "Gulf Eng.", "contact": "omar@client.com"},  # Missing lang
        "currency": "SAR",
        "items": [{"sku": "ALR-SL-90W", "qty": 120, "unit_cost": 240.0, "margin_pct": 22}]
    }
    response = client.post("/quote", json=incomplete_data)
    assert response.status_code == 422  # Unprocessable Entity for missing field