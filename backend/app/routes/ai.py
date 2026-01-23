from dotenv import load_dotenv
load_dotenv()
from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.event import Event
from pydantic import BaseModel
from typing import List, Optional, Dict
from pathlib import Path
import os
import json
import re
from datetime import datetime
import logging
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.tools import tool
import uuid
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random
import math

router = APIRouter(
    prefix="/ai",
    tags=["AI Features"]
)

def get_llm(temperature: float = 0.7):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="OpenAI API Key not configured")
    return ChatOpenAI(model="gpt-3.5-turbo", temperature=temperature)

class ChatRequest(BaseModel):
    message: str
    context: Optional[str] = None


class DescriptionRequest(BaseModel):
    title: str
    date: Optional[str] = None
    location: Optional[str] = None
    current_description: Optional[str] = None
    keywords: Optional[List[str]] = None

class TitleRequest(BaseModel):
    current_title: str

class ContentGeneratorRequest(BaseModel):
    event_title: str
    user_name: str
    ticket_type: str
    event_date: str
    message_type: str  

class CommentModerationRequest(BaseModel):
    comment_text: str

class ImagePromptRequest(BaseModel):
    event_title: str
    event_type: str
    location: str
    vibe: Optional[str] = None

class PosterRequest(BaseModel):
    title: str
    category: Optional[str] = "EVENT"
    location: Optional[str] = "LIVE EVENT"
    date: Optional[str] = None

# Logger setup
logger = logging.getLogger(__name__)

# Event Description Generator
@router.post("/generate-description")
async def generate_event_description(request: DescriptionRequest):
    """
    Generates a compelling event description based on the title and key details.
    """
    llm = get_llm(temperature=0.8)
    
    prompt = ChatPromptTemplate.from_template(
        """You are an expert event copywriter.
        
        Event Details:
        - Title: {title}
        - Location: {location}
        - Keywords: {keywords}
        - Current Draft: {current_description}
        
        Task:
        Write a captivating, professional, and exciting 2-paragraph description for this event.
        - Paragraph 1: Hook the audience and highlight the main value proposition.
        - Paragraph 2: Provide specific details (what to expect) and a strong call to action.
        
        Tone: Enthusiastic, inviting, and professional.
        
        Return JSON format:
        {{
            "description": "Your generated description here...",
            "improved_title": "Optional better title if the current one is weak"
        }}"""
    )
    
    chain = prompt | llm | StrOutputParser()
    
    try:
        keywords_str = ", ".join(request.keywords) if request.keywords else "None"
        
        result = chain.invoke({
            "title": request.title,
            "location": request.location or "To be announced",
            "keywords": keywords_str,
            "current_description": request.current_description or "None"
        })
        
        cleaned = result.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.split("```")[1].replace("json", "").strip()
            
        return json.loads(cleaned)
    except Exception as e:
        logger.error(f"Description generation error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error generating description: {str(e)}")

#  Website Chatbot 
@router.post("/chat")
async def chat_support(request: ChatRequest, db: Session = Depends(get_db)):
    try:
        logger.info(f"Chatbot received message: {request.message}")
        
        try:
            llm = get_llm()
        except HTTPException as he:
            logger.error(f"LLM Config Error: {he.detail}")
            return {
                "response": "AI Configuration Error: API Key missing.",
                "success": False,
                "error": he.detail
            }
        
        try:
            current_time = datetime.now()
            events = db.query(Event).filter(Event.starts_at >= current_time).order_by(Event.starts_at.asc()).limit(15).all()
            
            events_context = json.dumps([
                {
                    "id": e.id,
                    "title": e.title,
                    "date": e.starts_at.strftime("%Y-%m-%d %H:%M"),
                    "location": e.location,
                    "category": getattr(e, 'category', 'General'),
                    "price": f"Rs. {e.ga_ticket_price}" if e.ga_ticket_price else "Free/Varies",
                    "availability": "Available" if e.capacity > 0 else "Sold Out"
                }
                for e in events
            ], indent=2)
        except Exception as db_err:
            logger.error(f"Database error: {str(db_err)}")
            events_context = "[]"
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", f"""You are "Infinity Bot", the official AI assistant for the Infinity Events platform.
            
YOUR RESPONSIBILITIES:
1. Assist users with finding and booking events.
2. Provide details about ticket prices, locations, and timings.
3. Answer questions about refund/cancellation policies.
4. If you don't know the answer, politely ask the user to contact human support at support@infinityevents.com.

