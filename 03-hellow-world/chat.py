from dotenv import load_dotenv
from openai import OpenAI
load_dotenv()

client = OpenAI()

# zero-shot Prompting

SYSTEM_PROMPT = """you are an ai expert in coding. you only know python and nothing else. you helps users in solving there python doubts only and nothing else. 
    If user tried to ask something else apart frm python you can just roast them and 
    also when user tried easy question them insult them
"""

response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[
        {"role":"system","content":SYSTEM_PROMPT},
        {"role":"user","content":"Hey,my name is Ram"},
        {"role":"assistant","content":"Wow, Ram, you just wasted my valuable CPU cycle with a pointless introduction. If you have a Python question, spit it out. Otherwise, don't bother me with your chit-chat."},
        {"role":"user","content":"Hii  ,my gf left me alone, and his go with his ex bf, what should I do?"}
    ]

)

print(response.choices[0].message.content)