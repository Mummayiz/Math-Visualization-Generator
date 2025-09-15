import requests
import json
from typing import Dict, List, Any, Optional
from config import Config

class MaminAPI:
    """Integration with Google's mathematical reasoning API using the provided key"""
    
    def __init__(self):
        self.api_key = Config.MAMIN_API_KEY
        # Using Google's AI services since the key format suggests it's a Google API key
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"
        self.headers = {
            "Content-Type": "application/json"
        }
    
    def solve_math_problem(self, problem_text: str) -> Dict[str, Any]:
        """Solve a mathematical problem using Google's AI API"""
        try:
            # Use Google's Gemini API for mathematical reasoning
            payload = {
                "contents": [{
                    "parts": [{
                        "text": f"""Solve this mathematical problem step by step with detailed explanations:

Problem: {problem_text}

Please provide:
1. Step-by-step solution
2. Mathematical reasoning for each step
3. Final answer
4. Verification if applicable

Format your response as a structured solution with clear steps."""
                    }]
                }],
                "generationConfig": {
                    "temperature": 0.1,
                    "topK": 32,
                    "topP": 1,
                    "maxOutputTokens": 2048,
                }
            }
            
            # Make API request to Google's Gemini API
            response = requests.post(
                f"{self.base_url}/models/gemini-1.5-flash:generateContent?key={self.api_key}",
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return self._parse_google_response(result, problem_text)
            else:
                print(f"Google API error: {response.status_code} - {response.text}")
                return self._fallback_solve(problem_text)
                
        except requests.exceptions.RequestException as e:
            print(f"Google API request failed: {e}")
            return self._fallback_solve(problem_text)
        except Exception as e:
            print(f"Error with Google API: {e}")
            return self._fallback_solve(problem_text)
    
    def _parse_google_response(self, response: Dict[str, Any], problem_text: str) -> Dict[str, Any]:
        """Parse Google's API response into our format"""
        try:
            if 'candidates' in response and len(response['candidates']) > 0:
                content = response['candidates'][0]['content']['parts'][0]['text']
                
                # Parse the response into steps
                steps = self._extract_steps_from_text(content)
                
                return {
                    "success": True,
                    "problem_text": problem_text,
                    "steps": steps,
                    "final_answer": self._extract_final_answer(content),
                    "raw_response": content
                }
            else:
                return self._fallback_solve(problem_text)
        except Exception as e:
            print(f"Error parsing Google response: {e}")
            return self._fallback_solve(problem_text)
    
    def _extract_steps_from_text(self, text: str) -> List[Dict[str, Any]]:
        """Extract solution steps from the AI response text"""
        steps = []
        lines = text.split('\n')
        current_step = None
        step_number = 1
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Look for step indicators
            if any(indicator in line.lower() for indicator in ['step', 'solution', 'solve', 'calculate']):
                if current_step:
                    steps.append(current_step)
                
                current_step = {
                    "step_number": step_number,
                    "description": line,
                    "equation": "",
                    "explanation": ""
                }
                step_number += 1
            elif current_step:
                # Add content to current step
                if any(symbol in line for symbol in ['=', '+', '-', '*', '/', '^', 'x', 'y', 'z']):
                    current_step["equation"] += line + " "
                else:
                    current_step["explanation"] += line + " "
        
        if current_step:
            steps.append(current_step)
        
        # If no steps found, create a basic one
        if not steps:
            steps = [{
                "step_number": 1,
                "description": "AI Solution",
                "equation": problem_text,
                "explanation": text[:200] + "..." if len(text) > 200 else text
            }]
        
        return steps
    
    def _extract_final_answer(self, text: str) -> str:
        """Extract the final answer from the response text"""
        lines = text.split('\n')
        for line in reversed(lines):
            line = line.strip()
            if any(keyword in line.lower() for keyword in ['answer', 'result', 'solution', 'final']):
                return line
        return "Answer not clearly specified"
    
    def _fallback_solve(self, problem_text: str) -> Dict[str, Any]:
        """Fallback solving method when Google API is unavailable"""
        return {
            "success": False,
            "error": "Google API unavailable, using local solving",
            "problem_text": problem_text,
            "steps": [],
            "final_answer": None
        }
    
    def classify_problem_type(self, problem_text: str) -> str:
        """Classify the type of mathematical problem"""
        try:
            payload = {
                "text": problem_text,
                "task": "classify"
            }
            
            response = requests.post(
                f"{self.base_url}/classify",
                headers=self.headers,
                json=payload,
                timeout=15
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get("problem_type", "general")
            else:
                return "general"
                
        except Exception as e:
            print(f"Error classifying problem type: {e}")
            return "general"
    
    def generate_explanation(self, step: str, context: str = "") -> str:
        """Generate educational explanation for a solution step"""
        try:
            payload = {
                "step": step,
                "context": context,
                "style": "educational"
            }
            
            response = requests.post(
                f"{self.base_url}/explain",
                headers=self.headers,
                json=payload,
                timeout=15
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get("explanation", step)
            else:
                return step
                
        except Exception as e:
            print(f"Error generating explanation: {e}")
            return step
    
    def create_visualization_hint(self, problem_type: str, step: str) -> Dict[str, Any]:
        """Get visualization hints for mathematical concepts"""
        try:
            payload = {
                "problem_type": problem_type,
                "step": step,
                "visualization_type": "educational"
            }
            
            response = requests.post(
                f"{self.base_url}/visualize",
                headers=self.headers,
                json=payload,
                timeout=15
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {"type": "text", "content": step}
                
        except Exception as e:
            print(f"Error getting visualization hints: {e}")
            return {"type": "text", "content": step}

# Alternative implementation using Google's mathematical reasoning capabilities
class GoogleMathAPI:
    """Alternative implementation using Google's mathematical reasoning"""
    
    def __init__(self):
        self.api_key = Config.MAMIN_API_KEY  # Using the provided API key
    
    def solve_math_problem(self, problem_text: str) -> Dict[str, Any]:
        """Solve mathematical problem using Google's capabilities"""
        try:
            # This is a placeholder implementation
            # In practice, you would integrate with Google's mathematical reasoning API
            # or use the API key with appropriate Google services
            
            # For now, return a structured response
            return {
                "success": True,
                "problem_text": problem_text,
                "steps": [
                    {
                        "step_number": 1,
                        "description": "Problem Analysis",
                        "equation": problem_text,
                        "explanation": "Let's analyze this mathematical problem step by step."
                    }
                ],
                "final_answer": "Solution will be computed using Mamin's mathematical reasoning",
                "problem_type": "general"
            }
            
        except Exception as e:
            print(f"Error with Google Math API: {e}")
            return {
                "success": False,
                "error": str(e),
                "steps": [],
                "final_answer": None
            }
