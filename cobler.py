from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from llama_index.llms.openai import OpenAI
from llama_index.core.llms import ChatMessage
import os
import config

# Initialize FastAPI
app = FastAPI()

# Set up Jinja2 for rendering templates
templates = Jinja2Templates(directory="templates")

# Set your OpenAI API key
os.environ["OPENAI_API_KEY"] = config.API_DETAILS["openai_api_key"]

# Initialize the LLM
llm = OpenAI(model="gpt-4", temperature=0.3)

@app.get("/", response_class=HTMLResponse)
async def get_form(request: Request):
    return templates.TemplateResponse("index_cobler.html", {"request": request})

@app.post("/", response_class=HTMLResponse)
async def convert_cobol(request: Request, cobol_code: str = Form(...)):
    # Compose system prompt dynamically
    system_prompt = (
        "You are a skilled software engineer experienced in both COBOL and Python.\n"
        "Convert the COBOL code below into clean, idiomatic Python code. "
        "Preserve the logic as closely as possible. If any part of the COBOL is ambiguous, make reasonable assumptions.\n"
        "---------------------\n"
        f"{cobol_code}\n"
        "---------------------\n"
        "Python Code:"
    )

    # Create chat messages
    messages = [
        ChatMessage(role="system", content=system_prompt),
        ChatMessage(role="user", content="convert cobol code into python code"),
    ]

    # Get the response
    response = llm.chat(messages)

    return templates.TemplateResponse("index_cobler.html", {
        "request": request,
        "cobol_code": cobol_code,
        "python_code": response.message.content
    })