CONTEXT - UPCOMING EVENTS:
{{events_context}}

PLATFORM POLICIES:
- Refund Policy: Full refund if cancelled 7 days before the event. 50% refund if cancelled 3 days before. No refunds within 24 hours.
- Payment Methods: Visa, MasterCard, PayPal, and Bank Transfer.
- Support Email: support@infinityevents.com

GUIDELINES:
- ONLY answer questions related to events and the platform. Refuse irrelevant topics.
- Use the "Upcoming Events" list above to answer specific questions. 
- If the user asks about an event NOT in the list, say "I couldn't find a matching upcoming event."
- Be enthusiastic, professional, and concise.
- Use emojis sparingly to be friendly.
- If unsure, do NOT make up facts. Ask for clarification."""),
            ("user", "{input}"),
        ])
        
        chain = prompt | llm | StrOutputParser()
        
        response = chain.invoke({
            "input": request.message,
            "events_context": events_context
        })
        logger.info(f"Chatbot response: {response}")
        return {
            "response": response,
            "success": True
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        logger.error(f"Chatbot Critical Error: {str(e)}")
        return {
            "response": "I'm having trouble connecting to my brain. Please try later.",
            "success": False,
            "error": str(e)
        }

#  Ticket Support Assistant 
@router.post("/support-assistant")
async def ticket_support_assistant(request: ChatRequest):
    """
    AI support assistant for ticket-related issues:
    - Payment failures
    - QR code problems
    - Seat number issues
    - Booking problems
    """
    llm = get_llm()
    
    support_knowledge = """
PAYMENT FAILURES:
- Check if your card has sufficient funds
- Verify your card details are correct
- Try a different payment method (credit card, PayPal)
- Clear browser cache and retry
- Contact your bank to check for transaction blocks

QR CODE ISSUES:
- Check email (including spam folder) for QR code
- Download the mobile ticket from your account
- Screenshot the QR code for offline access
- QR codes are unique per booking - don't share with others
- If lost, regenerate from your booking confirmation

SEAT NUMBER PROBLEMS:
- Seats are auto-assigned during booking
- Premium seats may have additional charges
- Contact admin@antigravity-ems.com for seat changes
- Some events have general admission (no specific seats)

BOOKING PROBLEMS:
- Ensure all required fields are filled
- Check event capacity - some events may be full
- Verify you're not double-booking
- Contact support if booking repeatedly fails
"""
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", f"""You are a professional ticket support specialist for AntyGravity EMS.

Support Knowledge Base:
{support_knowledge}

Help users troubleshoot their ticket and booking issues. Be empathetic, clear, and provide step-by-step solutions.
If the issue cannot be resolved, provide the support email: support@antigravity-ems.com"""),
        ("user", "{input}"),
    ])
    
    chain = prompt | llm | StrOutputParser()
    
    try:
        response = chain.invoke({"input": request.message})
        return {
            "response": response,
            "support_email": "support@antigravity-ems.com"
        }
    except Exception as e:
        return {
            "response": "Support service temporarily unavailable. Please email support@antigravity-ems.com",
            "error": str(e)
        }

# Smart Search System
@router.post("/smart-search")
async def smart_search(query: str = Body(..., embed=True), db: Session = Depends(get_db)):
    """
    Natural language search that understands intent.
    Examples: "Music events in Colombo tomorrow", "Affordable concerts next week"
    """
    llm = get_llm()
    
    # Fetch only UPCOMING events
    current_time = datetime.now()
    events = db.query(Event).filter(Event.starts_at >= current_time).all()
    if not events:
        return {"events": [], "message": "No events found"}
    
    events_data = []
    for e in events:
        events_data.append({
            "id": e.id,
            "title": e.title,
            "date": str(e.starts_at),
            "location": e.location,
            "category": getattr(e, 'category', 'General'),
            "price": float(e.ga_ticket_price),
            "description": e.description[:150] if e.description else ""
        })
    
    prompt = ChatPromptTemplate.from_template(
        """You are an intelligent event search engine.

Available Events:
{events_data}

User Query: {query}

Analyze the user's natural language query and find the best matching events based on:
- Category/Type
- Location
- Date/Timing
- Price range
- Event description

