from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

# Use "dimensions" instead of "dimension"
embedding = OpenAIEmbeddings(
    model="text-embedding-3-small",
    dimensions=32   # <-- correct
)

result = embedding.embed_query("Delhi is the capital of India")

print(len(result))   # should print 32
print(result)        # embedding vector
