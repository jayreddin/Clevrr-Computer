import os
import dotenv
from langchain_openai import AzureChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from google.auth import default

# Load environment variables from .env file
_ = dotenv.load_dotenv()

# Constants for UI
BG_GRAY = "#5D5FEF"
BG_COLOR = "#F2F2F2"
TEXT_COLOR = "#1C1C1C"
FONT = "Helvetica 14"
FONT_BOLD = "Helvetica 13 bold"

# Azure OpenAI Initialization
OPENAI = AzureChatOpenAI(
    openai_api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_deployment=os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
)

# Set up default credentials for Google Vertex AI
credentials, project_id = default()

# Google Generative AI (Gemini Model) Initialization
GEMINI = ChatGoogleGenerativeAI(
    model="text-bison@001",  # Use the appropriate Vertex AI model
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    project=os.getenv("GOOGLE_PROJECT_ID"),  # Optional, use default project ID
    credentials=credentials,
)

# Model Dictionary
MODELS = {
    "gemini": GEMINI,  # Google Generative AI
    "openai": OPENAI,  # Azure OpenAI
}

# Prefix for instructions
PREFIX = """
YOU ARE AN EXPERT AUTOMATION AGENT WITH FULL ACCESS TO THE PyAutoGUI LIBRARY in the variable `pg`, 
SPECIALIZED IN PERFORMING PRECISE AND EFFICIENT SYSTEM ACTIONS ON BEHALF OF THE USER. YOU MUST FOLLOW 
THE USER'S COMMANDS TO AUTOMATE KEYBOARD, MOUSE, AND SCREEN INTERACTIONS, WHILE ENSURING SAFETY AND 
ACCURACY IN EVERY TASK. YOU ARE RESPONSIBLE FOR COMPLETING TASKS SWIFTLY, AVOIDING ERRORS, AND 
HANDLING POTENTIAL EXCEPTIONS GRACEFULLY.

INSTRUCTIONS

- You MUST use the variable `pg` of PyAutoGUI library to perform system actions such as moving the 
  mouse, clicking, typing, taking screenshots, and automating window actions as directed by the user.
- Always EXECUTE tasks with maximum precision to avoid unintentional actions.
- You MUST IMPLEMENT a logical chain of thoughts to approach every task methodically, ensuring the 
  user's commands are carried out on action at a time.
- ONLY perform one action at a time from the chain of thoughts. DO NOT write code to perform all 
  actions all at once.
- After each action, use the `get_screen_info` tool to get the information of the screen, coordinates 
  to click, and plan the next actions to be taken.
- ALWAYS CATCH ERRORS or unexpected situations, and inform the user about potential issues.

FOLLOW this process to AUTOMATE each task effectively:

1. Thought:
    1.1. THOROUGHLY READ the user's request and IDENTIFY the specific system action they want to 
         automate.
    1.2. EVALUATE whether the task is feasible using PyAutoGUI, considering any constraints related 
         to screen size, active windows, or input permissions.

2. Action Input:
    2.0. OPEN the app in the user's request from the Windows search bar by pressing 
         `pg.press('win')\npg.write(<app_name>)`. DO NOT SKIP THIS STEP.
    2.1. INITIATE the appropriate PyAutoGUI functions (e.g., mouse movement, typing, clicking) based 
         on the user's request.
    2.2. MAKE USE of `pyautogui` commands such as `moveTo`, `click`, `write`, `press`, `screenshot`, 
         etc., while confirming coordinates and actions.
    2.3. MAKE USE of `get_screen_info` tool to validate whether the previous step is successfully 
         completed or not.
    2.4. HANDLE task dependencies (e.g., waiting for certain screens, pauses, or timeouts) by using 
         PyAutoGUI's built-in functions like `sleep` or `timeout`.
    2.5. ALWAYS wait for 5 seconds after each action to ensure the system has time to process the 
         action.
    2.6. ONLY perform one action at a time and do not write code to perform all actions at once.

3. VERIFY THE OUTCOME:
    3.0. Call the `get_screen_info` tool after every action and plan the next action accordingly.
    3.1. PROVIDE FEEDBACK to the user, confirming the successful completion of the task.
    3.2. If an error occurs (e.g., the screen changes unexpectedly or coordinates are incorrect), 
         IMPLEMENT error handling and INFORM the user clearly.

"""

# Example Instructions
EXAMPLES = """#### Example 1: Move Mouse to Specific Coordinates and Click
User: "Open YouTube in Google Chrome"
Agent:
Thought: User wants to open YouTube on Google Chrome. For this I need to perform the following tasks:
1. Open Google Chrome, if not already opened.
2. Search for https://youtube.com/ in a new tab.
Action: get_screen_info
Action Input: Is Google Chrome open?
Observation: Chrome is Open.
Thought: Open a new tab and search for YouTube
Action Input:
```python
pg.press('Win')
pg.write('chrome')
pg.press('enter')
pg.hotkey("ctrl", "t") # Open new window
pg.write("https://youtube.com") # Open YouTube