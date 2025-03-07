from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from transformers import pipeline
from fastapi.responses import HTMLResponse
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

templates = Jinja2Templates(directory="backend")


class TextInput(BaseModel):
    text: str
    language: str


# Load models with error handling
try:
    logger.info("Loading English sentiment model...")
    english_model = pipeline("sentiment-analysis")
    logger.info("English model loaded successfully")
except Exception as e:
    logger.error(f"Error loading English model: {str(e)}")
    english_model = None

try:
    logger.info("Loading Arabic sentiment model...")
    arabic_model = pipeline(
        "sentiment-analysis",
        model="CAMeL-Lab/bert-base-arabic-camelbert-mix-sentiment"
    )
    logger.info("Arabic model loaded successfully")
except Exception as e:
    logger.error(f"Error loading Arabic model: {str(e)}")
    arabic_model = None


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/analyze")
def analyze_text(input: TextInput):
    try:
        if input.language.lower() == "arabic":
            # Check if Arabic model is available
            if arabic_model is None:
                return {"error": "Arabic model not available", "text": input.text, "language": input.language}

            # Use the Arabic-specific model
            result = arabic_model(input.text)[0]
            sentiment = {"label": result['label'], "score": result['score']}
        else:
            # Check if English model is available
            if english_model is None:
                return {"error": "English model not available", "text": input.text, "language": input.language}

            # Use the English model
            result = english_model(input.text)[0]
            sentiment = {"label": result['label'], "score": result['score']}

        return {"text": input.text, "language": input.language, "sentiment": sentiment}
    except Exception as e:
        logger.error(f"Error analyzing text: {str(e)}")
        return {"error": str(e), "text": input.text, "language": input.language}
