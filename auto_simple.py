from autogen import AssistantAgent, UserProxyAgent
from autogen.coding import LocalCommandLineCodeExecutor

config_list = [
    {
        "model": "codellama:13b",
        "base_url": "http://localhost:11434/v1",
        "api_key": "ollama",
    }
]

executor = LocalCommandLineCodeExecutor(work_dir="coding")

# To disable LLM caching, set the cache_seed to None
assistant = AssistantAgent("assistant", llm_config={"config_list": config_list})

user_proxy = UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={"executor": executor},
)

user_proxy.initiate_chat(
    assistant,
    message="""
    Plot a graph showing NVDA stock closing price using Yahoo Finance's Data
        since 2020, put a label on the graph marking the time when ChatGPT became popular
    """,
    summary_method="reflection_with_llm",
)
