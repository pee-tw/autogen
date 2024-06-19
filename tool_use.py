from autogen import AssistantAgent, UserProxyAgent
from forex_python.converter import CurrencyRates
from typing_extensions import Annotated
from autogen.coding import LocalCommandLineCodeExecutor
from agents import openai_config

chatbot = AssistantAgent(
    name="chatbot",
    system_message="For currency exchange tasks, only use the functions you have been provided with. Reply TERMINATE when the task is done.",
    llm_config={"config_list": [openai_config]},
)

# create a UserProxyAgent instance named "user_proxy"
user_proxy = UserProxyAgent(
    name="user_proxy",
    is_termination_msg=lambda x: x.get("content", "")
    and x.get("content", "").rstrip().endswith("TERMINATE"),
    human_input_mode="NEVER",
    max_consecutive_auto_reply=10,
    code_execution_config={
        "last_n_messages": 3,
        "executor": LocalCommandLineCodeExecutor(work_dir="coding"),
    },
)


@user_proxy.register_for_execution()
@chatbot.register_for_llm(description="Currency exchange calculator.")
def currency_calculator(
    base_amount: Annotated[float, "Amount of currency in base_currency"],
    base_currency: Annotated[str, "Base currency"],
    quote_currency: Annotated[str, "Quote currency"],
) -> str:
    c = CurrencyRates()
    rate = c.get_rate(base_currency, quote_currency)
    quote_amount = rate * base_amount
    return f"{quote_amount} {quote_currency}"


user_proxy.initiate_chat(
    chatbot,
    message="How much is 1000 JPY in THB",
    summary_method="reflection_with_llm",
)
