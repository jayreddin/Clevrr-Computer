from langchain.agents import AgentExecutor, create_react_agent
from langchain_experimental.tools import PythonAstREPLTool
import pyautogui as pg # type: ignore


def create_clevrr_agent(model, prompt):
    print("============================================\nInitialising Clevrr Agent\n============================================")
    df_locals = {}
    df_locals["pg"] = pg
    tools = [PythonAstREPLTool(locals=df_locals)]
    agent = create_react_agent(model, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True, return_intermediate_steps=True)
    return agent_executor