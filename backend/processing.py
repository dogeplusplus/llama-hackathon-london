import io
import json
import base64
import pymupdf

from typing import List, Optional
from functools import lru_cache
from PIL import Image
from groq import Groq
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


@lru_cache(maxsize=None)
def extract_page_content(pdf_path: str, page: int):
    doc = pymupdf.open(pdf_path)
    images = extract_images(doc, page)
    text = doc[int(page)].get_text()
    doc.close()
    content = [
        {"type": "text", "text": text}
    ]
    if len(images) > 0:
        content.append({
            "type": "image_url",
            "image_url": {"url": f"data:image/jpeg;base64,{encode_image(images[0])}"},
        })
        
    return content


@lru_cache(maxsize=None)
def extract_images(pdf_path: pymupdf.Document, page: int) -> List[Image.Image]:
    pdf = pymupdf.open(pdf_path)
    image_list = pdf[int(page)].get_images(full=True)
    images = []
    for img in image_list:
        data = pdf.extract_image(img[0])
        image_pil = Image.open(io.BytesIO(data.get("image")))
        images.append(image_pil)
        
    return images 

 
def encode_image(image: Image) -> str:
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')


class ModelInterface:
    def __init__(self, key: str, model: str = "llama-3.2-11b-vision-preview"):
        self.client = Groq(api_key=key)
        self.model = model
 
    def create_summary(self, book_path: str, page: int):
        instruction = "Summarize the text in this page. Keep it brief"
        content = extract_page_content(book_path, page)
        prompt = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": instruction},
                ] + content,
            },
        ]
        
        chat_completion = self.client.chat.completions.create(
            messages=prompt,
            model=self.model,
        )
        
        return chat_completion.choices[0].message.content

    def create_exercises(self, book_path: str, page: int):
        instruction = """
        Generate exercises based on the text in this page. Create them in a json format that can be parsed easily:
        {
            1: {
                "question": "What is the capital of France?",
                "answer": "Paris"
            },
            2: {
                "question": "What is the capital of Germany?",
                "answer": "Berlin"
            }
        }
        """
        content = extract_page_content(book_path, page)
        prompt = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": instruction},
                ] + content,
            },
        ]

        chat_completion = self.client.chat.completions.create(
            messages=prompt,
            model=self.model,
        )
        
        result = json.loads(chat_completion.choices[0].message.content)
        return result

    def question(
        self,
        book_path: str,
        page: int,
        question: Optional[str] = None,
        highlighted_text: Optional[str] = None,
    ):
        page_content = extract_page_content(book_path, page)
        if question:
            instruction= """
            Answer the following query to the best of your ability. Use the content in the page to help you
            answer.
            """
            prompt = [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": instruction},
                        {"type": "text", "text": f"Question: {question}"},
                    ] + page_content,
                },
            ]
        elif highlighted_text:
            instruction= """
            Elaborate on the selected text. Provide more information on the topic.
            There is additional content in the page that you can use to elaborate on the selected text.
            """
            prompt = [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": instruction},
                        {"type": "text", "text": f"Selected text: {highlighted_text}"},
                    ] + page_content,
                },
            ]
        else:
            raise ValueError("Either question or highlighted_text must be provided")
            
        chat_completion = self.client.chat.completions.create(
            messages=prompt,
            model=self.model,
        )

        return chat_completion.choices[0].message.content 
