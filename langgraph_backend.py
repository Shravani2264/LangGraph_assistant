from langgraph.graph import StateGraph, START, END
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
print(f"✅ Model successfully initialized: {llm.model}") # Add this line

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


def chat_node(state: ChatState):
    # take query from state
    messages = state['messages']
    #send to llm
    print(f"--- Just before API call, model is: {llm.model} ---")
    response = llm.invoke(messages)
    #response store in state
    return {'messages':[response]}
conn = sqlite3.connect(database='chatbot.db', check_same_thread=False)
checkpointer = SqliteSaver(conn = conn)
graph = StateGraph(ChatState)

#nodes
graph.add_node('chat_node', chat_node)
graph.add_edge(START, 'chat_node')
graph.add_edge('chat_node', END)
chatbot = graph.compile(checkpointer=checkpointer)
def retrieve_all_threads():
    all_threads = set()
    for checkpoint in checkpointer.list(None):
        all_threads.add(checkpoint.config['configurable']['thread_id'])
    return list(all_threads)

# while True:
#     user_message = input('Type here:')
#     if user_message.strip().lower() in ['exit', 'quit', 'bye']:
#       break
#     print('User:', user_message)
#     response = chatbot.invoke({'messages': [HumanMessage(content=user_message)]})
#     print('AI:', response['messages'][-1].content)