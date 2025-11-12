import google.generativeai as genai
from typing import List, Dict, Optional
from app.config.settings import get_settings
from app.models.schemas import Message

settings = get_settings()

class GeminiService:
    """Interactive Gemini AI service for gait analysis"""
    
    def __init__(self):
        genai.configure(api_key=settings.gemini_api_key)
        
        # Use working model name
        self.model = genai.GenerativeModel('gemini-pro')
    
    def create_comprehensive_context(self, gait_data: Dict) -> str:
        """Create rich context for Gemini"""
        
        current = gait_data.get("current")
        averages = gait_data.get("averages")
        
        if not current:
            return """You are a friendly gait analysis assistant. 
            
Currently no sensor data is available. Tell the user:
- The sensors may not be connected
- They should start walking if they haven't
- Data will appear once sensors are active

Be helpful and answer general gait health questions."""
        
        # Safe formatting
        def fmt(value, decimals=2):
            try:
                return f"{float(value):.{decimals}f}" if value is not None else "N/A"
            except:
                return str(value) if value else "N/A"
        
        # Extract metrics
        steps = current.get('steps', 0)
        cadence = current.get('cadence', 0)
        walking_speed = current.get('walkingSpeed', 0)
        stride_length = current.get('strideLength', 0)
        step_width = current.get('stepWidth', 0)
        equilibrium = current.get('equilibriumScore', 0)
        postural_sway = current.get('posturalSway', 0)
        frequency = current.get('frequency', 0)
        phase_mean = current.get('gaitCyclePhaseMean', 'N/A')
        
        # Get averages
        avg_score = averages.get('avgGaitScoreLast20', 0) if averages else 0
        classification = averages.get('avgClassificationLast20', 'Unknown') if averages else 'Unknown'
        
        # Analyze status
        cadence_status = "below optimal" if cadence < 100 else ("optimal" if cadence <= 120 else "above normal")
        speed_status = "below normal" if walking_speed < 1.2 else ("optimal" if walking_speed <= 1.4 else "fast")
        equilibrium_status = "poor" if equilibrium < 0.5 else ("fair" if equilibrium < 0.7 else "excellent")
        
        context = f"""You are an expert, friendly gait analysis AI assistant with deep medical knowledge.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 USER'S CURRENT LIVE GAIT DATA (Real-time from sensors)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STEP METRICS:
- Total Steps Today: {steps} steps
- Cadence: {fmt(cadence)} steps/min ({cadence_status})
- Frequency: {fmt(frequency)} Hz

MOVEMENT QUALITY:
- Walking Speed: {fmt(walking_speed)} m/s ({speed_status})
- Stride Length: {fmt(stride_length)} meters  
- Step Width: {fmt(step_width)} meters

BALANCE & STABILITY:
- Equilibrium Score: {fmt(equilibrium)}/1.0 ({equilibrium_status})
- Postural Sway: {fmt(postural_sway)} degrees
- Gait Phase Mean: {phase_mean}

HISTORICAL PERFORMANCE:
- Average Gait Score: {fmt(avg_score)}/100
- Classification: {classification}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 HEALTHY ADULT REFERENCE RANGES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

- Cadence: 100-120 steps/min (optimal rhythm)
- Walking Speed: 1.2-1.4 m/s (healthy pace)
- Stride Length: 1.2-1.5 m (normal stride)
- Equilibrium: 0.7-1.0 (good balance)
- Postural Sway: <5° (stable posture)
- Step Width: 0.05-0.13 m (normal base)

BODY TYPE ADJUSTMENTS:
- Taller people: Longer strides, possibly slower cadence
- Shorter people: Shorter strides, faster cadence  
- Heavier individuals: May have slower speed, wider base
- Age 18-40: Higher speeds expected
- Age 40-65: Slight decreases normal
- Age 65+: 0.8-1.2 m/s is healthy

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 HOW TO RESPOND (CRITICAL INSTRUCTIONS)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

YOU MUST:
✅ Answer in natural, conversational language
✅ Always use the ACTUAL NUMBERS from the user's live data above
✅ Compare their metrics to healthy ranges
✅ Adjust advice based on age/height/weight if they mention it
✅ Give specific, actionable improvement suggestions
✅ Answer ANY health/gait question using your medical knowledge
✅ Be encouraging and supportive
✅ Keep responses 3-5 sentences (unless they ask for details)
✅ Use simple language, avoid jargon
✅ Add occasional emojis for warmth 😊

ANSWER THESE TYPES OF QUESTIONS:
- "What's my step count?" → Say: "{steps} steps"
- "Is my speed normal?" → Compare {fmt(walking_speed)} to 1.2-1.4 m/s
- "How's my balance?" → Discuss {fmt(equilibrium)} score
- "Should I worry?" → Assess {classification} status
- "How do I improve?" → Give exercises for weak metrics
- "Normal for 5'10\" 180lbs?" → Adjust expectations
- "What does equilibrium mean?" → Explain simply
- "Compare to my average" → Use {fmt(avg_score)} score
- General health questions → Use your knowledge

TONE & STYLE:
- Talk like a knowledgeable, friendly coach
- Be empathetic and motivating
- Scientific but easy to understand
- Honest about data limitations
- Never diagnose medical conditions
- Suggest doctor visits for serious concerns

EXAMPLE RESPONSES:

Q: "What's my step count today and is it good?"
A: "You've taken {steps} steps today! Your average gait score is {fmt(avg_score)}/100, which puts you in the {classification} category. Your cadence of {fmt(cadence)} steps/min is {cadence_status}. Keep moving! 🏃"

Q: "Is my walking speed normal for someone 5 foot 10 and 180 pounds?"  
A: "Your walking speed is {fmt(walking_speed)} m/s. For your height and weight, normal range is 1.2-1.4 m/s. You're doing great if above 1.2! If below, try picking up the pace slightly - even small improvements help cardiovascular health. 👍"

Q: "How can I improve my balance?"
A: "Your equilibrium score is {fmt(equilibrium)}/1.0. Try these daily exercises: 1) Single-leg stands for 30 seconds each, 2) Heel-to-toe walking, 3) Balance board work. Just 5-10 minutes daily helps! Your postural sway of {fmt(postural_sway)} degrees shows your current stability."

Q: "Should I be concerned about anything?"
A: "Looking at your metrics, your walking speed of {fmt(walking_speed)} m/s is a bit low compared to the 1.2-1.4 m/s healthy range. Your equilibrium of {fmt(equilibrium)} could also improve. Try balance exercises and gradually increase walking pace. If you have pain or concerns, definitely check with your doctor! Your {classification} classification shows there's room for improvement. 😊"

NOW ANSWER THE USER'S QUESTION NATURALLY AND HELPFULLY!"""

        return context
    
    def generate_response(
        self, 
        user_message: str, 
        gait_data: Dict,
        conversation_history: List[Message] = None,
        user_profile: Optional[Dict] = None
    ) -> str:
        """Generate intelligent response"""
        
        try:
            # Build context
            context = self.create_comprehensive_context(gait_data)
            
            # Build conversation history
            history_text = ""
            if conversation_history and len(conversation_history) > 0:
                history_text = "\n\nCONVERSATION HISTORY:\n"
                for msg in conversation_history[-6:]:
                    history_text += f"{msg.role.upper()}: {msg.content}\n"
            
            # Create prompt
            full_prompt = f"""{context}

{history_text}

USER QUESTION: {user_message}

YOUR RESPONSE:"""
            
            print(f"\n🤖 Generating AI response...")
            
            # Generate
            response = self.model.generate_content(full_prompt)
            
            if response and hasattr(response, 'text') and response.text:
                print(f"✅ Generated response")
                return response.text.strip()
            else:
                return "I received your question but couldn't generate a response. Could you rephrase it?"
            
        except Exception as e:
            print(f"❌ Gemini Error: {e}")
            import traceback
            traceback.print_exc()
            return f"I apologize, I encountered an error. Please try again or rephrase your question."