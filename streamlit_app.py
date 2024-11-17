import streamlit as st
import requests
import pandas as pd
import streamlit_pdf_viewer as spv

st.set_page_config(page_title="spicy doge", layout="wide")
title = st.write("spicy doge")
left, right = st.columns(2)

def summarize_page(book_hash: str, page: int):
    url = "http://localhost:8000/summarize"
    response = requests.post(
        url,
        params={
            "book_hash": book_hash,
            "page": page
        }
    )
    return response.json()["summary"]


def upload_pdf_to_server(pdf: bytes):
    url = "http://localhost:8000/upload"
    files = {
        "file": pdf
    }
    response = requests.post(url, files=files)
    response = response.json()
    st.session_state.book_hash = response["book_hash"]
    return response


def question(question: str, book_hash: str, page: int):
    url = "http://localhost:8000/question"
    response = requests.post(
        url,
        params={
            "question": question,
            "book_hash": book_hash,
            "page": page,
            "highligthed_text": None,
        }
    )
    return response.json()


def expand_on_highlighted_text(book_hash: str, page: int, text: str):
    url = "http://localhost:8000/expand"
    response = requests.post(
        url,
        params={
            "book_hash": book_hash,
            "page": page,
            "highligthed_text": text,
            "question": None,
        }
    )
    return response.json()

def create_exercises(book_hash: str, page: int):
    url = "http://localhost:8000/exercises"
    response = requests.post(
        url,
        params={
            "book_hash": book_hash,
            "page": page,
        }
    )
    return pd.DataFrame(response.json()["exercises"])


with left:
    pdf_uploader = st.file_uploader("Upload a PDF file", type=["pdf"])
    
with right:
    if pdf_uploader:
        page_selector = st.number_input("Select a page number", min_value=1, value=1)
        pdf_viewer = spv.pdf_viewer(pdf_uploader.getvalue(), pages_to_render=[page_selector], render_text=True)
        book_hash = upload_pdf_to_server(pdf_uploader.getvalue())

summarize_button = st.button("Summarize")
exercises_button = st.button("Create exercises")

if summarize_button:
    summary = summarize_page(st.session_state.book_hash, page_selector)
    left.write(summary)
    
if exercises_button:
    exercises = create_exercises(st.session_state.book_hash, page_selector)
    left.table(exercises)

