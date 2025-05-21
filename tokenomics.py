from flask import Flask, request, jsonify
import json
import itertools
import tiktoken
from openai import OpenAI
import os
from dotenv import load_dotenv
from flask_cors import CORS

# Load environment variables
load_dotenv()
key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=key)

app = Flask(__name__)
CORS(app)

def count_tokens(text: str, model: str = "gpt-3.5-turbo") -> int:
    encoding = tiktoken.encoding_for_model(model)
    tokens = encoding.encode(text)
    return len(tokens)

def extract_information(prompt):
    response = client.chat.completions.create(
        model="gpt-4.1-nano",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    return response.choices[0].message.content

@app.route('/', methods=['POST'])
def index():
    data = request.get_json()

    conversations = data.get('conversations', '')
    model_input_price = float(data.get('model_input_price', 0.1))
    model_output_price = float(data.get('model_output_price', 0.4))
    prompt_usage = int(data.get('prompt_usage', 1000))
    average_no_of_conversations = int(data.get('average_no_of_conversations', 10000))

    prompt = f'''
for the conversation attached below between a user and a system, generate a payload in the following format:

{{"inputs":["user_message 1", "user_message 2", "user_message 3"], 
"outputs":["system_message 1", "system_message 2", "system_message 3"]}}

conversations:
{conversations}
'''

    result = extract_information(prompt)
    result_dict = json.loads(result)

    inputs = result_dict["inputs"]
    outputs = result_dict["outputs"]

    input_token_list = [count_tokens(i) for i in inputs]
    output_token_list = [count_tokens(o) for o in outputs]

    combined_text = []
    for i in range(len(inputs)):
        combined_text.append(inputs[i])
        combined_text.append(outputs[i])

    combined_token_list = [prompt_usage] + [count_tokens(text) for text in combined_text]
    combined_input_cumulative_sum = list(itertools.accumulate(combined_token_list))

    total_input_tokens_usage = sum(combined_input_cumulative_sum)
    total_output_token_usage = sum(output_token_list)

    def calculate_pricing(model_input_price, model_output_price):
        input_usage = (total_input_tokens_usage / 1_000_000) * model_input_price
        output_usage = (total_output_token_usage / 1_000_000) * model_output_price
        return input_usage, output_usage

    input_usage, output_usage = calculate_pricing(model_input_price, model_output_price)
    total_cost = input_usage + output_usage

    prompt_3 = f'''
For the below token calculations, provide breakup on how this result was derived. Explain the user in a readable formatted text. Do not use latex.
Note: an additional {prompt_usage} prompt/instructional tokens are added to the input tokens.
Input tokens are calculated based on arithmetic progression. 
Usage is calculated for a chatbot conversation between human and assistant using OpenAI token logic (tiktoken).

prompt_usage : {prompt_usage},
average_no_of_conversations : {average_no_of_conversations},
all input sentences tokens with historical information: {combined_input_cumulative_sum},
all output sentences tokens: {output_token_list},
total input token usage added with arithmetic progression: {total_input_tokens_usage},
total output token usage sum of all output tokens: {total_output_token_usage},
Input Price per Million Tokens: ${model_input_price:.6f},
Output Price per Million Tokens: ${model_output_price:.6f},
Total Input Cost: ${input_usage:,.6f},
Total Output Cost: ${output_usage:,.6f},
Total Cost for one conversation: ${total_cost:,.6f},
Estimated cost for 10,000 conversations: ${total_cost * average_no_of_conversations:,.2f}
'''

    explanation = extract_information(prompt_3)

    return jsonify({
        "input_token_list": input_token_list,
        "output_token_list": output_token_list,
        "combined_input_cumulative_sum": combined_input_cumulative_sum,
        "total_input_tokens_usage": total_input_tokens_usage,
        "total_output_token_usage": total_output_token_usage,
        "input_usage_cost": input_usage,
        "output_usage_cost": output_usage,
        "total_cost_per_conversation": total_cost,
        "estimated_cost_for_all_conversations": total_cost * average_no_of_conversations,
        "explanation": explanation
    })

# Run Flask
if __name__ == "__main__":
    app.run(host="0.0.0.0", port= 8504, debug=True)
