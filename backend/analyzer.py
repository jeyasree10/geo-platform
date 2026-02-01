"""
Content Analyzer module
Performs TF-IDF analysis, topic extraction, and gap detection
"""

import logging
from typing import Dict, List
from collections import Counter
import re
import math

logger = logging.getLogger(__name__)


def analyze_content(website_content: str, ai_answer: str, question: str) -> Dict:
    """
    Analyze website content and AI answer to identify gaps
    
    Args:
        website_content: Scraped website text
        ai_answer: AI-generated answer
        question: Original user question
        
    Returns:
        Dictionary with analysis results
    """
    logger.info(f"Starting content analysis for question: '{question}'")  # ✅ ADD THIS
    
    # ✅ CHANGED: Pass question to extract_topics
    ai_topics = extract_topics(ai_answer, top_n=15, question=question)
    logger.info(f"✅ Extracted {len(ai_topics)} AI topics: {ai_topics[:5]}")  # ✅ ADD THIS
    
    website_topics = extract_topics(website_content, top_n=15, question=question)
    logger.info(f"✅ Extracted {len(website_topics)} website topics: {website_topics[:5]}")  # ✅ ADD THIS
    
    # Find missing topics (in AI answer but not on website)
    missing_topics = identify_missing_topics(ai_topics, website_topics, website_content)
    
    # Detect answer format
    answer_format = detect_answer_structure(ai_answer)
    
    # Identify content gaps
    content_gaps = identify_content_gaps(website_content, ai_answer, question)
    
    results = {
        'ai_topics': ai_topics,
        'website_topics': website_topics,
        'missing_topics': missing_topics,
        'answer_format': answer_format,
        'content_gaps': content_gaps
    }
    
    logger.info(f"Analysis complete. Found {len(missing_topics)} missing topics")
    return results


def extract_topics(text: str, top_n: int = 15, question: str = "") -> List[str]:
    """Extract important topics using TF-IDF-like approach"""
    
    # Clean and tokenize
    text = text.lower()
    text = re.sub(r'[^\w\s]', ' ', text)
    words = text.split()
    
    # Stop words to filter out
    stop_words = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
        'of', 'with', 'by', 'from', 'up', 'about', 'into', 'through', 'during',
        'before', 'after', 'above', 'below', 'between', 'under', 'again', 'further',
        'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all',
        'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such',
        'only', 'own', 'same', 'so', 'than', 'too', 'very', 'can', 'will',
        'just', 'should', 'now', 'this', 'that', 'these', 'those', 'it', 'its',
        'they', 'them', 'their', 'what', 'which', 'who', 'when', 'where', 'why',
        'how', 'could', 'should', 'might', 'being', 'been', 'have', 'has', 'had',
        'do', 'does', 'did', 'may', 'must', 'shall', 'have', 'has'
    }
    
    # Filter words
    filtered_words = [
        w for w in words
        if w not in stop_words and len(w) > 3 and not w.isdigit()
    ]
    
    # Calculate word frequencies
    word_freq = Counter(filtered_words)
    
    # Extract top N words
    top_words = [word for word, _ in word_freq.most_common(top_n)]
    
    # ✅ NEW: Prioritize words from the question
    if question:
        question_words = set(w.lower() for w in question.split() if len(w) > 3 and w.lower() not in stop_words)
        
        # Sort: question-related words first, then by frequency
        top_words = sorted(top_words, key=lambda w: (
            -(1 if w in question_words else 0),  # Question words first
            -word_freq.get(w, 0)  # Then by frequency
        ))
    
    return top_words[:top_n]
def identify_missing_topics(ai_topics: List[str], website_topics: List[str],
                          website_content: str) -> List[str]:
    """Identify topics present in AI answer but missing from website"""
    
    missing = []
    website_content_lower = website_content.lower()
    website_topics_lower = set(t.lower() for t in website_topics)  # ✅ ADD THIS
    
    for topic in ai_topics:
        topic_lower = topic.lower()  # ✅ ADD THIS
        
        # ✅ IMPROVED: Check both topic list and content frequency
        if topic_lower not in website_topics_lower:
            # Double-check it's not just a frequency difference
            if website_content_lower.count(topic_lower) < 2:
                missing.append(topic)
                logger.info(f"Missing topic identified: {topic}")  # ✅ ADD DEBUG LOG
    
    logger.info(f"✅ Found {len(missing)} missing topics")  # ✅ ADD THIS
    return missing[:10]  # Return top 10 missing topics




def detect_answer_structure(answer: str) -> str:
    """
    Detect the structural format of the AI answer
    
    Args:
        answer: AI-generated answer
        
    Returns:
        Format description
    """
    lines = answer.split('\n')
    
    # Count different structural elements
    bullet_points = sum(1 for line in lines if line.strip().startswith(('•', '*', '-')))
    numbered_items = sum(1 for line in lines if line.strip() and 
                        len(line.strip()) > 2 and line.strip()[0].isdigit() and 
                        line.strip()[1] in '.)')
    paragraphs = len([p for p in answer.split('\n\n') if len(p.strip()) > 50])
    
    # Determine primary format
    if numbered_items >= 3:
        return "Numbered Steps/List"
    elif bullet_points >= 3:
        return "Bullet Points"
    elif paragraphs >= 3:
        return "Multi-Paragraph"
    elif paragraphs >= 1:
        return "Single Paragraph"
    else:
        return "Mixed Format"

