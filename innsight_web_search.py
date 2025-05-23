from openai import OpenAI
from dotenv import load_dotenv
from flask_cors import CORS
import os
from flask import Flask, request, jsonify

# Load environment variables 
load_dotenv()
key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=key)

app = Flask(__name__)
CORS(app)

hotel_name = 'Red Rhino, Whitefield, Bangalore'

@app.route('/', methods=['POST'])
def index():
    completion = client.chat.completions.create(
        model="gpt-4o-mini-search-preview",
        messages=[
            {
                "role": "user",
                "content": f'''
                Fetch me 10 recent reviews from all over internet for {hotel_name} hotel. 
                Try and collect the recent reviews and all the details mentioned below. 
                {{"reviewer_name":"Vanessa",
                "review":"Nice, stay",
                "review_date":"may 25, 2025",
                "source":"https://www.makemytrip.com/hotels/lemon_tree_hotel_whitefield-details-bangalore.html",
                "sentiment_score":"score between 0-1"}}''',
            }
        ],
    )
    response = completion.choices[0].message.content
    return jsonify({"answer": response})

reviews_list_2 = ['Red Rhino, Bangalore']
review_list_2_content = []
@app.route('/compare', methods=['POST'])
def index2():
    data = request.json
    competitors = data.get('competitors', [])
    reviews_list_2.extend(competitors)
    print(f"review list: {reviews_list_2}")
    for x in reviews_list_2:
        completion = client.chat.completions.create(
            model="gpt-4o-mini-search-preview",
            messages=[
                {
                    "role": "user",
                    "content": f'''
                    Fetch me 10 recent reviews from all over internet for {x} hotel. 
                    Try and collect the recent reviews and all the details mentioned below. 
                    {{"Hotel_Name":"Taj, Yeswanthpur,
                    "reviewer_name":"Vanessa",
                    "review":"Nice, stay",
                    "review_date":"may 25, 2025",
                    "source":"https://www.makemytrip.com/hotels/lemon_tree_hotel_whitefield-details-bangalore.html",
                    "sentiment_score":"score between 0-1"}}''',
                }
            ],
        )
        review_list_2_content.append(completion.choices[0].message.content)
        
       
    completion = client.chat.completions.create(
            model="gpt-4.1-nano",
            messages=[
                {
                    "role": "user",
                    "content": f'''
                    Compare all the hotel reviews with Red Rhino's reviews, below given are list of reviews 
                    for each of the hotels. Give a detailed analysis on what Red Rhino can improve based on 
                    competetor reviews.
                    Reveiws:
                    {review_list_2_content}
                    '''}])
    response = completion.choices[0].message.content
    return jsonify({"answer": review_list_2_content,
                    "response":response})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8505, debug=True)