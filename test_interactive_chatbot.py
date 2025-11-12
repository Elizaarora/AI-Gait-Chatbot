import requests
import json

BASE_URL = "http://127.0.0.1:8000"

print("\n" + "="*80)
print("🤖 TESTING FULLY INTERACTIVE GAIT CHATBOT")
print("="*80 + "\n")

# Simulate a realistic conversation
conversation = []

test_conversations = [
    {
        "title": "📊 Basic Data Query",
        "questions": [
            "What's my step count for today?",
            "How does that compare to my average?",
        ]
    },
    {
        "title": "🏃 Performance Analysis",
        "questions": [
            "Is my walking speed normal?",
            "What about my cadence? Is it good?",
            "How's my overall gait health?",
        ]
    },
    {
        "title": "⚖️ Body-Specific Questions",
        "questions": [
            "I'm 5'10\" and weigh 180 lbs. Is my step count normal for my size?",
            "Should someone my height have a longer stride?",
        ]
    },
    {
        "title": "💪 Improvement & Advice",
        "questions": [
            "How can I improve my balance?",
            "What exercises would help my gait?",
            "Am I walking too slowly? What should I do?",
        ]
    },
    {
        "title": "🧠 Knowledge-Based Questions",
        "questions": [
            "What does equilibrium score mean?",
            "Why is cadence important for health?",
            "What's a healthy walking speed for my age group? I'm 35.",
        ]
    },
    {
        "title": "🔍 Detailed Analysis",
        "questions": [
            "Give me a complete summary of my gait health right now",
            "Should I be concerned about anything in my metrics?",
        ]
    }
]

for section in test_conversations:
    print("\n" + "━"*80)
    print(f"  {section['title']}")
    print("━"*80)
    
    for question in section['questions']:
        print(f"\n👤 USER: {question}")
        print("-" * 80)
        
        try:
            response = requests.post(
                f"{BASE_URL}/api/chat/",
                json={
                    "message": question,
                    "conversation_history": conversation[-4:]  # Last 4 messages for context
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                ai_response = result['response']
                
                print(f"🤖 ASSISTANT: {ai_response}\n")
                
                # Add to conversation history
                conversation.append({"role": "user", "content": question})
                conversation.append({"role": "assistant", "content": ai_response})
                
            else:
                print(f"❌ Error {response.status_code}: {response.text}\n")
                
        except Exception as e:
            print(f"❌ Request failed: {e}\n")
    
    print()

print("="*80)
print("✅ INTERACTIVE TESTING COMPLETE!")
print(f"📝 Total conversation length: {len(conversation)} messages")
print("="*80 + "\n") 



