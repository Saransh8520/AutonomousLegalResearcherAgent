from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from config import DATA_PATH, CHROMA_DB_PATH

def initialize_db():
    loader = TextLoader(DATA_PATH)
    documents = loader.load()

    splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    db = Chroma.from_documents(
        docs,
        embeddings,
        persist_directory=CHROMA_DB_PATH
    )
    db.persist()

def retrieve_context(query):
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    db = Chroma(
        persist_directory=CHROMA_DB_PATH,
        embedding_function=embeddings
    )

    results = db.similarity_search_with_score(query, k=3)

    if not results:
        return "", 0

    best_score = results[0][1]  # lower = more similar
    context = "\n".join([doc.page_content for doc, score in results])

    return context, best_score