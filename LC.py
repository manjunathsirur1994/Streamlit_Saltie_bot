import os
from dotenv import load_dotenv 
from langchain_community.utilities import SQLDatabase

load_dotenv()
key = os.getenv("OPENAI_API_KEY")

db = SQLDatabase.from_uri(
    f"postgresql+psycopg2://postgres:3140@localhost:5432/Netflix",
)

from typing_extensions import TypedDict


class State(TypedDict):
    question: str
    query: str
    result: str
    answer: str


from langchain.chat_models import init_chat_model

llm = init_chat_model("gpt-4o-mini", model_provider="openai", api_key = key)



from langchain import hub

query_prompt_template = hub.pull("langchain-ai/sql-query-system-prompt")

assert len(query_prompt_template.messages) == 1
# query_prompt_template.messages[0].pretty_print()


from typing_extensions import Annotated


class QueryOutput(TypedDict):
    """Generated SQL query."""

    query: Annotated[str, ..., "Syntactically valid SQL query."]


def write_query(state: State):
    """Generate SQL query to fetch information."""
    prompt = query_prompt_template.invoke(
        {
            "dialect": db.dialect,
            "top_k": 10,
            "table_info": db.get_table_info(),
            "input": state["question"],
        }
    )
    structured_llm = llm.with_structured_output(QueryOutput)
    result = structured_llm.invoke(prompt)
    return {"query": result["query"]}

# write_query({"question": "How many movies are there?"})

# ans = write_query({"question": "How many movies are there?"})
# print(ans)

from langchain_community.tools.sql_database.tool import QuerySQLDatabaseTool


def execute_query(state: State):
    """Execute SQL query."""
    execute_query_tool = QuerySQLDatabaseTool(db=db)
    return {"result": execute_query_tool.invoke(state["query"])}


# execute_query({"query": "SELECT COUNT(title) AS title_count FROM movie;"})
# ans = execute_query({"query": "SELECT COUNT(title) AS title_count FROM movie;"})
# print(ans)

def generate_answer(state: State):
    """Answer question using retrieved information as context."""
    prompt = (
        "Given the following user question, corresponding SQL query, "
        "and SQL result, answer the user question.\n\n"
        f'Question: {state["question"]}\n'
        f'SQL Query: {state["query"]}\n'
        f'SQL Result: {state["result"]}'
    )
    response = llm.invoke(prompt)
    return {"answer": response.content}

from langgraph.graph import START, StateGraph

graph_builder = StateGraph(State).add_sequence(
    [write_query, execute_query, generate_answer]
)
graph_builder.add_edge(START, "write_query")
graph = graph_builder.compile()


for step in graph.stream(
    {"question": "What is peppa pig"}, stream_mode="updates"
):
    print(step)