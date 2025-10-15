from langgraph.graph import StateGraph, START, END
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import InMemorySaver

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

checkpointer = InMemorySaver()
graph = StateGraph(ChatState)

#nodes
graph.add_node('chat_node', chat_node)
graph.add_edge(START, 'chat_node')
graph.add_edge('chat_node', END)
chatbot = graph.compile(checkpointer=checkpointer)


# while True:
#     user_message = input('Type here:')
#     if user_message.strip().lower() in ['exit', 'quit', 'bye']:
#       break
#     print('User:', user_message)
#     response = chatbot.invoke({'messages': [HumanMessage(content=user_message)]})
#     print('AI:', response['messages'][-1].content)