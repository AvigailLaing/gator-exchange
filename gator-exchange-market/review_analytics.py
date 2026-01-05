import pandas as pd
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/analyze-reviews', methods=['POST'])
def analyze_reviews():
    data = request.get_json()
    #We get a list like text: rating: category:
    #Then we load the JSON into a Pandas DataFrame
    df = pd.DataFrame(data)

    #Then we make sure each entry has all required columns
    required_cols = ['text', 'rating', 'category']
    if not all(col in df.columns for col in required_cols):
        return jsonify({"error": f"Missing columns. Required: {required_cols}"}), 400

    #Now we use vectorized text analysis to scan for all bad words at once instead of iterating with a for loop
    danger_pattern = "scam|broken|rude|stolen|dangerous"
    df['is_flagged'] = df['text'].str.contains(danger_pattern, case=False, na=False)

    # Then we use aggregation to group the reviews by category then come up with an average
    #rating and total flags for each category
 
    category_report = df.groupby('category').agg({
        'rating': 'mean',          # Average rating
        'is_flagged': 'sum',       # Total flags
        'text': 'count'            # Total volume
    }).rename(columns={'text': 'total_reviews', 'is_flagged': 'flagged_count'})
    
    #Then we just round the ratings 
    category_report['rating'] = category_report['rating'].round(2)
    
    #Then we create a flagged_reviews dataFrame to get the reviews to moderate
    flagged_reviews = df[df['is_flagged'] == True]

    return jsonify({
        "market_health_report": category_report.to_dict(orient='index'),
        "moderation_queue": flagged_reviews.to_dict(orient='records')
    })

if __name__ == '__main__':
    #5001 avoids conflicts with Node app on 5000
    app.run(port=5001)