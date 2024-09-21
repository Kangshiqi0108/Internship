from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
import weaviate
from weaviate.embedded import EmbeddedOptions
from langchain.prompts import ChatPromptTemplate
from langchain_community.chat_models import ChatOllama
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser
from langchain_community.vectorstores import Weaviate
import requests
from langchain_chroma import Chroma
loader = TextLoader('./state_of_the_union.txt')
print('loader.load()')
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
print('text_splitter')
chunks = text_splitter.split_documents(documents)
print('split_documents')
# 初始化向量数据库并嵌入目标文档

vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=OllamaEmbeddings(model="phi3:3.8b"),
    persist_directory="./vector_store"
)


# vectorstore = Chroma(persist_directory="./vector_store", embedding_function=OllamaEmbeddings(model="phi3"))
print('vectorstore')
# 检索器
#retriever = vectorstore.as_retriever()
retriever = vectorstore.as_retriever(search_kwargs={"k": 10})
print('retriever')
# LLM提示模板
template = """You are an assistant for question-answering tasks. 
   Use the following pieces of retrieved context to answer the question. 
   If you don't know the answer, just say that you don't know. 
   Use three sentences maximum and keep the answer concise.
   Question: {question} 
   Context: {context} 
   Answer:
   """
prompt = ChatPromptTemplate.from_template(template)
print('prompt')
llm = ChatOllama(model="phi3:3.8b", temperature=10)
rag_chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
)
# 开始查询&生成
query = "What did the president mainly say?"
print(rag_chain.invoke(query))