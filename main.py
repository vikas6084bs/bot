from chatbot.chatbot import ImprovedDBChatbot
from chatbot.config import OPENROUTER_API_KEY, DB_CONFIG, OPENAI_API_KEY

def main():
    print("Database Chatbot - Ask questions about your database")
    print("Type 'quit' to exit")

    chatbot = ImprovedDBChatbot(OPENROUTER_API_KEY, DB_CONFIG, OPENAI_API_KEY)

    while True:
        try:
            query = input("\nYou: ").strip()
            if query.lower() == 'quit':
                break
            if query:
                response = chatbot.ask(query)
                print(f"Assistant: {response}")
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Assistant: I encountered an error. Please try again.\nError: {str(e)}")

    chatbot.close()

if __name__ == "__main__":
    main()
