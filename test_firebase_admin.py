from app.services.firebase_service import FirebaseService

print("="*70)
print("Testing Firebase Admin SDK Connection")
print("="*70 + "\n")

try:
    service = FirebaseService()
    
    print("\n1. Testing Latest Gait Data...")
    print("-" * 50)
    current = service.get_latest_gait_data()
    
    if current:
        print("\n✅ SUCCESS! Current Data:")
        for key, value in current.items():
            if isinstance(value, (int, float)):
                print(f"   {key}: {value:.2f}" if isinstance(value, float) else f"   {key}: {value}")
            else:
                print(f"   {key}: {value}")
    else:
        print("\n❌ FAILED to get current data")
    
    print("\n2. Testing Average Scores...")
    print("-" * 50)
    averages = service.get_average_scores()
    
    if averages:
        print("\n✅ SUCCESS! Average Data:")
        print(f"   Avg Score: {averages.get('avgGaitScoreLast20', 'N/A')}")
        print(f"   Classification: {averages.get('avgClassificationLast20', 'N/A')}")
    else:
        print("\n❌ FAILED to get averages")
    
    print("\n3. Testing Complete Data Fetch...")
    print("-" * 50)
    all_data = service.get_all_data()
    
    print("\n" + "="*70)
    if all_data['current'] and all_data['averages']:
        print("✅ Firebase connection FULLY working!")
        print("✅ Ready for chatbot integration!")
    else:
        print("⚠️ Partial data available")
    print("="*70)
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()