Return ONLY a JSON array of event IDs that match (max 5). Example: [1, 3, 5]
If no events match, return: []"""
    )
    
    chain = prompt | llm | StrOutputParser()
    
    try:
        result = chain.invoke({
            "events_data": json.dumps(events_data),
            "query": query
        })
        
        # Parse response
        cleaned = result.strip()
        if cleaned.startswith("["):
            ids = json.loads(cleaned)
        else:
            ids = []
        
        # Fetch matched events
        matched_events = db.query(Event).filter(Event.id.in_(ids)).all() if ids else []
        return {
            "query": query,
            "events": [
                {
                    "id": e.id,
                    "title": e.title,
                    "date": str(e.starts_at),
                    "location": e.location,
                    "price": float(e.ga_ticket_price)
                }
                for e in matched_events
            ],
            "count": len(matched_events)
        }
    except Exception as e:
        return {
            "query": query,
            "events": [],
            "error": str(e)
        }

#  Email/SMS Content Generator
@router.post("/generate-content")
async def generate_email_sms_content(request: ContentGeneratorRequest):
    """
    Generates personalized email/SMS content:
    - Booking confirmation messages
    - Event reminder messages
    - Promotional content
    """
    llm = get_llm(temperature=0.8)
    
    templates = {
        "confirmation": """Write a professional yet friendly booking confirmation message for:
- Event: {event_title}
- Customer: {user_name}
- Ticket Type: {ticket_type}
- Event Date: {event_date}

Include: confirmation details, ticket information, QR code reminder, and next steps.
Keep it concise (max 3-4 sentences for SMS, 2 paragraphs for email).""",
        
        "reminder": """Write an engaging event reminder message for:
- Event: {event_title}
- Customer: {user_name}
- Event Date: {event_date}

Include: event excitement, timing reminder, location hint, and call-to-action.
Keep it concise and encouraging.""",
        
        "promotional": """Write a promotional/marketing message for:
- Event: {event_title}
- Event Date: {event_date}

Create buzz and urgency. Highlight unique features and benefits.
Keep it compelling and action-oriented."""
    }
    
    template = templates.get(request.message_type, templates["confirmation"])
    
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | llm | StrOutputParser()
    
    try:
        content = chain.invoke({
            "event_title": request.event_title,
            "user_name": request.user_name,
            "ticket_type": request.ticket_type,
            "event_date": request.event_date
        })
        
        return {
            "message_type": request.message_type,
            "content": content,
            "recipient": request.user_name,
            "event": request.event_title
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating content: {str(e)}")

#  Event Title Improver
@router.post("/improve-title")
async def improve_event_title(request: TitleRequest):
    """
    Improves simple event titles to be more marketing-friendly and attractive.
    Example: "Party Night" → "Ultimate Party Night – Colombo 2026"
    """
    llm = get_llm(temperature=0.9)
    
    prompt = ChatPromptTemplate.from_template(
        """You are an expert event marketer and title strategist.

Given this simple event title: "{current_title}"

Generate 5 improved, marketing-friendly versions that:
- Are catchy and memorable
- Include location or year if appropriate
- Create excitement and intrigue
- Are suitable for social media
- Are between 40-70 characters

Return ONLY a JSON object with this format:
{{
    "original": "{current_title}",
    "suggestions": [
        "Suggestion 1",
        "Suggestion 2",
        "Suggestion 3",
        "Suggestion 4",
        "Suggestion 5"
    ]
}}"""
    )
    
    chain = prompt | llm | StrOutputParser()
    
    try:
        result = chain.invoke({"current_title": request.current_title})
        
        cleaned = result.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.split("```")[1].replace("json", "").strip()
        
        return json.loads(cleaned)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error improving title: {str(e)}")

# Comment Moderation
@router.post("/moderate-comment")
async def moderate_comment(request: CommentModerationRequest):
    """
    AI comment moderation that checks for:
    - Spam content
    - Abusive language
    - Unsafe content
    - Inappropriate material
    """
    llm = get_llm(temperature=0.3) 
    
    prompt = ChatPromptTemplate.from_template(
        """You are a professional content moderator.

Analyze this user comment for safety and appropriateness:
"{comment}"

Check for:
1. Spam or promotional content
2. Abusive, hateful, or offensive language
3. Personal attacks or harassment
4. Unsafe or illegal content
5. Explicit or inappropriate material

Provide a moderation decision in JSON format:
{{
    "approved": true/false,
    "reason": "Brief reason if rejected",
    "severity": "none|low|medium|high",
    "suggestions": ["Any suggestions for improvement"]
}}

