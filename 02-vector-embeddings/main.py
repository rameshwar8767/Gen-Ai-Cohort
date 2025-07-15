from dotenv import load_dotenv
from openai import OpenAI
load_dotenv()

client = OpenAI()

text = "Kalpesh is a Ai Engineer"

response = client.embeddings.create(
    input=text,
    model="text-embedding-3-small"

)

print("Response:", response)
print("Length of Embedding:", len(response.data[0].embedding))