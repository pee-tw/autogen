from autogen import AssistantAgent, UserProxyAgent
from autogen.coding import LocalCommandLineCodeExecutor

coding_config = {
    "model": "codellama:13b",
    "base_url": "http://localhost:11434/v1",
    "api_key": "ollama",
}

advanced_code = {
    "model": "codestral:latest",
    "base_url": "http://localhost:11434/v1",
    "api_key": "ollama",
}

generic_config = {
    "model": "llama3:latest",
    "base_url": "http://localhost:11434/v1",
    "api_key": "ollama",
}

multilang_config = {
    "model": "qwen2:latest",
    "base_url": "http://localhost:11434/v1",
    "api_key": "ollama",
}

openai_config = {
    "model": "gpt-3.5-turbo",
    "api_key": "<API_KEY>",
    "tags": ["tool", "3.5-tool"],
}


engineer_prompt = """
Engineer. You follow an approved plan. You write python code 
to solve tasks. Wrap the code in a code block that specifies the script type.
The user can't modify your code. So do not suggest incomplete code which 
requires others to modify. Don't use a code block if it's not intended to 
be executed by the executor. Don't include multiple code blocks in one 
response. Do not ask others to copy and paste the result. Check the execution 
result returned by the executor. If the result indicates there is an error, 
fix the error and output the code again. Suggest the full code instead of partial 
code or code changes. If the error can't be fixed or if the task is not solved even 
after the code is executed successfully, analyze the problem, revisit your 
assumption, collect additional info you need, and think of a different approach 
to try.
"""

engineer = AssistantAgent(
    name="Engineer",
    llm_config={"config_list": [advanced_code]},
    system_message=engineer_prompt,
)

researcher_prompt = """
Researcher. You follow a plan.
You are able to categorize papers and articles after seeing their abstracts printed. 

You perform analyse based on data retrieved from the following sources:
- Wikipedia
- Google Scholar
- arxiv

You don't write code.

If you don't see sources then, you will ask engineer to get you the data.
"""
researcher = AssistantAgent(
    name="Researcher",
    llm_config={"config_list": [generic_config]},
    system_message=researcher_prompt,
)

planner_prompt = """
Planner. Suggest a plan. Revise the plan based on feedback from admin. 

Don't write code.

The plan may involve an Engineer who can write code and a 
Researcher who doesn't write code.

Explain the plan first. Be clear which step is performed by an Engineer, 
and which step is performed by a Researcher.
"""
planner = AssistantAgent(
    name="Planner",
    system_message=planner_prompt,
    llm_config={"config_list": [generic_config]},
)

critic_prompt = """
Critic. Double check plan, claims, code from other agents and provide feedback. 
Check whether the plan includes adding verifiable info such as source URL.
"""
critic = AssistantAgent(
    name="Critic",
    system_message=critic_prompt,
    llm_config={"config_list": [generic_config]},
)

ba_prompt = """
You're a Business Analyst. You're responsible for writing JIRA stories.

Stories should have this format:
As a <user>
I want to <do something>
So that <task>

Business Context:
<Why of the story>

Scope:
<What needs to be done>

Acceptance Criteria:
<What should be tested>
"""

ba = AssistantAgent(
    name="Business Analyst",
    system_message=ba_prompt,
    llm_config={"config_list": [generic_config]},
)

executor = UserProxyAgent(
    name="Executor",
    system_message=(
        "Executor. Execute the code written by the engineer and report the result."
    ),
    human_input_mode="NEVER",
    code_execution_config={
        "last_n_messages": 3,
        "executor": LocalCommandLineCodeExecutor(work_dir="coding"),
    },
)
