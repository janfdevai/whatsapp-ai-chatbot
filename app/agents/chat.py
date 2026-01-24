# Step 1: Define tools and model

import operator

from langchain.chat_models import init_chat_model
from langchain.messages import AnyMessage, SystemMessage
from langchain.tools import ToolRuntime, tool
from langgraph.graph import END, START, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition
from typing_extensions import Annotated, TypedDict

model = init_chat_model("openai:gpt-5-nano", temperature=0)


@tool
def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"


@tool
def get_user_phone_number(runtime: ToolRuntime) -> str:
    """Get the user's phone number."""

    return runtime.state.get("user_phone_number")


tools = [get_weather, get_user_phone_number]
model_with_tools = model.bind_tools(tools)


class MessagesState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]
    user_phone_number: str
    llm_calls: int


def llm_call(state: MessagesState):
    """LLM decides whether to call a tool or not"""

    return {
        "messages": [
            model_with_tools.invoke(
                [
                    SystemMessage(
                        content="You are a helpful assistant tasked with performing arithmetic on a set of inputs."
                    )
                ]
                + state["messages"]
            )
        ],
        "user_phone_number": state.get("user_phone_number"),
        "llm_calls": state.get("llm_calls", 0) + 1,
    }


tool_node = ToolNode(tools)

# Step 6: Build agent

# Build workflow
agent_builder = StateGraph(MessagesState)

# Add nodes
agent_builder.add_node("llm_call", llm_call)
agent_builder.add_node("tools", tool_node)

# Add edges to connect nodes
agent_builder.add_edge(START, "llm_call")
agent_builder.add_conditional_edges("llm_call", tools_condition, ["tools", END])
agent_builder.add_edge("tools", "llm_call")

# Compile the agent
chat_agent = agent_builder.compile()
