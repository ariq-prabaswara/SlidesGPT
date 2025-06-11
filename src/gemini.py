import os
import google.generativeai as genai
from dotenv import load_dotenv
from typing import Optional
from .utils import logger

class GeminiService:
    def __init__(self):
        """Initialize the Gemini service with API key"""
        load_dotenv()
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            logger.error("GOOGLE_API_KEY not found in environment variables. Please create a .env file with your API key.")
            raise ValueError("GOOGLE_API_KEY not found in environment variables. Please create a .env file with your API key.")
            
        genai.configure(api_key=api_key)
        
        # List available models
        for model in genai.list_models():
            if 'generateContent' in model.supported_generation_methods:
                logger.info(f"Found model: {model.name}")
        
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        logger.info("Successfully initialized Gemini service")
        
    def process_content(self, content: str) -> str:
        """Process content using Gemini API"""
        try:
            prompt = f"""
            Convert the following text into a presentation format using markdown.
            Follow these specific rules:
            1. Use # for the title slide
            2. Use ## for each slide title
            3. Use - for bullet points
            4. Separate slides with ---
            5. Keep each slide concise (3-5 bullet points max)
            6. Use ** for emphasis
            7. Add a title slide at the beginning
            8. Add a "Thank You" slide at the end
            
            Text to convert:
            {content}
            """
            
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            logger.error(f"Error processing content with Gemini: {str(e)}")
            raise
            
    def validate_response(self, response: str) -> bool:
        """
        Validate the response from Gemini
        
        Args:
            response (str): The response to validate
            
        Returns:
            bool: True if response is valid, False otherwise
        """
        if not response:
            return False
            
        # Check for required markdown elements
        required_elements = ["# ", "## ", "---", "- "]
        return all(element in response for element in required_elements) 