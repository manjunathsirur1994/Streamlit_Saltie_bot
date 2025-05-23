from openai import OpenAI
from dotenv import load_dotenv
# from flask_cors import CORS
import os 

# # Load environment variables
load_dotenv()
key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=key)

# hotel_name = 'Red Rhino, Whitefield, Bangalore'
# n_reviews = 20
# n_reviews = n_reviews//10
# reviews_list = []
# prompt = '''

# '''
# for x in range(n_reviews):
#     completion = client.chat.completions.create(
#         model="gpt-4o-mini-search-preview",
#         web_search_options={},
#         messages=[
#             {
#                 "role": "user",
#                 "content": f'''Previous reviews: {reviews_list}. 
#                 Fetch me 10 recent reviews from all over internet for {hotel_name} hotel. 
#                 Make sure they are not the same as previous reviews.
#                 Try and collect the recent reviews. 
#                 Make sure to format it in the below format:
#                 {{"reviewer_name":"Vanessa",
#                 "review":"Nice, stay",
#                 "review_date":"may 25, 2025",
#                 "source":"https://www.makemytrip.com/hotels/lemon_tree_hotel_whitefield-details-bangalore.html",
#                 "sentiment_score":"score between 0-1"}}''',
#             }
#         ],
#     )
#     reviews_list.append(completion.choices[0].message.content)

# print(reviews_list)

from openai import OpenAI

completion = client.chat.completions.create(
    model="gpt-4o-search-preview",
    web_search_options={},
    messages=[
        {
            "role": "user",
            "content": "What was a positive news story from today? tell me in one line. ",
        }
    ],
)

print(completion.choices[0].message.content)