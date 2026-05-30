from langchain_groq.chat_models import ChatGroq
from dotenv import load_dotenv

load_dotenv()

llm=ChatGroq(model="meta-llama/llama-4-scout-17b-16e-instruct")

