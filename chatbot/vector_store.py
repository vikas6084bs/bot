from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_classic.schema import Document
from langchain_classic.text_splitter import CharacterTextSplitter

def create_vector_store(conn, tables, schema, openai_api_key=None):
    documents = []
    cursor = conn.cursor()

    for table in tables:
        schema_text = f"Table {table} has columns: {', '.join([f'{col[0]} ({col[1]})' for col in schema[table]])}"
        documents.append(Document(page_content=schema_text, metadata={"type": "schema", "table": table}))

        try:
            cursor.execute(f"SELECT * FROM {table} LIMIT 10")
            sample_data = cursor.fetchall()
            if sample_data:
                columns = [desc[0] for desc in cursor.description]
                for row in sample_data:
                    row_text = f"In {table}: {dict(zip(columns, row))}"
                    documents.append(Document(page_content=row_text, metadata={"type": "data", "table": table}))
        except Exception:
            continue

    cursor.close()

    # Use text splitter for chunking
    text_splitter = CharacterTextSplitter(chunk_size=400, chunk_overlap=50)
    split_documents = []
    for doc in documents:
        chunks = text_splitter.split_text(doc.page_content)
        for chunk in chunks:
            split_documents.append(Document(page_content=chunk, metadata=doc.metadata))

    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key) if openai_api_key else HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vector_store = Chroma.from_documents(split_documents, embeddings)

    return vector_store
