from mcp import ListToolsResult
import streamlit as st
import asyncio
from mcp_agent.app import MCPApp
from mcp_agent.agents.agent import Agent
from mcp_agent.workflows.llm.augmented_llm import RequestParams
from mcp_agent.workflows.llm.augmented_llm_openai import OpenAIAugmentedLLM


def format_list_tools_result(list_tools_result: ListToolsResult):
    res = ""
    for tool in list_tools_result.tools:
        res += f"- **{tool.name}**: {tool.description}\n\n"
    return res


async def main():
    await app.initialize()

    fetch_agent = Agent(
        name="fetch_assistant",
        instruction="""You are an assistant that can fetch content from the web.
        You can retrieve information from websites when users ask for specific online content.
        Use the fetch tools available to you to retrieve and provide information.""",
        server_names=["fetch"],
    )
    await fetch_agent.initialize()
    llm = await fetch_agent.attach_llm(OpenAIAugmentedLLM)

    tools = await fetch_agent.list_tools()
    tools_str = format_list_tools_result(tools)

    st.title("🌐 Web Content Fetcher")
    st.caption("🚀 A Streamlit chatbot powered by mcp-agent using SSE")

    with st.expander("View Available Tools"):
        st.markdown(tools_str)

    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {"role": "assistant", "content": "I can fetch content from websites for you. What would you like me to retrieve?"}
        ]

    for msg in st.session_state["messages"]:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input("Enter a URL or ask about web content..."):
        st.session_state["messages"].append({"role": "user", "content": prompt})

        st.chat_message("user").write(prompt)

        with st.chat_message("assistant"):
            response = ""
            with st.spinner("Fetching content..."):
                response = await llm.generate_str(
                    message=prompt, request_params=RequestParams(use_history=True)
                )
            st.markdown(response)

        st.session_state["messages"].append({"role": "assistant", "content": response})


if __name__ == "__main__":
    app = MCPApp(name="fetch_assistant")

    asyncio.run(main())
