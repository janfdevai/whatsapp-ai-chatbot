import operator

from langchain.chat_models import init_chat_model
from langchain.messages import AnyMessage, SystemMessage
from langgraph.graph import END, START, StateGraph
from typing_extensions import Annotated, TypedDict

model = init_chat_model("openai:gpt-5-nano", temperature=0)


class MessagesState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]
    llm_calls: int


def llm_call(state: dict):
    """LLM call node. Calls the language model and returns the response."""

    return {
        "messages": [
            model.invoke(
                [SystemMessage(content="You are a friendly chatbot.")]
                + state["messages"]
            )
        ],
        "llm_calls": state.get("llm_calls", 0) + 1,
    }


# Build workflow
chat_agent_builder = StateGraph(MessagesState)

# Add nodes
chat_agent_builder.add_node("llm_call", llm_call)


# Add edges to connect nodes
chat_agent_builder.add_edge(START, "llm_call")
chat_agent_builder.add_edge("llm_call", END)


chat_agent = chat_agent_builder.compile()
