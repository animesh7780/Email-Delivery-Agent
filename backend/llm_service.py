import google.generativeai as genai
from typing import Dict, List, Optional
import json
from config import settings

genai.configure(api_key=settings.gemini_api_key)


class LLMService:
    def __init__(self):
        self.model = genai.GenerativeModel(settings.gemini_model)
    
    async def categorize_email(self, email_subject: str, email_body: str, custom_prompt: Optional[str] = None) -> Dict:
        """Categorize email using LLM"""
        default_prompt = """Analyze the following email and categorize it.

Email Subject: {subject}
Email Body: {body}

Respond ONLY with a valid JSON object (no markdown, no extra text) with these exact keys:
{{
  "category": "Work|Personal|Promotional|Social|Important|Spam|Newsletter",
  "priority": "High|Medium|Low",
  "sentiment": "Positive|Neutral|Negative",
  "reasoning": "brief explanation"
}}"""
        
        prompt = custom_prompt or default_prompt
        prompt = prompt.format(subject=email_subject, body=email_body)
        
        try:
            response = self.model.generate_content(prompt)
            result = response.text.strip()
            
            # Remove markdown code blocks if present
            if result.startswith("```"):
                result = result.split("```")[1]
                if result.startswith("json"):
                    result = result[4:]
                result = result.strip()
            
            # Try to parse JSON response
            try:
                parsed = json.loads(result)
                return parsed
            except json.JSONDecodeError:
                # If not valid JSON, try to extract info from text
                print(f"Failed to parse JSON, raw response: {result}")
                return {
                    "category": "Uncategorized",
                    "priority": "Medium",
                    "sentiment": "Neutral",
                    "reasoning": result
                }
        except Exception as e:
            print(f"Error in categorize_email: {str(e)}")
            return {
                "category": "Error",
                "priority": "Medium",
                "sentiment": "Neutral",
                "error": str(e)
            }
    
    async def extract_action_items(self, email_subject: str, email_body: str, custom_prompt: Optional[str] = None) -> Dict:
        """Extract action items from email"""
        default_prompt = """Analyze the following email and extract all action items, tasks, or requests.

Email Subject: {subject}
Email Body: {body}

Respond ONLY with a valid JSON object (no markdown, no extra text):
{{
  "has_action_items": true or false,
  "action_items": [
    {{"task": "description", "deadline": "date or null", "priority": "High|Medium|Low"}}
  ],
  "summary": "brief summary"
}}"""
        
        prompt = custom_prompt or default_prompt
        prompt = prompt.format(subject=email_subject, body=email_body)
        
        try:
            response = self.model.generate_content(prompt)
            result = response.text.strip()
            
            # Remove markdown code blocks if present
            if result.startswith("```"):
                result = result.split("```")[1]
                if result.startswith("json"):
                    result = result[4:]
                result = result.strip()
            
            try:
                return json.loads(result)
            except json.JSONDecodeError:
                print(f"Failed to parse JSON for action items, raw response: {result}")
                return {
                    "has_action_items": False,
                    "action_items": [],
                    "summary": result
                }
        except Exception as e:
            print(f"Error in extract_action_items: {str(e)}")
            return {
                "has_action_items": False,
                "action_items": [],
                "error": str(e)
            }
    
    async def generate_draft_reply(self, email_subject: str, email_body: str, tone: str = "professional", 
                                   custom_prompt: Optional[str] = None) -> Dict:
        """Generate a draft reply to an email"""
        default_prompt = """Generate a {tone} reply to the following email.

Email Subject: {subject}
Email Body: {body}

Respond ONLY with a valid JSON object (no markdown, no extra text):
{{
  "subject": "reply subject line",
  "body": "reply email body",
  "key_points": ["point 1", "point 2"]
}}"""
        
        prompt = custom_prompt or default_prompt
        prompt = prompt.format(subject=email_subject, body=email_body, tone=tone)
        
        try:
            response = self.model.generate_content(prompt)
            result = response.text.strip()
            
            # Remove markdown code blocks if present
            if result.startswith("```"):
                result = result.split("```")[1]
                if result.startswith("json"):
                    result = result[4:]
                result = result.strip()
            
            try:
                return json.loads(result)
            except json.JSONDecodeError:
                print(f"Failed to parse JSON for draft, raw response: {result}")
                return {
                    "subject": f"Re: {email_subject}",
                    "body": result,
                    "key_points": []
                }
        except Exception as e:
            print(f"Error in generate_draft_reply: {str(e)}")
            return {
                "subject": f"Re: {email_subject}",
                "body": "Error generating draft.",
                "error": str(e)
            }
    
    async def chat_about_inbox(self, user_message: str, context: Optional[str] = None) -> str:
        """Handle chat interactions about the inbox"""
        prompt = f"""You are an AI email assistant helping users manage their inbox.
You can answer questions about emails, help prioritize tasks, and provide insights about the inbox.

{f'Context: {context}' if context else ''}

User question: {user_message}"""
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error processing chat: {str(e)}"


llm_service = LLMService()
