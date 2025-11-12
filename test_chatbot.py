import requests
import json

BASE_URL = "http://127.0.0.1:8000"

print("\n" + "="*70)
print("🏃 TESTING GAIT CHATBOT WITH NATURAL LANGUAGE")
print("="*70 + "\n")

# Test Questions
questions = [
    "What is my step count for today and how far is it from average? Do I need to improve?",
    "How is my walking speed compared to normal? Should I be concerned?",
    "Am I walking too slowly? What can I do to improve?",
    "Give me a summary of my overall gait health right now.",
    "Is my cadence good? How does it compare to what's healthy?",
    "What's my equilibrium score and what does it mean?"
]

for i, question in enumerate(questions, 1):
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"Question {i}: {question}")
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
    
    response = requests.post(
        f"{BASE_URL}/api/chat/",
        json={
            "message": question,
            "conversation_history": []
        }
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"🤖 AI Response:\n{result['response']}\n")
    else:
        print(f"❌ Error: {response.json()}\n")
    
    print()

print("="*70)
print("✅ TESTING COMPLETE!")
print("="*70 + "\n")