Be fair but strict about safety."""
    )
    
    chain = prompt | llm | StrOutputParser()
    
    try:
        result = chain.invoke({"comment": request.comment_text})
        
        cleaned = result.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.split("```")[1].replace("json", "").strip()
        
        moderation_result = json.loads(cleaned)
        return {
            "comment": request.comment_text,
            "moderation": moderation_result
        }
    except Exception as e:
        return {
            "comment": request.comment_text,
            "moderation": {
                "approved": False,
                "reason": "Content could not be verified",
                "severity": "medium"
            }
        }

#Image Prompt Generator 
@router.post("/generate-image-prompt")
async def generate_image_prompt(request: ImagePromptRequest):
    """
    Generates detailed AI image prompts for poster/banner creation.
    Can be used with Midjourney, DALL·E, or similar tools.
    """
    llm = get_llm(temperature=0.85)
    
    prompt = ChatPromptTemplate.from_template(
        """You are an expert AI image prompt engineer and graphic designer.

Create detailed, vivid image prompts for generating event posters using Midjourney or DALL·E.

Event Information:
- Title: {event_title}
- Type: {event_type}
- Location: {location}
- Vibe/Mood: {vibe}

Generate TWO detailed image prompts:

1. A **professional poster design** prompt that includes:
   - Visual style and art direction
   - Color palette recommendations
   - Key visual elements
   - Composition and layout
   - Typography style
   - Mood and atmosphere

2. A **banner/social media** prompt that includes:
   - Platform-specific dimensions consideration
   - Eye-catching visual elements
   - Text overlay placement
   - Engagement factors

Format as JSON:
{{
    "event_title": "{event_title}",
    "poster_prompt": "Detailed prompt for poster...",
    "banner_prompt": "Detailed prompt for banner...",
    "color_palette": ["Color 1", "Color 2", "Color 3"],
    "style_references": ["Reference 1", "Reference 2"]
}}

