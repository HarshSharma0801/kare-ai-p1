from fastapi import FastAPI
from pydantic import BaseModel
from typing import Any, Dict
import json
from fastapi.middleware.cors import CORSMiddleware


# Assuming the IndustryAnalysis class and its methods are properly defined in model.py
from model import IndustryAnalysis

# Instantiate the IndustryAnalysis object with the provided API key and model
api_key = "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"
grok_model = "mixtral-8x7b-32768"
news_api_key = "2f4a447b4c3942b2bb0504ea778ee9cc"

analysis = IndustryAnalysis(api_key, grok_model, news_api_key)

app = FastAPI()

app.add_middleware(
    CORSMiddleware, allow_origins=origins, allow_methods=["*"], allow_headers=["*"]
)

@app.get("/")
def read_root():
    return {"message": "Yahoo the server is up and running !"}

class IndustryRequest(BaseModel):
    industry_sector: str
    industry_subsector: str
    region: str

class KeyTakeawaysRequest(BaseModel):
    industry_sector: str
    industry_subsector: str
    company_value_proposition: str
    region: str

@app.post("/top_competitors/")
def top_competitors(request: IndustryRequest):
    result = analysis.find_top_competitors(
        request.industry_sector,
        request.industry_subsector,
        request.region
    )
    result = json.loads(result)
    return {"top_competitors": result}

@app.post("/industry_news/")
def industry_news(request: IndustryRequest):
    result = analysis.get_articles(
        request.industry_sector,
        request.industry_subsector,
        request.region
    )
    return {"industry_news": result}


@app.post("/technological_trends/")
def technological_trends(request: IndustryRequest):
    result = analysis.find_technological_trends(
        request.industry_sector,
        request.industry_subsector,
        request.region
    )
    result = json.loads(result)
    return {"technological_trends": result}

@app.post("/industry_trends/")
def industry_trends(request: IndustryRequest):
    result = analysis.find_industry_trends(
        request.industry_sector,
        request.industry_subsector,
        request.region
    )
    result = json.loads(result)
    return {"industry_trends": result}

@app.post("/key_takeaways/")
def key_takeaways(request: KeyTakeawaysRequest):
    result = analysis.find_key_takeways(
        request.industry_sector,
        request.industry_subsector,
        request.company_value_proposition,
        request.region
    )
    result = json.loads(result)
    return {"key_takeaways": result}

@app.post("/top_5_predictions/")
def top_5_predictions(request: IndustryRequest):
    result = analysis.top_5_predictions(
        request.industry_sector,
        request.industry_subsector,
        request.region
    )
    result = json.loads(result)
    return {"top_5_predictions": result}
