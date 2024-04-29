from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

openai_key = os.getenv("OPENAI_API_KEY")


# Function to evaluate and suggest improvements for a product description
async def evaluate_description(description):
    llm = ChatOpenAI(temperature=0.5, openai_api_key=openai_key)  # Adjust the temperature as needed
    prompt = PromptTemplate(
        input_variables=["description"],
        template="Evaluate this product description and suggest improvements: '{description}'"
    )
    chain = LLMChain(llm=llm, prompt=prompt)
    response = await chain.ainvoke({'description': description})
    if 'text' in response:
        return response['text']
    else:
        return "No improvement suggestions available."
    
async def regenerate_description(description):
    llm = ChatOpenAI(temperature=0.7, openai_api_key=openai_key)
    prompt = PromptTemplate(
        input_variables=["description"],
        template="Generate a new, improved product description based on: '{description}'"
    )
    chain = LLMChain(llm=llm, prompt=prompt)
    response = await chain.ainvoke({'description': description})
    return response.get('text', 'No new description available.')

