# Step 1: Define tools and model

import operator

from langchain.chat_models import init_chat_model
from langchain.messages import AnyMessage, SystemMessage, ToolMessage
from langchain.tools import ToolRuntime, tool
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.types import Command
from typing_extensions import Annotated, TypedDict

model = init_chat_model("openai:gpt-5-nano", temperature=0)


class UserState(TypedDict):
    name: str
    phone_number: str


def merge_user(current: UserState, update: UserState) -> UserState:
    # Merges new keys into the existing user dictionary
    if current is None:
        return update
    return {**current, **update}


class MessagesState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]
    user: Annotated[UserState, merge_user]
    llm_calls: int


@tool
def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"


@tool
def get_user_phone_number(runtime: ToolRuntime) -> str:
    """Get the user's phone number."""

    return runtime.state.get("user", {}).get("phone_number", "unknown")


@tool
def get_user_name(runtime: ToolRuntime) -> str:
    """Get the name of the user"""
    return runtime.state.get("user", {}).get("name", "unknown")


@tool
def update_user_name(user_name: str, runtime: ToolRuntime) -> Command:
    """Update the name of the user in the state once they've revealed it."""
    return Command(
        update={
            "user": {"name": user_name},
            "messages": [
                ToolMessage(
                    "Successfully updated user name",
                    tool_call_id=runtime.tool_call_id,
                )
            ],
        }
    )


tools = [get_weather, get_user_phone_number, get_user_name, update_user_name]
model_with_tools = model.bind_tools(tools)


def llm_call(state: MessagesState):
    """LLM decides whether to call a tool or not"""

    return {
        "messages": [
            model_with_tools.invoke(
                [SystemMessage(content="You are a helpful assistant.")]
                + state["messages"]
            )
        ],
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

checkpointer = InMemorySaver()

# Compile the agent
chat_agent = agent_builder.compile(checkpointer=checkpointer)
