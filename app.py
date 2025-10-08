import os
from fastapi import FastAPI, HTTPException, status, Request
from fastapi.responses import JSONResponse
from openai import AsyncOpenAI
import uvicorn
import json
from model.client import QuoteResponse, QuoteRequest
from modules.mock import get_prompt
from modules.utils import calculate_totals
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

rate_limits = {}
LIMIT = 10
WINDOW = 60


def get_client_id(request: Request):
    return request.client.host


async def rate_limit_middleware(request: Request, call_next):
    client_id = get_client_id(request)
    current_time = datetime.now()

    if client_id not in rate_limits:
        rate_limits[client_id] = {"count": 0, "last_reset": current_time}

    entry = rate_limits[client_id]
    if (current_time - entry["last_reset"]).total_seconds() > WINDOW:
        entry["count"] = 0
        entry["last_reset"] = current_time

    entry["count"] += 1

    if entry["count"] > LIMIT:
        raise HTTPException(
            status_code=429,
            detail=f"Too Many Requests. Limit is {LIMIT} requests per {WINDOW} seconds."
        )

    response = await call_next(request)
    return response


app = FastAPI(title="Quotation Microservice", version="1.0.0")

app.middleware("http")(rate_limit_middleware)


@app.post("/quote", response_model=QuoteResponse)
async def generate_quote(request: QuoteRequest):
    try:
        grand_total,line_totals = await calculate_totals(request)
        request = request.dict()
        if os.getenv("OPENAI_API_KEY"):
            prompt = await get_prompt(request=request,total=grand_total,mode="openai")

            client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            response = await client.responses.parse(
                model="gpt-4o-2024-08-06",
                input=prompt,
                text_format=QuoteResponse,
            )
            draft = response.output_parsed
            draft["line_totals"] = line_totals
            draft["grand_total"] = grand_total
            return JSONResponse(content=draft.dict(), status_code=status.HTTP_200_OK)
        else:
            draft = await get_prompt(request=request, total=grand_total, mode="mock")
            draft["line_totals"] = line_totals
            draft["grand_total"] = grand_total
            return JSONResponse(content=draft, status_code=status.HTTP_200_OK)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