Make prompts specific, detailed, and optimized for AI image generation."""
    )
    
    chain = prompt | llm | StrOutputParser()
    
    try:
        result = chain.invoke({
            "event_title": request.event_title,
            "event_type": request.event_type,
            "location": request.location,
            "vibe": request.vibe or "exciting and engaging"
        })
        
        cleaned = result.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.split("```")[1].replace("json", "").strip()
        
        return json.loads(cleaned)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating image prompt: {str(e)}")

# Dynamic Poster Generator
@router.post("/generate-poster")
async def generate_poster(request: PosterRequest):
    """
    Dynamically generates a high-quality event poster using Pillow.
    Creates unique backgrounds, patterns, and typography based on event details.
    """
    try:
        # Configuration
        width, height = 800, 1100
        base_dir = Path(__file__).resolve().parent.parent.parent
        upload_dir = base_dir / "uploads" / "event_posters"
        upload_dir.mkdir(parents=True, exist_ok=True)
        
        # 1. Background Generation
        # Choose a color palette based on category or random
        palettes = {
            "CONFERENCE": [(13, 110, 253), (11, 94, 215), (173, 216, 230)], # Blues
            "WORKSHOP": [(25, 135, 84), (20, 108, 67), (144, 238, 144)], # Greens
            "MUSIC": [(220, 53, 69), (187, 45, 59), (255, 182, 193)], # Reds/Pinks
            "MEETUP": [(102, 16, 242), (82, 13, 194), (230, 230, 250)], # Purples
            "SEMINAR": [(255, 193, 7), (255, 160, 0), (255, 253, 208)]  # Yellows/Golds
        }
        
        primary_palette = palettes.get(request.category.upper(), palettes["MEETUP"])
        color1 = primary_palette[0]
        color2 = primary_palette[1]
        
        # Create gradient
        base = Image.new('RGB', (width, height), color1)
        draw = ImageDraw.Draw(base)
        
        for i in range(height):
            # LERP color
            r = int(color1[0] + (color2[0] - color1[0]) * (i / height))
            g = int(color1[1] + (color2[1] - color1[1]) * (i / height))
            b = int(color1[2] + (color2[2] - color1[2]) * (i / height))
            draw.line([(0, i), (width, i)], fill=(r, g, b))
            
        # 2. Add Abstract Patterns
        overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        overlay_draw = ImageDraw.Draw(overlay)
        
        for _ in range(15):
            shape_type = random.choice(['circle', 'rectangle', 'line'])
            x = random.randint(0, width)
            y = random.randint(0, height)
            size = random.randint(50, 400)
            opacity = random.randint(20, 60)
            shape_color = (*random.choice(primary_palette), opacity)
            
            if shape_type == 'circle':
                overlay_draw.ellipse([x, y, x + size, y + size], fill=shape_color)
            elif shape_type == 'rectangle':
                overlay_draw.rectangle([x, y, x + size, y + size], fill=shape_color)
                
        # Blend patterns
        base = base.convert('RGBA')
        base = Image.alpha_composite(base, overlay)
        
        # 3. Add Typography
        draw = ImageDraw.Draw(base)
        
        # Try to load a nice font, fallback to default
        font_paths = [
            "C:/Windows/Fonts/arialbd.ttf", 
            "C:/Windows/Fonts/arial.ttf",
            "C:/Windows/Fonts/segoeuib.ttf",
            "C:/Windows/Fonts/tahoma.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
        ]
        
        title_font = None
        subtitle_font = None
        detail_font = None
        
        for path in font_paths:
            try:
                if os.path.exists(path):
                    title_font = ImageFont.truetype(path, 80)
                    subtitle_font = ImageFont.truetype(path, 40)
                    detail_font = ImageFont.truetype(path, 30)
                    break
            except Exception as e:
                logger.warning(f"Failed to load font {path}: {e}")
                continue
        
        if not title_font:
            # Absolute fallback
            title_font = ImageFont.load_default()
            subtitle_font = ImageFont.load_default()
            detail_font = ImageFont.load_default()
            logger.warning("Using default bitmap font (may look basic)")

        # Custom text drawing helper to handle potential version issues
        def draw_centered_text(draw_obj, text, y, font, fill=(255, 255, 255)):
            try:
                # Try modern way (Pillow 8.0+)
                draw_obj.text((width // 2, y), text, font=font, fill=fill, anchor="mm")
            except:
                # Fallback for older Pillow
                try:
                    w, h = draw_obj.textsize(text, font=font)
                    draw_obj.text(((width - w) // 2, y - h // 2), text, font=font, fill=fill)
                except:
                    # Very basic fallback
                    draw_obj.text((width // 2 - 100, y), text, font=font, fill=fill)

        # Draw Overlay Rectangle for Text Contrast
        text_bg = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        text_bg_draw = ImageDraw.Draw(text_bg)
        text_bg_draw.rectangle([50, height-400, width-50, height-50], fill=(0, 0, 0, 150))
        base = Image.alpha_composite(base, text_bg)
        
        draw = ImageDraw.Draw(base)
        
        # Wrap Title
        def wrap_text(text, font, max_width):
            lines = []
            words = text.split()
            while words:
                line = ''
                while words:
                    test_line = line + words[0] + ' '
                    try:
                        # Modern way
                        w = draw.textlength(test_line, font=font)
                    except:
                        # Fallback
                        try:
                            w, _ = draw.textsize(test_line, font=font)
                        except:
                            w = len(test_line) * 20 # Very rough estimate
                            
                    if w < max_width:
                        line = words.pop(0) + ' '
                    else:
                        break
                        
                if not line and words: # Forced break if single word is too long
                    line = words.pop(0)
                lines.append(line.strip())
            return lines

        title_lines = wrap_text(request.title.upper(), title_font, width - 150)
        
        # Draw Title
        y_text = height - 350
        for line in title_lines:
            draw_centered_text(draw, line, y_text, font=title_font)
            y_text += 90
            
        # Draw Subtitle (Category)
        draw_centered_text(draw, request.category.upper(), height - 120, font=subtitle_font)
        
        # Draw Location/Date if provided
        loc_str = request.location or "VENUE TBA"
        draw_centered_text(draw, loc_str.upper(), height - 80, font=detail_font, fill=(200, 200, 200))

        # 4. Save Image
        unique_id = str(uuid.uuid4())
        filename = f"gen_poster_{unique_id}.png"
        file_path = upload_dir / filename
        
        # Convert back to RGB for saving as PNG/JPG
        final_image = base.convert('RGB')
        final_image.save(file_path)
        
        return {
            "success": True,
            "poster_url": f"/uploads/event_posters/{filename}",
            "filename": filename
        }
        
    except Exception as e:
        logger.error(f"Error generating poster: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
