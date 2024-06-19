from autogen import UserProxyAgent, GroupChat, GroupChatManager
from agents import engineer, executor, generic_config

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

    if last_speaker is engineer:
        if "```" in last_message:
            return executor
        else:
            # Otherwise, let the engineer to continue
            return engineer
    elif last_speaker is executor:
        if "Traceback (most recent call last):" in last_message:
            return engineer

    return "auto"


groupchat = GroupChat(
    agents=[user_proxy, engineer, executor],
    messages=[],
    max_round=50,
    allow_repeat_speaker=False,
    speaker_selection_method=state_transition,
)
manager = GroupChatManager(
    groupchat=groupchat, llm_config={"config_list": [generic_config]}
)

chat_message = """
Write a Python function to scrape certifications for a given user on Credly

You starting point should be https://www.credly.com/organizations/google-cloud/directory

Here's an example user's name: Pee Tankulrat
"""


user_proxy.initiate_chat(manager, message=chat_message)
