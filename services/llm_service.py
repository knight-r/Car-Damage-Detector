import json
import re
from typing import List, Dict, Any
from openai import OpenAI
from config import config
from prompts.damage_analysis_prompt import get_damage_prompt

class LLMService:
    def __init__(self):
        if not config.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        self.client = OpenAI(api_key=config.OPENAI_API_KEY)
    
    def _extract_json(self, text: str) -> Dict[Any, Any]:
        """Extract JSON from text that might contain markdown or other content"""
        # Try to find JSON in markdown code blocks
        json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', text, re.DOTALL)
        if json_match:
            text = json_match.group(1)
        
        # Try to find JSON object directly
        json_match = re.search(r'\{.*\}', text, re.DOTALL)
        if json_match:
            text = json_match.group(0)
        
        try:
            return json.loads(text)
        except json.JSONDecodeError as e:
            print(f"Failed to parse JSON: {e}")
            print(f"Raw text: {text}")
            return {"damages": [], "error": "Failed to parse LLM response"}
    
    async def analyze_with_openai(
        self,
        base64_images: List[str],
        image_formats: List[str],
        custom_prompt: str = None
    ) -> Dict[Any, Any]:
        """Analyze car damage using OpenAI Vision API"""
        
        # Prepare image content
        image_content = []
        for base64_img, img_format in zip(base64_images, image_formats):
            image_content.append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/{img_format};base64,{base64_img}",
                    "detail": "high"  # Use high detail for better damage detection
                }
            })
        
        # Prepare messages
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": get_damage_prompt(custom_prompt)},
                    *image_content
                ]
            }
        ]
        
        try:
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model=config.OPENAI_MODEL,
                messages=messages,
                max_tokens=2000,
                temperature=0.1
            )
            
            result_text = response.choices[0].message.content
            return self._extract_json(result_text)
        
        except Exception as e:
            print(f"OpenAI API Error: {str(e)}")
            return {
                "damages": [],
                "error": f"OpenAI API Error: {str(e)}"
            }
    
    async def analyze_car_damage(
        self,
        images_data: List[tuple],  # List of (filename, base64, format)
        custom_prompt: str = None
    ) -> List[Dict[Any, Any]]:
        """Analyze car damage for multiple images"""
        results = []
        
        for filename, base64_img, img_format in images_data:
            try:
                analysis = await self.analyze_with_openai(
                    [base64_img], [img_format], custom_prompt
                )
                
                # Add image name to result
                analysis["image_name"] = filename
                
                # Calculate overall severity
                if analysis.get("damages"):
                    damages = analysis["damages"]
                    avg_severity = sum(d.get("severity", 0) for d in damages) / len(damages)
                    if avg_severity <= 2:
                        overall = "minor"
                    elif avg_severity <= 3.5:
                        overall = "moderate"
                    else:
                        overall = "severe"
                    
                    analysis["total_damages"] = len(damages)
                    analysis["overall_severity"] = overall
                else:
                    analysis["total_damages"] = 0
                    analysis["overall_severity"] = "none"
                
                results.append(analysis)
                
            except Exception as e:
                results.append({
                    "image_name": filename,
                    "damages": [],
                    "total_damages": 0,
                    "overall_severity": "error",
                    "error": str(e)
                })
        
        return results

# Create singleton instance
llm_service = LLMService()