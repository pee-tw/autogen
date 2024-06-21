from autogen import UserProxyAgent, GroupChat, GroupChatManager
from agents import planner, ba, generic_config

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

    if len(messages) <= 1:
        return planner

    return "auto"


groupchat = GroupChat(
    agents=[user_proxy, planner, ba],
    messages=[],
    max_round=50,
    allow_repeat_speaker=False,
    speaker_selection_method=state_transition,
)
manager = GroupChatManager(
    groupchat=groupchat, llm_config={"config_list": [generic_config]}
)

chat_message = """
Draft a JIRA story to:

Create a data pipeline to ingest Google sheet to GCS as parquet files.

The following are the requirements for this task:
- The pipeline should be idempotent and retryable in case of failure.
- The pipeline should be able to handle multiple sheets in the same Google sheet file.
"""


user_proxy.initiate_chat(manager, message=chat_message)
