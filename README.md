# AutoGen Examples

An early experiment to replicate AutoGen's examples with [ollama](https://ollama.com/download) local models.

Install AutoGen with: `pip install pyautogen`

You'll most likely need to `pip install yfinance matplotlib`

When generated code fails with module not found errors, give it some human assitant and pip install things for it.

Note: There are other ways to execute code besides directly running using LocalExecutor and manually pip installing things. However, I have mixed results using Docker and LocalExecutor with VirtualEnvironment.

Your millage may vary.

Mostly, all the examples are based from [AutoGen's examples](https://microsoft.github.io/autogen/docs/Examples)


## Simple usage
Give a simple prompt and use executor to repeatedly try until it gets the result
`python auto_simple.py`

## Coding task
This example is more akin to Software Developers usual tasks. Where we're in the loop and continuously give feedback to the agents.
`python coding_task.py`

## Perform research
The most succesful experiment is having multiple agents start doing research on their own and then have them communicate with each other. While having a `Planner` to reflect and look at the output.
`python research.py`


## Launching AutoGen Studio

`pip install autogenstudio`

`autogenstudio ui --port 8081`