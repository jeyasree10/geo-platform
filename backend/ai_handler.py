"""
AI Handler module for Gemini API integration
Generates answers using Google's Gemini AI
"""

import requests
import logging
from typing import Optional

logger = logging.getLogger(__name__)

# Placeholder API key (replace with actual key)
GEMINI_API_KEY = "AIza-YOUR_GEMINI_API_KEY_HERE"
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"


def generate_ai_answer(question: str) -> Optional[str]:
    """
    Generate AI answer using Gemini API
    
    Args:
        question: User's question/topic
        
    Returns:
        AI-generated answer or None if failed
    """
    try:
        logger.info(f"Generating AI answer for: {question}")
        
        # Prepare API request
        url = f"{GEMINI_API_URL}?key={GEMINI_API_KEY}"
        
        headers = {
            "Content-Type": "application/json"
        }
        
        payload = {
            "contents": [{
                "parts": [{
                    "text": f"Answer this question comprehensively: {question}"
                }]
            }],
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 1024,
            }
        }
        
        # For demo purposes, if API key is placeholder, use fallback
        if "YOUR_GEMINI_API_KEY" in GEMINI_API_KEY:
            logger.warning("Using placeholder API key - falling back to mock response")
            return generate_mock_answer(question)
        
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            answer = data.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', '')
            logger.info(f"Successfully generated answer: {len(answer)} characters")
            return answer
        else:
            logger.error(f"Gemini API error: {response.status_code}")
            return generate_mock_answer(question)
            
    except Exception as e:
        logger.error(f"AI generation error: {str(e)}")
        return generate_mock_answer(question)


def generate_mock_answer(question: str) -> str:
    """
    Generate a mock AI answer for demo purposes
    
    Args:
        question: User's question
        
    Returns:
        Mock answer with realistic structure
    """
    logger.info("Generating mock answer")
    
    # Create a realistic mock answer based on common patterns
    mock_answer = f"""
{question} - Comprehensive Answer

Overview:
This is an AI-generated response that demonstrates how modern AI search engines typically answer queries. The response is structured to provide clear, actionable information.

Key Points:
• Understanding the fundamentals is crucial for success in this area
• Multiple approaches exist, each with distinct advantages and trade-offs
• Recent developments have significantly impacted best practices
• Industry experts recommend a balanced strategy combining proven methods with innovation

Detailed Explanation:
The topic encompasses several important dimensions that need to be considered together. First, the foundational concepts provide the necessary context for understanding more advanced applications. Second, practical implementation requires careful attention to specific requirements and constraints.

Current trends suggest that organizations are increasingly adopting integrated approaches that leverage both traditional wisdom and emerging technologies. This hybrid methodology has proven effective across various use cases and industries.

Best Practices:
1. Start with a clear understanding of your specific goals and requirements
2. Research current industry standards and proven methodologies
3. Implement solutions incrementally to allow for testing and refinement
4. Monitor results and adjust strategies based on performance data
5. Stay informed about emerging trends and technological advancements

Conclusion:
Success in this domain requires a combination of knowledge, strategy, and consistent execution. By following established best practices while remaining adaptable to change, you can achieve optimal outcomes.
    """.strip()
    
    return mock_answer


def detect_answer_format(answer: str) -> str:
    """
    Detect the structural format of an AI answer
    
    Args:
        answer: AI-generated answer text
        
    Returns:
        Format type (paragraph, bullet_points, numbered_list, mixed)
    """
    bullet_count = answer.count('•') + answer.count('*') + answer.count('-')
    numbered_count = sum(1 for line in answer.split('\n') if line.strip() and line.strip()[0].isdigit())
    
    if bullet_count > 3:
        return "bullet_points"
    elif numbered_count > 3:
        return "numbered_steps"
    elif '\n\n' in answer and len(answer.split('\n\n')) > 2:
        return "multi_paragraph"
    else:
        return "single_paragraph"


def extract_key_phrases(text: str, top_n: int = 10) -> list:
    """
    Extract key phrases from text using simple frequency analysis
    
    Args:
        text: Input text
        top_n: Number of top phrases to return
        
    Returns:
        List of key phrases
    """
    from collections import Counter
    import re
    
    # Remove special characters and convert to lowercase
    text = re.sub(r'[^\w\s]', ' ', text.lower())
    
    # Split into words
    words = text.split()
    
    # Remove common stop words
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
                  'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'be',
                  'this', 'that', 'these', 'those', 'it', 'its', 'can', 'will', 'would'}
    
    filtered_words = [w for w in words if w not in stop_words and len(w) > 3]
    
    # Count word frequency
    word_freq = Counter(filtered_words)
    
    # Get top N words
    top_words = [word for word, _ in word_freq.most_common(top_n)]
    
    return top_words