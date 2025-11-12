import google.generativeai as genai
from typing import List
from app.config.settings import get_settings
from app.models.schemas import Message

settings = get_settings()

class GeminiService:
    """Service to interact with Google Gemini AI"""
    
    def __init__(self):
        genai.configure(api_key=settings.gemini_api_key)
        self.model = genai.GenerativeModel('gemini-1.5-pro-latest')
    
    def create_context_prompt(self, gait_data: dict) -> str:
        """Create a rich context with gait data for Gemini"""
        
        current = gait_data.get("current")
        averages = gait_data.get("averages")
        
        # Handle missing data
        if not current or current is None:
            return """You are a gait analysis assistant. 
            
IMPORTANT: Currently, no real-time gait data is available from the sensors. 
This could mean:
1. The sensors are not connected
2. The user hasn't started walking yet
3. There's a connection issue with Firebase

Please politely inform the user that no data is currently available and suggest:
- Checking if the sensors are connected and powered on
- Starting to walk if they haven't already
- Waiting a few moments for the system to sync

Be friendly and helpful!"""
        
        # Safe formatting
        def fmt(value, decimals=2):
            try:
                return f"{float(value):.{decimals}f}" if value is not None else "N/A"
            except:
                return "N/A"
        
        # Extract metrics
        steps = current.get('steps', 0)
        cadence = current.get('cadence', 0)
        walking_speed = current.get('walkingSpeed', 0)
        stride_length = current.get('strideLength', 0)
        equilibrium = current.get('equilibriumScore', 0)
        postural_sway = current.get('posturalSway', 0)
        
        # Calculate status
        cadence_status = "below normal" if cadence < 100 else ("optimal" if cadence <= 120 else "above normal")
        speed_status = "below normal" if walking_speed < 1.2 else ("optimal" if walking_speed <= 1.4 else "above normal")
        
        # Get averages
        avg_score = averages.get('avgGaitScoreLast20', 0) if averages else 0
        classification = averages.get('avgClassificationLast20', 'Unknown') if averages else 'Unknown'
        
        context = f"""You are a friendly, knowledgeable gait analysis AI assistant. You're analyzing LIVE, REAL-TIME data from wearable sensors.

🏃 CURRENT LIVE METRICS (Right Now):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- Steps Today: {steps} steps
- Cadence: {fmt(cadence)} steps/min ({cadence_status})
- Walking Speed: {fmt(walking_speed)} m/s ({speed_status})
- Stride Length: {fmt(stride_length)} meters
- Step Width: {fmt(current.get('stepWidth'))} meters
- Equilibrium Score: {fmt(equilibrium)}/1.0 (balance indicator)
- Postural Sway: {fmt(postural_sway)}° (stability indicator)
- Frequency: {fmt(current.get('frequency'))} Hz
- Gait Phase: {current.get('gaitCyclePhaseMean', 'N/A')}

📊 YOUR HISTORICAL PERFORMANCE (Last 20 sessions):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- Average Gait Score: {fmt(avg_score)}/100
- Health Classification: {classification}

📋 HEALTHY ADULT REFERENCE RANGES:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- Cadence: 100-120 steps/min ✓
- Walking Speed: 1.2-1.4 m/s ✓
- Stride Length: 1.2-1.5 m ✓
- Equilibrium: 0.7-1.0 ✓
- Postural Sway: <5° ✓

🎯 HOW TO RESPOND:
1. Be conversational and warm - talk like a knowledgeable friend
2. Always reference the ACTUAL NUMBERS from the live data above
3. When user asks about "today" → use steps: {steps}
4. When comparing to average → use score: {fmt(avg_score)}
5. Give specific, actionable advice based on their metrics
6. Be encouraging! Celebrate good metrics and gently suggest improvements
7. Use emojis occasionally to be friendly 😊
8. Keep responses 3-5 sentences unless they ask for details
9. Compare their values to the reference ranges I provided
10. Never make medical diagnoses - suggest consulting professionals if concerned

EXAMPLE GOOD RESPONSE:
"Your step count today is {steps} steps. Your average gait score is {fmt(avg_score)}/100, which puts you in the '{classification}' category. Your cadence of {fmt(cadence)} steps/min is {cadence_status} - {'great work!' if cadence >= 100 else 'try to increase it to 100-120 for optimal gait'}. Your walking speed is {fmt(walking_speed)} m/s, which is {speed_status}. {'Keep it up!' if walking_speed >= 1.2 else 'Consider picking up the pace slightly to reach 1.2-1.4 m/s.'}"

Remember: Use REAL data, be specific, be helpful, be encouraging!"""

        return context
    
    def generate_response(
        self, 
        user_message: str, 
        gait_data: dict,
        conversation_history: List[Message] = None
    ) -> str:
        """Generate natural language response using Gemini AI"""
        
        try:
            # Build context
            context = self.create_context_prompt(gait_data)
            
            # Build conversation history
            history_text = ""
            if conversation_history and len(conversation_history) > 0:
                for msg in conversation_history[-5:]:
                    history_text += f"\n{msg.role.upper()}: {msg.content}"
            
            # Create full prompt
            full_prompt = f"""{context}

{history_text if history_text else ''}

USER: {user_message}

ASSISTANT:"""
            
            print(f"\n🤖 Sending to Gemini AI...")
            
            # Generate response
            response = self.model.generate_content(full_prompt)
            
            if response and hasattr(response, 'text') and response.text:
                print(f"✅ Got response from Gemini!")
                return response.text.strip()
            else:
                print(f"⚠️ Empty response from Gemini")
                return "I received your question but couldn't generate a response. Could you rephrase it?"
            
        except Exception as e:
            print(f"❌ Gemini API Error: {e}")
            return f"I apologize, I encountered an error: {str(e)}. Please make sure your Gemini API key is valid."