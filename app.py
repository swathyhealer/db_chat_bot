import os
from agent import GeminiAgentWithRAGTool

api_key = os.getenv("GEMINI_API_KEY")


def run_agent():

    chat_agent = GeminiAgentWithRAGTool()

    print("invoice management assistant (Type 'exit' to quit)")
    while True:
        query = input("You: ")
        if query.lower() == "exit":
            print("Goodbye!")
            break
        response = chat_agent.send_msg(query)

        print("invoice management assistant :", str(response))


if __name__ == "__main__":
    run_agent()