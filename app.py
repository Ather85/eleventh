# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "fastapi",
#   "uvicorn",
#   "pandas",
#   "python-multipart"
# ]
# ///

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from typing import List, Optional

app = FastAPI()

# Enable CORS for GET requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

# Load CSV data once at startup
df = pd.read_csv("students.csv")  # CSV has columns studentId,class

@app.get("/api")
async def get_students(class_: Optional[List[str]] = Query(None, alias="class")):
    data = df
    if class_:
        data = data[data['class'].isin(class_)]
    # Convert to list of dicts in the same order as CSV
    students_list = data.to_dict(orient="records")
    return {"students": students_list}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
