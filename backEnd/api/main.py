from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain_community.chat_models import ChatOllama
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser
from langchain_chroma import Chroma
from fastapi import FastAPI,Form,Body
from fastapi.middleware.cors import CORSMiddleware
origins = ["*"]
template = """You are an assistant for question-answering tasks. 
   Use three sentences maximum and keep the answer concise.
   Question: {question} 
   Answer:
   """
prompt = ChatPromptTemplate.from_template(template)
llm = ChatOllama(model="phi3:3.8b", temperature=10)
rag_chain = (
        {"question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
)
query = "who are you?"
print(rag_chain.invoke(query))
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/q")
def get_answer():
    return rag_chain.invoke("hello")
@app.post("/q")
def post_query(query: str = Form(...)):
    return rag_chain.invoke(query)
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)