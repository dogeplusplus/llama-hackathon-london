import os
import uvicorn

from uuid import uuid4
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from fastapi.responses import JSONResponse
from backend.database import DatabaseInterface
from backend.processing import ModelInterface
from backend.models import Summarize, Exercises, Question

app = FastAPI()

# origins = [
#     "*",
#     "http://localhost:5173",
#     "http://127.0.0.1:5173",
#     "https://localhost:5173",
# ]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
#     expose_headers=["*"],
# )

def wrap_response(data, status_code=200):
    response = JSONResponse(
        content=data,
        status_code=status_code,
    )
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "*"
    return response

UPLOAD_DIRECTORY = "uploads"
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)
app = FastAPI()
db = DatabaseInterface(os.environ.get("POSTGRES_STR"))
model = ModelInterface(os.environ.get("GROQ_API_KEY"))


@app.post("/upload/")
async def upload_pdf(file: UploadFile = File(...)):
    # Generate a unique ID for the file
    file_id = str(uuid4())
    file_path = os.path.join(UPLOAD_DIRECTORY, f"{file_id}.pdf")
    
    # Save the uploaded file to the directory
    with open(file_path, "wb") as f:
        f.write(await file.read())
 
    book_id = db.add_book(book_path=file_path)

    return wrap_response({"book_id": book_id})


@app.post("/summarize/")
def summarize_text(data: Summarize = Depends()):
    book_path = db.get_book_path(data.book_hash)
    
    summary = model.create_summary(
        book_path=book_path,
        page=data.page,
    )
    return wrap_response({"summary": summary})
    
    
@app.get("/summary/")
def get_summary(data: Summarize = Depends()):
    summary = db.get_summary(data.book_hash, data.page)
    return wrap_response({"summary": summary})


@app.post("/exercises/")
def create_exercises(data: Exercises = Depends()):
    book_path = db.get_book_path(data.book_hash)
    exercises = model.create_exercises(
        book_path=book_path,
        page=data.page,
    )
    for exercise in exercises:
        db.add_exercise(
            book_hash=data.book_hash,
            page=exercise["page"],
            exercise_id=str(uuid4()),
            question=exercise["question"],
            answer=exercise["answer"],
        )
    
    return wrap_response({
        "exercises": exercises,
    })


@app.get("/revision/")
def get_exercises(data: Exercises = Depends()):
    exercises = db.get_exercises(data.book_hash)
    return wrap_response({"exercises": exercises})


@app.post("/question/")
def question(data: Question = Depends()):
    book_path = db.get_book_path(data.book_hash)
    answer = model.question(
        book_path=book_path,
        page=data.page,
        question=data.question,
        highlighted_text=data.highlighted_text,
    )
    
    return wrap_response({
        "answer": answer,
    })


if __name__ == "__main__":
    uvicorn.run("server:app", host="localhost", port=8000, reload=True)
                

