import os
import re
from io import BytesIO
from PIL import Image
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_default_api_key():
    """Get the default API key from environment variables."""
    return os.getenv('GOOGLE_API_KEY', '')

def enhance_educational_prompt(prompt: str) -> str:
    """Enhance a prompt for educational topics with specific improvements."""
    
    # Educational topic keywords and their enhancements
    educational_enhancements = {
        'mathematics': {
            'keywords': ['math', 'mathematics', 'algebra', 'geometry', 'calculus', 'trigonometry', 'statistics', 'probability', 'equation', 'formula', 'theorem', 'graph', 'function', 'derivative', 'integral'],
            'enhancement': 'Create a clear, educational illustration showing mathematical concepts with precise diagrams, clean geometric shapes, proper mathematical notation, educational color coding, and visual clarity suitable for learning. Include relevant formulas, graphs, or visual representations. Style: educational textbook illustration, clean and professional.'
        },
        'physics': {
            'keywords': ['physics', 'force', 'energy', 'momentum', 'wave', 'electromagnetic', 'quantum', 'relativity', 'mechanics', 'thermodynamics', 'optics', 'electric', 'magnetic', 'gravity', 'atom', 'particle'],
            'enhancement': 'Create an educational physics illustration with clear scientific accuracy, showing physical phenomena with proper scientific visualization, labeled diagrams, appropriate scale representations, and educational clarity. Include relevant equations, force vectors, or wave patterns. Style: scientific textbook illustration, precise and informative.'
        },
        'chemistry': {
            'keywords': ['chemistry', 'molecule', 'atom', 'element', 'compound', 'reaction', 'bond', 'periodic', 'ion', 'electron', 'proton', 'neutron', 'acid', 'base', 'catalyst', 'organic', 'inorganic'],
            'enhancement': 'Create an educational chemistry illustration with accurate molecular structures, proper chemical notation, clear atomic diagrams, color-coded elements following standard conventions, and precise scientific representation. Include molecular bonds, electron configurations, or reaction mechanisms. Style: scientific educational diagram, clean and accurate.'
        },
        'biology': {
            'keywords': ['biology', 'cell', 'dna', 'gene', 'organism', 'species', 'evolution', 'ecosystem', 'photosynthesis', 'respiration', 'anatomy', 'physiology', 'genetics', 'bacteria', 'virus', 'protein'],
            'enhancement': 'Create an educational biology illustration with accurate anatomical details, proper biological structures, clear cellular components, natural color schemes, and scientific precision. Include labeled parts, biological processes, or anatomical cross-sections. Style: scientific biological illustration, detailed and educational.'
        },
        'science': {
            'keywords': ['science', 'experiment', 'hypothesis', 'theory', 'observation', 'research', 'laboratory', 'scientific method', 'discovery', 'innovation'],
            'enhancement': 'Create an educational science illustration with clear scientific concepts, proper experimental setups, accurate scientific equipment, educational clarity, and inspiring scientific discovery themes. Include laboratory equipment, scientific processes, or discovery moments. Style: educational science textbook, engaging and informative.'
        },
        'social': {
            'keywords': ['history', 'geography', 'culture', 'society', 'civilization', 'government', 'democracy', 'economics', 'politics', 'anthropology', 'sociology', 'archaeology', 'timeline', 'map', 'ancient', 'modern'],
            'enhancement': 'Create an educational social studies illustration with historical accuracy, cultural sensitivity, clear geographical representations, proper historical context, and educational value. Include maps, timelines, cultural artifacts, or historical scenes. Style: educational textbook illustration, informative and culturally appropriate.'
        }
    }
    
    # Convert prompt to lowercase for keyword matching
    prompt_lower = prompt.lower()
    
    # Check which educational topic the prompt relates to
    detected_topic = None
    max_matches = 0
    
    for topic, data in educational_enhancements.items():
        matches = sum(1 for keyword in data['keywords'] if keyword in prompt_lower)
        if matches > max_matches:
            max_matches = matches
            detected_topic = topic
    
    # If we detected an educational topic, enhance the prompt
    if detected_topic and max_matches > 0:
        enhancement = educational_enhancements[detected_topic]['enhancement']
        enhanced_prompt = f"{prompt}. {enhancement}"
        return enhanced_prompt
    
    # If no specific educational topic detected, add general educational enhancement
    general_educational_keywords = ['learn', 'teach', 'education', 'study', 'academic', 'school', 'university', 'student', 'lesson', 'concept']
    if any(keyword in prompt_lower for keyword in general_educational_keywords):
        enhanced_prompt = f"{prompt}. Create an educational illustration that is clear, informative, and suitable for learning. Use clean design, appropriate colors, and visual elements that enhance understanding. Style: educational textbook illustration."
        return enhanced_prompt
    
    # Return original prompt if no educational context detected
    return prompt

def initialize_client(api_key: str):
    """Initialize the GenAI client with the provided API key."""
    try:
        return genai.Client(api_key=api_key)
    except Exception as e:
        raise RuntimeError(f"Failed to initialize GenAI client: {e}")

def generate_image(prompt: str, api_key: str) -> dict:
    """Generate an image from a text prompt using Google's Gemini 2.5 Flash."""
    try:
        # Enhance the prompt for educational topics
        enhanced_prompt = enhance_educational_prompt(prompt)
        
        client = initialize_client(api_key)
        response = client.models.generate_content(
            model="gemini-2.5-flash-image-preview",
            contents=enhanced_prompt,
            config=types.GenerateContentConfig(
                response_modalities=['TEXT', 'IMAGE']
            )
        )
        image = None
        text_response = ""
        for part in response.candidates[0].content.parts:
            if part.text:
                text_response = part.text
            elif part.inline_data:
                image = Image.open(BytesIO(part.inline_data.data))
        if image:
            return {"status": "success", "image": image, "text": text_response, "enhanced_prompt": enhanced_prompt, "original_prompt": prompt}
        else:
            return {"status": "error", "message": "No image data found in the response."}
    except Exception as e:
        return {"status": "error", "message": f"An error occurred during image generation: {str(e)}"}