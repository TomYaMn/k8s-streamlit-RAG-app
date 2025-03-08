import streamlit as st
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import ChatPromptTemplate
from langchain_chroma import Chroma
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.storage import LocalFileStore
from langchain.storage._lc_store import create_kv_docstore
from langchain.retrievers.multi_vector import MultiVectorRetriever
import base64
import chromadb

# Helper functions
def is_base64(s):
    try:
        return base64.b64encode(base64.b64decode(s)).decode() == s
    except Exception:
        return False

def parse_docs(docs):
    b64 = []
    text = []
    for doc in docs:
        if isinstance(doc.page_content, str) and is_base64(doc.page_content):
            b64.append(doc.page_content)
        else:
            text.append(doc.page_content)
    return {"images": b64, "texts": text}

def build_prompt(kwargs):
    docs_by_type = kwargs["context"]
    user_question = kwargs["question"]
    context_text = "\n".join(docs_by_type["texts"])
    prompt_template = f"""
    Answer the question based only on the following context.
    Context: {context_text}
    Question: {user_question}
    """
    prompt_content = [{"type": "text", "text": prompt_template}]
    if len(docs_by_type["images"]) > 0:
        for image in docs_by_type["images"]:
            prompt_content.append(
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image}"}}
            )
    return ChatPromptTemplate.from_messages([HumanMessage(content=prompt_content)])

# Initialize OpenAI Embeddings
embedding_function = OpenAIEmbeddings()
chroma_client = chromadb.HttpClient(host="localhost", port=8000)
vectorstore = Chroma(client=chroma_client, collection_name="multi_modal_rag", embedding_function=embedding_function)
store_path = "./store_document"
fs = LocalFileStore(store_path)
docstore = create_kv_docstore(fs)
retriever = MultiVectorRetriever(vectorstore=vectorstore, docstore=docstore, id_key="doc_id")

# Define RAG pipeline
chain_with_sources = {
    "context": retriever | RunnableLambda(parse_docs),
    "question": RunnablePassthrough(),
} | RunnablePassthrough().assign(
    response=(RunnableLambda(build_prompt) | ChatOpenAI(model="gpt-4o-mini") | StrOutputParser())
)

# Streamlit App
st.title("AI Chatbot with RAG")
user_query = st.text_input("Ask a question:")
if st.button("Submit"):
    if user_query:
        response = chain_with_sources.invoke(user_query)
        st.subheader("Response:")
        st.write(response['response'])
        st.subheader("Retrieved Images:")
        for image in response['context']['images']:
            st.image(base64.b64decode(image), use_column_width=True)
