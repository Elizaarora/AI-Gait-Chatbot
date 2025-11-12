import requests

FIREBASE_URL = "https://gaitanalyzer-c23c7-default-rtdb.firebaseio.com"

print("Testing Firebase Connection...\n")

# Test 1: Get gait data
print("1. Fetching gait data...")
response = requests.get(f"{FIREBASE_URL}/gaitData.json")
print(f"Status Code: {response.status_code}")

if response.status_code == 200:
    data = response.json()
    print(f"✅ SUCCESS! Found {len(data)} gait records")
    
    # Get latest
    latest_key = list(data.keys())[-1]
    latest = data[latest_key]
    print(f"\nLatest Data:")
    print(f"  Steps: {latest.get('steps')}")
    print(f"  Cadence: {latest.get('cadence')}")
    print(f"  Walking Speed: {latest.get('walkingSpeed')}")
else:
    print(f"❌ FAILED! Error: {response.status_code}")
    print(f"Response: {response.text}")

# Test 2: Get averages
print("\n2. Fetching average scores...")
response = requests.get(f"{FIREBASE_URL}/average_scores.json")
print(f"Status Code: {response.status_code}")

if response.status_code == 200:
    data = response.json()
    print(f"✅ SUCCESS!")
    print(f"  Average Score: {data.get('avgGaitScoreLast20')}")
    print(f"  Classification: {data.get('avgClassificationLast20')}")
else:
    print(f"❌ FAILED! Error: {response.status_code}")
    print(f"Response: {response.text}")