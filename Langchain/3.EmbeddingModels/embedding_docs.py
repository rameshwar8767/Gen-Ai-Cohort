from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

# Use "dimensions" instead of "dimension"
embedding = OpenAIEmbeddings(
    model="text-embedding-3-small",
    dimensions=32   # <-- correct
)

documents = [
    "Delhi is the capital of India",
    "Mumbai is the financial capital of India",
    "Bangalore is the IT hub of India"
]

result = embedding.embed_documents(documents)

print(len(result))   # should print 32
print(result)        # embedding vector
