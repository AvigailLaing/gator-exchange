import requests
import json
import random

categories = ["Electronics", "Textbooks", "Furniture", "Clothing"]

good_reviews = [
    "Works perfectly, thanks!", "Great condition.", "Fast shipping.", 
    "Exactly as described.", "Love it!", "Good price for the quality.",
    "Helpful seller.", "Clean and well-maintained."
]

bad_reviews = [
    "This is a SCAM.", "Item was BROKEN upon arrival.", 
    "Seller was RUDE.", "STOLEN item, do not buy!", 
    "Dangerous wiring, almost caught fire.", "Total rip-off.",
    "Lens is cracked and useless.", "Do not trust this person."
]

test_data = []

for i in range(50):
    if random.random() > 0.2:
        review = {
            "text": random.choice(good_reviews),
            "rating": random.randint(4, 5),
            "category": random.choice(categories)
        }
    else:
        review = {
            "text": random.choice(bad_reviews),
            "rating": random.randint(1, 2),
            "category": random.choice(categories)
        }
    test_data.append(review)

try:
    print(f"Sending {len(test_data)} reviews to the Python Service...")
    
    response = requests.post('http://127.0.0.1:5001/analyze-reviews', json=test_data)
    
    print("\n--- ANALYTICS REPORT ---")
    print(json.dumps(response.json(), indent=2))

except Exception as e:
    print(f"Error: {e}")
    print("Make sure 'review_analytics.py' is running!")