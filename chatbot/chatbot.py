from .db_connection import get_db_connection
from .schema_loader import load_detailed_schema
from .vector_store import create_vector_store
from .query_generator import QueryGenerator
from .query_executor import QueryExecutor
from langchain_classic.schema import Document
from langchain_classic.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings, HuggingFaceEmbeddings
import re
import psycopg2

class ImprovedDBChatbot:
    def __init__(self, openrouter_api_key, db_config, openai_api_key=None):
        self.openrouter_api_key = openrouter_api_key
        self.openai_api_key = openai_api_key

        self.conn = get_db_connection(db_config)

        self.tables, self.schema = load_detailed_schema(self.conn)
        self.vector_store = create_vector_store(self.conn, self.tables, self.schema, openai_api_key)
        self.query_generator = QueryGenerator(openrouter_api_key)
        self.query_executor = QueryExecutor(self.conn)

    def _semantic_search(self, question, k=5):
        try:
            return self.vector_store.similarity_search(question, k=k)
        except Exception:
            return []

    def _get_enhanced_context(self, question):
        schema_context = "DATABASE SCHEMA:\n"
        for table in self.tables:
            schema_context += f"Table: {table}\nColumns: {', '.join([col[0] for col in self.schema[table]])}\n"

        similar_docs = self._semantic_search(question)
        if similar_docs:
            schema_context += "\nRELEVANT DATA SNIPPETS:\n"
            for doc in similar_docs[:3]:
                schema_context += f"- {doc.page_content}\n"

        return schema_context

    def _clean_sql(self, sql):
        sql = re.sub(r'``````|`', '', sql).strip()
        sql = sql.split(';')[0].strip()
        return sql

    def _generate_smart_sql(self, question):
        context = self._get_enhanced_context(question)

        messages = [
            {
                "role": "system",
                "content": (
                    "You are an expert SQL generator for PostgreSQL. "
                    "Given the database schema and relevant data snippets, generate an accurate SQL query "
                    "that answers the user's question. Return ONLY the SQL query, no explanations."
                )
            },
            {
                "role": "user",
                "content": f"""Database Context:
{context}

User Question:
{question}

Generate the SQL query:"""
            }
        ]

        sql = self.query_generator._call_openrouter_api(messages, temperature=0.1)
        return self._clean_sql(sql)

    def ask(self, question):
        if not question or not question.strip():
            return "Please ask a question about the database."

        question = question.strip()

        if self._is_general_conversation(question):
            return self._handle_general_conversation(question)

        sql = self._generate_smart_sql(question)
        if sql.startswith('Error'):
            return "I'm having trouble connecting to the AI service. Please try again."

        return self.query_executor.execute_with_smart_matching(question, sql)

    def _is_general_conversation(self, question):
        question_lower = question.lower().strip()
        general_phrases = ['hello', 'hi', 'hey', 'how are you', 'bye', 'goodbye', 'help', 'what can you do']
        return any(phrase in question_lower for phrase in general_phrases)

    def _handle_general_conversation(self, question):
        question_lower = question.lower().strip()

        if any(greeting in question_lower for greeting in ['hello', 'hi', 'hey']):
            return "Hello! I can help you query your database."
        elif 'how are you' in question_lower:
            return "I'm ready to help you with your database queries."
        elif 'help' in question_lower:
            return "I can answer questions about your database using natural language."
        elif any(farewell in question_lower for farewell in ['bye', 'goodbye']):
            return "Goodbye!"
        else:
            return "I'm here to help you with database queries."

    def close(self):
        if hasattr(self, 'conn') and self.conn:
            self.conn.close()