def identify_content_gaps(website_content: str, ai_answer: str, question: str) -> List[str]:
    """Identify specific content gaps between website and AI answer"""
    
    logger.info(f"Identifying content gaps for: '{question}'")  # ✅ ADD THIS
    
    gaps = []
    
    # ✅ ADD: Extract question keywords for context
    question_keywords = set(w.lower() for w in question.split() if len(w) > 3)
    
    # Check for structural elements in AI answer
    ai_has_examples = 'example' in ai_answer.lower() or 'for instance' in ai_answer.lower()
    website_has_examples = 'example' in website_content.lower() or 'for instance' in website_content.lower()
    
    if ai_has_examples and not website_has_examples:
        gaps.append(f"AI answer includes examples, but website lacks concrete examples about '{question}'")  # ✅ MADE SPECIFIC

    
    if ai_has_examples and not website_has_examples:
        gaps.append("AI answer includes examples, but website lacks concrete examples")
    
    # Check for statistics/data
    ai_has_numbers = bool(re.search(r'\d+%|\d+ percent|\$\d+', ai_answer))
    website_has_numbers = bool(re.search(r'\d+%|\d+ percent|\$\d+', website_content))
    
    if ai_has_numbers and not website_has_numbers:
        gaps.append("AI answer includes statistics/data, but website lacks quantitative information about '" + question + "'")
    
    # Check for step-by-step instructions
    ai_has_steps = bool(re.search(r'\d+\.', ai_answer)) and 'step' in ai_answer.lower()
    website_has_steps = bool(re.search(r'\d+\.', website_content)) and 'step' in website_content.lower()
    
    if ai_has_steps and not website_has_steps:
        gaps.append("AI answer provides step-by-step guidance, but website lacks structured instructions for '" + question + "'")
    
    # Check for best practices section
    if 'best practice' in ai_answer.lower() and 'best practice' not in website_content.lower():
        gaps.append("AI answer highlights best practices, but website doesn't emphasize them")
    
    # Check for benefits/advantages discussion
    ai_has_benefits = 'benefit' in ai_answer.lower() or 'advantage' in ai_answer.lower()
    website_has_benefits = 'benefit' in website_content.lower() or 'advantage' in website_content.lower()
    
    if ai_has_benefits and not website_has_benefits:
        gaps.append("AI answer discusses benefits/advantages, but website doesn't clearly articulate them")
    
    # Check content depth
    ai_words = len(ai_answer.split())
    website_words = len(website_content.split())
    
    if ai_words > 300 and website_words < 500:
        gaps.append("AI provides comprehensive answer, but website content appears thin")
    
    return gaps[:8]  # Return top 8 gaps


def extract_recommendations(missing_topics: List[str], content_gaps: List[str], 
                           answer_format: str) -> List[str]:
    """
    Generate actionable recommendations for website optimization
    
    Args:
        missing_topics: Topics missing from website
        content_gaps: Identified content gaps
        answer_format: Detected AI answer format
        
    Returns:
        List of recommendations
    """
    logger.info(f"Generating recommendations for: '{question}'")
    recommendations = []
    
    # Topic-based recommendations
    if missing_topics:
        topics_str = ', '.join(missing_topics[:5])
        recommendations.append(
            f"📝 Add content covering these topics related to '{question}': {topics_str}"
        )
    
    # Format-based recommendations
    if answer_format == "Numbered Steps/List":
        recommendations.append(
            f"📊 Structure your content with numbered steps or lists - AI tends to present '{question}' in step format"
            
        )
    elif answer_format == "Bullet Points":
        recommendations.append(
            f"🔹 Use bullet points to organize key information about '{question}' - AI responds to this topic with bulleted lists"
            
        )
    
    # Gap-based recommendations
    for gap in content_gaps[:3]:  # Top 3 gaps
        if "examples" in gap.lower():
            recommendations.append(
                "💡 Include concrete examples and real-world use cases to match AI comprehensiveness"
            )
        elif "statistics" in gap.lower() or "data" in gap.lower():
            recommendations.append(
                "📊 Add statistics, data points, or quantitative information to strengthen credibility"
            )
        elif "step-by-step" in gap.lower():
            recommendations.append(
                "🔢 Create step-by-step guides or how-to sections for better AI discoverability"
            )
        elif "best practice" in gap.lower():
            recommendations.append(
                "⭐ Highlight best practices and expert recommendations explicitly"
            )
        elif "benefits" in gap.lower():
            recommendations.append(
                "✅ Clearly articulate benefits and advantages in dedicated sections"
            )
    
    # General SEO/GEO recommendations
    recommendations.append(
        "🎯 Use clear headings (H2, H3) that match common question patterns AI recognizes"
    )
    
    recommendations.append(
        "🔍 Include FAQ sections addressing variations of common questions in your topic area"
    )
    
    # Content depth recommendation
    if len(content_gaps) > 3:
        recommendations.append(
            "📈 Expand content depth - AI provides more comprehensive answers than your current content"
        )
    
    return recommendations[:8]  # Return top 8 recommendations
