import uvicorn

# Importing app here makes the syntax cleaner as it will be picked up by refactors
from main import app

if __name__ == "__main__":
    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True)