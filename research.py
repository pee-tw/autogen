from autogen import UserProxyAgent, GroupChat, GroupChatManager
from agents import engineer, planner, researcher, executor


regular_config = {
    "model": "qwen2:latest",
    "base_url": "http://localhost:11434/v1",
    "api_key": "ollama",
}

user_proxy = UserProxyAgent(
    name="Admin",
    system_message=(
        "A human admin. Interact with the planner to discuss the plan. "
        "Plan execution needs to be approved by this admin."
    ),
    code_execution_config=False,
)


def state_transition(last_speaker, groupchat_instance):
    messages = groupchat_instance.messages
    last_message = messages[-1]["content"]

    if len(messages) <= 1:
        return planner

    if last_speaker is engineer:
        if "```" in last_message:
            # Contain code, ask executor to run
            return executor
        # Does not contain code ask engineer to re-write code
        return engineer
    elif last_speaker is executor:
        if "Traceback (most recent call last):" in last_message:
            return engineer
        return researcher

    return "auto"


groupchat = GroupChat(
    agents=[user_proxy, planner, researcher, engineer, executor],
    messages=[],
    max_round=50,
    allow_repeat_speaker=False,
    send_introductions=True,
    speaker_selection_method=state_transition,
)
manager = GroupChatManager(
    groupchat=groupchat, llm_config={"config_list": [regular_config]}
)

chat_message = """
Answer the following by looking at economic data from Wikipedia and arXiv:

Thailand is making a loan to give away 10 thoudsand baht to its citizen but only to those 
who has less than 500 thousands baht in savings and earn less than 70 thousand baht 
per month.

The engineer should ask the executor to write a Python script to fetch the data
print the results so that other agents can read the result.

Requirement: 
- Cite data from 5 - 10 papers arXiv.
- Use economic, demographic and cultural data from Wikipedia.
- Find similar schemes implemented by other countries.

Draw conclusion based on papers and data. 

Analyse possible risks and critique whether this is a good action or not.
"""


user_proxy.initiate_chat(manager, message=chat_message)
