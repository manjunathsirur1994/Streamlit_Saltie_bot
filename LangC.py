# Download data

# import kagglehub

# # Download latest version
# path = kagglehub.dataset_download("harmanpreet93/hotelreviews")

# print("Path to dataset files:", path)


# Data pre processing
# import pandas as pd
# import numpy as np
# df = pd.read_csv('hotel-reviews.csv', low_memory=False)

# start_date = pd.to_datetime('2024-11-01')
# end_date = pd.to_datetime('2025-05-31')

# num_days = (end_date - start_date).days

# random_dates = start_date + pd.to_timedelta(np.random.randint(0, num_days + 1, size=len(df)), unit='D')

# df['date'] = random_dates

# df['review_month'] = df['date'].dt.month
# df['review_year'] = df['date'].dt.year
# df.rename(columns = {"Description":"reviews"}, inplace=True)
# df.drop(columns=['Browser_Used', 'Device_Used', 'Is_Response'], inplace=True)
# df.to_csv('hotel-reviews.csv')
# print(df.head())


# Append to db in postgres

# import pandas as pd
# import psycopg2
# from sqlalchemy import create_engine

# # Load CSV using pandas
# df = pd.read_csv("hotel-reviews.csv")

# # Create SQLAlchemy engine
# engine = create_engine("postgresql://chatbotuser:chatbot123@chatbot-db.c9fmepiiqg6o.us-east-1.rds.amazonaws.com:5432/Hackathon_Guest_Genius_tables")

# # Write data to a new table (will auto-create table schema)
# df.to_sql("Review_table", engine, index=False, if_exists="replace")  # or "append"



# ------------------------------------------------------------------------------------------------------------

from flask import Flask, request, jsonify
from langchain_community.utilities import SQLDatabase
from langchain.chat_models import init_chat_model
from langchain import hub
from langchain_community.tools.sql_database.tool import QuerySQLDatabaseTool
from langgraph.graph import START, StateGraph
from typing_extensions import TypedDict, Annotated
from dotenv import load_dotenv
import os
import lcconfig

# Load API key
load_dotenv()
key = os.getenv("OPENAI_API_KEY")

# Load database config
config = lcconfig.load_config()
username, password, host, port, uri, db_name = (
    config['username'], config['password'], config['host'], 
    config['port'], config['uri'], config['DB']
)

# Initialize Flask app
app = Flask(__name__)

# Setup database connection
db = SQLDatabase.from_uri(f"{uri}://{username}:{password}@{host}:{port}/{db_name}")

# Define state class
class State(TypedDict):
    question: str
    query: str
    result: str
    answer: str

# Initialize chat model
llm = init_chat_model("gpt-4.1-nano", model_provider="openai", api_key=key)
query_prompt_template = hub.pull("langchain-ai/sql-query-system-prompt")

# Define query generation function
class QueryOutput(TypedDict):
    query: Annotated[str, ..., "Syntactically valid SQL query."]

def write_query(state: State):
    print(f"Dialect: --> {db.dialect}") 
    prompt = query_prompt_template.invoke(
        {
            "dialect": db.dialect,
            "top_k": 1000,
            "table_info": db.get_table_info(),
            "input": f"{state["question"]}. Return equal to 1000 rows. Do not use LIMIT 1.",
        }
    )
    
    structured_llm = llm.with_structured_output(QueryOutput)
    result = structured_llm.invoke(prompt)
    return {"query": result["query"]}

# Define query execution function
def execute_query(state: State):
    execute_query_tool = QuerySQLDatabaseTool(db=db)
    return {"result": execute_query_tool.invoke(state["query"])}

# Define answer generation function
def generate_answer(state: State):
    prompt = (
        f'''Given the following user question, corresponding SQL query, and SQL result, answer the user question.\n\n
        Note: you are a review analyser, make sure to give the right analysis of the reviews you are provided with'''
        f'Question: {state["question"]}\n'
        f'SQL Query: {state["query"]}\n'
        f'SQL Result: {state["result"]}'
    )
    response = llm.invoke(prompt)
    return {"answer": response.content}

# Create LangGraph pipeline
graph_builder = StateGraph(State).add_sequence([
    write_query, execute_query, generate_answer
])
graph_builder.add_edge(START, "write_query")
graph = graph_builder.compile()

# CLI interaction
@app.route("/query", methods=["POST"])
def query_bot():
    all_answers = ''
    data = request.json
    question = data.get("question", "")
    if not question:
        return jsonify({"error": "Missing 'question' in request"}), 400

    try:
        state = {"question": question}
        for step in graph.stream(state, stream_mode="updates"):
            step_name = list(step.keys())[0]
            step_output = list(list(step.values())[0].values())[0]
            all_answers = all_answers + f'{step_name}\n  {step_output}' 
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    return jsonify({"answer": all_answers})

# Run Flask
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)



