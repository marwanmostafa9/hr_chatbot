from nodes import SharedState, agent
from langgraph.graph import START, END, StateGraph
from langgraph.checkpoint.memory import MemorySaver

# Create graph
graph_builder = StateGraph(SharedState)
memory = MemorySaver()

graph_builder.add_node("agent", agent)
graph_builder.add_edge(START, "agent")
graph_builder.add_edge("agent", END)
graph = graph_builder.compile(checkpointer=memory)


# def stream_tool_responses(user_input: str):
#     config = {"configurable":{"thread_id":"single_session_memory"}}

#     # Stream through the graph
#     for event in graph.stream({"messages":[("user",user_input)]}, config):
#         for value in event.values():
#             print(value["messages"][-1].content)

# # Chat loop
# for _ in range(5):
#     user_input = input("You: ")
#     stream_tool_responses(user_input)
