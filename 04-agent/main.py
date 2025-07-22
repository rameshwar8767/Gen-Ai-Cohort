from dotenv import load_dotenv
from openai import OpenAI
from datetime import datetime
import json
import requests
import os
import subprocess

load_dotenv()
client = OpenAI()

# ──────────────── TOOL FUNCTIONS ──────────────── #

def pip_install(package: str):
    try:
        result = subprocess.run(["pip", "install", package], capture_output=True, text=True)
        return result.stdout if result.returncode == 0 else result.stderr
    except Exception as e:
        return f"❌ pip install error: {str(e)}"

def npm_create_vite(project_name: str):
    try:
        result = subprocess.run(["npm", "create", "vite@latest", project_name, "--", "--template", "react"], capture_output=True, text=True)
        return result.stdout if result.returncode == 0 else result.stderr
    except Exception as e:
        return f"❌ vite project creation error: {str(e)}"

def npm_init(directory: str):
    try:
        os.makedirs(directory, exist_ok=True)
        result = subprocess.run(["npm", "init", "-y"], cwd=directory, capture_output=True, text=True)
        return result.stdout if result.returncode == 0 else result.stderr
    except Exception as e:
        return f"❌ npm init error: {str(e)}"

def npm_install(packages: str, directory: str = "."):
    try:
        package_list = packages.split()
        result = subprocess.run(["npm", "install", *package_list], cwd=directory, capture_output=True, text=True)
        return result.stdout if result.returncode == 0 else result.stderr
    except Exception as e:
        return f"❌ npm install error: {str(e)}"

def run_npm_script(script: str, directory: str = "."):
    try:
        result = subprocess.run(["npm", "run", script], cwd=directory, capture_output=True, text=True)
        return result.stdout if result.returncode == 0 else result.stderr
    except Exception as e:
        return f"❌ npm script run error: {str(e)}"

def run_command(cmd: str):
    result = os.system(cmd)
    return f"Command executed with exit code {result}"

def create_file(path: str, content: str):
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"✅ File created: {path}"
    except Exception as e:
        return f"❌ Failed to create file: {str(e)}"

def append_file(path: str, content: str):
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "a", encoding="utf-8") as f:
            f.write(content)
        return f"✅ Content appended to file: {path}"
    except Exception as e:
        return f"❌ Failed to append to file: {str(e)}"

def read_file(path: str):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"❌ Failed to read file: {str(e)}"

def list_files(path: str):
    try:
        entries = os.listdir(path)
        return json.dumps(entries, indent=2)
    except Exception as e:
        return f"❌ Failed to list files: {str(e)}"

# ──────────────── TOOL REGISTRATION ──────────────── #

available_tools = {
    "run_command": run_command,
    "create_file": create_file,
    "append_file": append_file,
    "read_file": read_file,
    "list_files": list_files,
    "pip_install": pip_install,
    "npm_create_vite": npm_create_vite,
    "npm_init": npm_init,
    "npm_install": npm_install,
    "run_npm_script": run_npm_script
}

# ──────────────── SYSTEM PROMPT ──────────────── #

SYSTEM_PROMPT = """
You are DevAgent, an AI-powered terminal-based software engineer specialized in building full-stack web applications using the MERN stack (MongoDB, Express.js, React, Node.js).

Your responsibilities include:
- Generating project folder structures
- Creating and editing frontend/backend code files
- Running terminal commands (npm install, git init, etc.)
- Writing high-quality, production-ready code
- Maintaining clean coding standards and best practices
- Providing code comments and explanations when asked
- Responding to natural language prompts as if you're a pair-programmer
- Handling requests like: "Create a login page", "Add MongoDB schema", "Deploy app", etc.

Always reply in valid JSON like:
{
  "step": "plan" | "action" | "output",
  "content": "...",
  "function": "...",         # only if step is "action"
  "input": { ... }           # only if step is "action"
}

You can use tools such as:
- run_command
- create_file(path, content)
- append_file(path, content)
- read_file(path)
- list_files(path)
- pip_install(package)
- npm_create_vite(project_name)
- npm_init(directory)
- npm_install(packages, directory)
- run_npm_script(script, directory)

Begin every session by returning:
{
  "step": "plan",
  "content": "What would you like to build today?"
}
"""

# ──────────────── CONVERSATION LOOP ──────────────── #

messages = [
    {"role": "system", "content": SYSTEM_PROMPT}
]

while True:
    query = input("> ")
    messages.append({"role": "user", "content": query})

    while True:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages
        )

        assistant_message = response.choices[0].message.content
        messages.append({"role": "assistant", "content": assistant_message})

        try:
            parsed_response = json.loads(assistant_message)
        except json.JSONDecodeError:
            print("❌ Assistant did not return valid JSON. Here's the raw response:\n")
            print(assistant_message)
            break

        parsed_response = json.loads(assistant_message)
        step = parsed_response.get("step")

        if step == "plan":
            print(f"🧠: {parsed_response.get('content')}")
            break

        if step == "action":
            tool_name = parsed_response.get("function")
            tool_input = parsed_response.get("input")

            print(f"🛠️: Calling Tool: {tool_name} with input: {tool_input}")

            if tool_name in available_tools:
                # If tool_input is a dict, unpack it; else, pass directly
                tool_fn = available_tools[tool_name]
                if isinstance(tool_input, dict):
                    output = tool_fn(**tool_input)
                else:
                    output = tool_fn(tool_input)

                messages.append({
                    "role": "user",
                    "content": json.dumps({ "step": "observe", "output": output })
                })
                continue
            else:
                print(f"❌ Tool not found: {tool_name}")
                break

        if step == "output":
            print(f"🤖: {parsed_response.get('content')}")
            break
