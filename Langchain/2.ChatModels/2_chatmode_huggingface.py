from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv
import os

# Load .env file (must contain HUGGINGFACEHUB_API_TOKEN)
load_dotenv()

# Create Hugging Face Endpoint LLM
llm = HuggingFaceEndpoint(
    repo_id="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    task="text-generation",
    huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_API_TOKEN"),
    max_new_tokens=128
)

# Wrap it as a Chat model
model = ChatHuggingFace(llm=llm)

# Query the model
response = model.invoke("What is the capital of India?")
print(response.content)
