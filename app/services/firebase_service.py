import firebase_admin
from firebase_admin import credentials, db
from typing import Dict, Optional
from app.config.settings import get_settings
import os

settings = get_settings()

class FirebaseService:
    """Service to fetch gait data from Firebase Realtime Database using Admin SDK"""
    
    def __init__(self):
        # Initialize Firebase Admin SDK only once
        if not firebase_admin._apps:
            try:
                service_account_path = settings.firebase_service_account
                
                if not os.path.exists(service_account_path):
                    print(f"❌ Service account file not found: {service_account_path}")
                    raise FileNotFoundError(f"Firebase service account file not found at {service_account_path}")
                
                cred = credentials.Certificate(service_account_path)
                firebase_admin.initialize_app(cred, {
                    'databaseURL': settings.firebase_db_url
                })
                print("✅ Firebase Admin SDK initialized successfully!")
            except Exception as e:
                print(f"❌ Error initializing Firebase: {e}")
                raise
    
    def get_latest_gait_data(self) -> Optional[Dict]:
        """Fetch the latest gait data from Firebase"""
        try:
            print("🔍 Fetching gait data from Firebase...")
            
            # Reference to gaitData
            ref = db.reference('gaitData')
            data = ref.get()
            
            if not data or not isinstance(data, dict):
                print("❌ No gait data found in Firebase")
                return None
            
            print(f"📦 Found {len(data)} items in gaitData")
            
            # Filter out 'average_scores' and get actual gait entries
            gait_entries = {k: v for k, v in data.items() if k != 'average_scores' and isinstance(v, dict)}
            
            if not gait_entries:
                print("❌ No valid gait entries found")
                return None
            
            # Get the latest entry (last key)
            latest_key = list(gait_entries.keys())[-1]
            latest_data = gait_entries[latest_key]
            
            print(f"✅ Got latest gait data (key: {latest_key})")
            print(f"   Steps: {latest_data.get('steps', 'N/A')}")
            print(f"   Cadence: {latest_data.get('cadence', 'N/A')}")
            print(f"   Walking Speed: {latest_data.get('walkingSpeed', 'N/A')}")
            
            return latest_data
            
        except Exception as e:
            print(f"❌ Error fetching gait data: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def get_average_scores(self) -> Optional[Dict]:
        """Fetch average scores from Firebase"""
        try:
            print("🔍 Fetching average scores from Firebase...")
            
            # Try the nested path first (inside gaitData)
            ref = db.reference('gaitData/average_scores')
            data = ref.get()
            
            if data and isinstance(data, dict):
                print(f"✅ Found average scores in gaitData/average_scores")
                print(f"   Keys found: {list(data.keys())}")
                
                # Extract the scores
                result = {
                    'avgGaitScoreLast20': data.get('avgGaitScoreLast20') or data.get('avgGaitScoreLast100', 0),
                    'avgClassificationLast20': data.get('avgClassificationLast20', 'Unknown')
                }
                
                print(f"   Average Score: {result['avgGaitScoreLast20']}")
                print(f"   Classification: {result['avgClassificationLast20']}")
                
                return result
            
            # Try root level as fallback
            ref = db.reference('average_scores')
            data = ref.get()
            
            if data and isinstance(data, dict):
                print(f"✅ Found average scores at root level")
                return {
                    'avgGaitScoreLast20': data.get('avgGaitScoreLast20') or data.get('avgGaitScoreLast100', 0),
                    'avgClassificationLast20': data.get('avgClassificationLast20', 'Unknown')
                }
            
            print("⚠️ No average scores found, using defaults")
            return {
                'avgGaitScoreLast20': 0,
                'avgClassificationLast20': 'Unknown'
            }
            
        except Exception as e:
            print(f"❌ Error fetching average scores: {e}")
            import traceback
            traceback.print_exc()
            return {
                'avgGaitScoreLast20': 0,
                'avgClassificationLast20': 'Unknown'
            }
    
    def get_all_data(self) -> Dict:
        """Get both current and average data"""
        current = self.get_latest_gait_data()
        averages = self.get_average_scores()
        
        result = {
            "current": current,
            "averages": averages
        }
        
        print(f"\n📊 Firebase Data Summary:")
        print(f"   Current data: {'✅ Available' if current else '❌ Missing'}")
        print(f"   Average data: {'✅ Available' if averages else '❌ Missing'}\n")
        
        return result