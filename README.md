# Alrouf Lighting Technology Pvt Ltd. - Task 2: Quotation Microservice

This repository contains the implementation of the Quotation Microservice (Task 2) as part of the Alrouf Lighting Technology Pvt Ltd. Task Pack. The microservice provides a `POST /quote` endpoint using FastAPI, integrating with OpenAI for email draft generation, and includes mocks for local runs without secrets.

## General Notes
- **Tools Allowed**: Python (FastAPI/Flask), OpenAI API.
- **Deliverables**: README, `.env.sample`, and a 3-7 min video walkthrough.
- **Requirement**: Include mocks so we can run locally without secrets.

## Prerequisites
- Python 3.12
- Docker (optional, for containerized setup)

## Setup Instructions

### Option 1: Using Docker
1. **Install Docker**: Ensure Docker is installed on your system.
2. **Copy Environment File**:
   - Copy `.env.sample` to `.env`:
     ```bash
     cp .env.sample .env
     ```
   - Edit `.env` to set `OPENAI_API_KEY` if using the real API (leave blank for mock mode).
3. **Build the Docker Image**:
   ```bash
   docker build -t quotation-service .
   ```
4. **Run the Container**:
   ```bash
   docker run -p 8000:8000 -e quotation-service
   ```
   - Access the API at `http://localhost:8000/docs` for OpenAPI documentation.
   - Use `docker run -p 8000:8000 -e OPENAI_API_KEY=your_key` for production with real keys.
5. **Test the Application**:
   - Send a POST request to `http://localhost:8000/quote` with the sample JSON:
     ```json
     {
       "client": {"name": "Gulf Eng.", "contact": "omar@client.com", "lang": "en"},
       "currency": "SAR",
       "items": [
         {"sku": "ALR-SL-90W", "qty": 120, "unit_cost": 240.0, "margin_pct": 22},
         {"sku": "ALR-OBL-12V", "qty": 40, "unit_cost": 95.5, "margin_pct": 18}
       ],
       "delivery_terms": "DAP Dammam, 4 weeks",
       "notes": "Client asked for spec compliance with Tarsheed."
     }
     ```

### Option 2: Using Virtual Environment
1. **Create a Virtual Environment**:
   ```bash
   python -m venv venv
   ```
2. **Activate the Virtual Environment**:
   - On Windows: `venv\Scripts\activate`
   - On macOS/Linux: `source venv/bin/activate`
3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Copy Environment File**:
   - Copy `.env.sample` to `.env`:
     ```bash
     cp .env.sample .env
     ```
   - Edit `.env` to set `OPENAI_API_KEY` if needed (leave blank for mock mode).
5. **Run the Application**:
   ```bash
   uvicorn app:app --host 0.0.0.0 --port 8000 --reload
   ```
   - Access the API at `http://localhost:8000/docs`.
6. **Run Tests**:
   ```bash
   pytest tests/
   ```

## Task Details
### Task 2 - Quotation Microservice (Python + OpenAI)
- **Endpoint**: `POST /quote` (FastAPI)
- **Input JSON**: As shown in the test example above.
- **Logic**: 
  - Price per line = `unit_cost × (1 + margin_pct%) × qty`
  - Returns line totals, grand total, and an email draft (AR/EN) summarizing price, terms, and notes.
- **Non-Functional Requirements**:
  - Tests (pytest) in `tests/`
  - Dockerfile for containerization
  - OpenAPI docs available at `/docs`
  - Local run without keys (mock LLM implemented)

## Configuration
- Use `.env` for environment variables (see `.env.sample`).
- Mock mode enabled by default (`MOCK_MODE=true`) for local runs without secrets.

## Deliverables
- **README**: This file.
- **.env.sample**: Configuration template.
- **Video Walkthrough**: 3-7 min video (to be uploaded separately) showing setup, API testing, and Docker run.

## Notes
- The task is due in three days (October 11, 2025, 1:04 PM PKT).
- Ensure all code is runnable locally with mocks as per general criteria.