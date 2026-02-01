"""
Main FastAPI application for GEO Platform
Handles API routing and orchestrates analysis workflow
"""


from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from scraper import scrape_website
from ai_handler import generate_ai_answer
from analyzer import analyze_content, extract_recommendations
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="GEO Platform API")

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AnalyzeRequest(BaseModel):
    """Request model for analysis endpoint"""
    url: str
    question: str


class AnalyzeResponse(BaseModel):
    """Response model with analysis results"""
    ai_answer: str
    answer_format: str
    ai_topics: list
    website_topics: list
    missing_topics: list
    content_gaps: list
    recommendations: list
    scraped_content_preview: str


@app.get("/")
async def root():
    """Health check endpoint"""
    return {"status": "GEO Platform API is running"}


@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze_website(request: AnalyzeRequest):
    """
    Main analysis endpoint
    
    Steps:
    1. Scrape website content
    2. Generate AI answer for the question
    3. Analyze both contents
    4. Extract topics and identify gaps
    5. Generate recommendations
    """
    try:
        logger.info(f"Starting analysis for URL: {request.url}")
        logger.info(f"Question: {request.question}") 
        
        
        # Step 1: Scrape website content
        logger.info("Scraping website...")
        website_content = scrape_website(request.url)
        
        if not website_content:
            raise HTTPException(status_code=400, detail="Failed to scrape website content")
        
        # Step 2: Generate AI answer
        logger.info("Generating AI answer...")
        ai_answer = generate_ai_answer(request.question)
        
        if not ai_answer:
            raise HTTPException(status_code=500, detail="Failed to generate AI answer")
        
        # Step 3: Analyze content and extract topics
        logger.info("Analyzing content...")
        analysis_results = analyze_content(website_content, ai_answer, request.question)
        
        # Step 4: Generate recommendations
        logger.info("Generating recommendations...")
        recommendations = extract_recommendations(
            analysis_results['missing_topics'],
            analysis_results['content_gaps'],
            analysis_results['answer_format']
        )
        
        # Prepare response
        response = AnalyzeResponse(
            ai_answer=ai_answer,
            answer_format=analysis_results['answer_format'],
            ai_topics=analysis_results['ai_topics'],
            website_topics=analysis_results['website_topics'],
            missing_topics=analysis_results['missing_topics'],
            content_gaps=analysis_results['content_gaps'],
            recommendations=recommendations,
            scraped_content_preview=website_content[:500] + "..."
        )
        
        logger.info("Analysis complete")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error during analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
