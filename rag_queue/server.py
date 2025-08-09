from fastapi import FastAPI,Query
from .queue.connection import queue
from .queue.worker import process_query

app = FastAPI()


@app.get("/")
def root():
    return {"Status":'Server is up and running'}

@app.post('/chat')
def chat(
    query: str = Query(..., description="Chat Message")
):
    # Query ko Queue mei dall do
   
    job = queue.enqueue(process_query, queue) # process_query(query)
    
     # User ko bolo your job received
    return{"status": "queued","job_id":job.id}
