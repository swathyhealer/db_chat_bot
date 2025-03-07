from google import genai
from google.genai import types
import os
import json
from tools import insert_invoice ,show_invoice,update_invoice, get_last_week_invoices


api_key = os.getenv("GEMINI_API_KEY")


class GeminiAgentWithRAGTool:
    def __init__(self):
        self.__client__ = genai.Client(api_key=api_key)

        safety_settings = [
            types.SafetySetting(
                category="HARM_CATEGORY_DANGEROUS_CONTENT",
                threshold="BLOCK_ONLY_HIGH",
            ),
        ]
        self.__config__ = types.GenerateContentConfig(
            temperature=0,
            seed=5,
            safety_settings=safety_settings,
            tools=[insert_invoice,show_invoice,update_invoice,get_last_week_invoices],
            system_instruction="""
You are an AI-powered invoice management assistant. Your role is to help users insert, update, view, and summarize invoices in a database. Follow these guidelines:

Core Functionalities:

1. Insert Invoice:
    When a user provides invoice details, transform them into JSON format.
    Call the insert_invoice(json_data) function to store the invoice in the database.
    ### Parameter:
    - **json_data**: containing details of the invoice:
        ```json
        {
            "id": "<invoice id>",
            "customer_name": "customer name",
            "date": "<date in YYYY-MM-DD>",
            "total_amount": <total amount in invoice>,
            "items": [<lineitem 1>, <lineitem 2>]
        }
        ```

2. Update Invoice:
    Retrieve the most recent invoice from the conversation unless the user specifies a different invoice.
    Extract updated_data in given format from user input (ingore fields that are not given)
    Call the update_invoice(invoice_id, updated_data) function with the necessary modifications.
    ### Parameters:
        - **invoice_id**: Id of the invoice which will be an integer
        - **updated_data**: containing details of the invoice that needs to get updated:
                ```json
                {
                    "id": "<invoice id>",
                    "customer_name": "customer name",
                    "date": "<date in YYYY-MM-DD>",
                    "total_amount": <total amount in invoice>,
                    "items": [<lineitem 1>, <lineitem 2>]
                }
                ```
3. Show Invoice:
    If a user requests to see an invoice, retrieve the most recent one from the conversation or use a specified invoice ID.
    Call the show_invoice(invoice_id) function to display the invoice.
    ### Parameter:
    - **invoice_id**: Id of the invoice which will be an integer
4. Summarize Invoices:
    When the user requests an invoice summary, call  get_last_week_invoices function.
    Provide a clear concise summary of all stored invoices.

General Rules:
    Always ensure invoices are formatted correctly before inserting or updating them.
    Confirm updates with the user before making changes.
    If an invoice is not found, ask for clarification or suggest recent invoices.
    Keep responses clear and concise while maintaining accuracy.
    Ensure all JSON data follows a valid structure before calling functions.

""",
        )
        self.__chat__ = self.__client__.chats.create(
            model="gemini-2.0-flash", history=[], config=self.__config__
        )

    def send_msg(self, user_input):
        response = self.__chat__.send_message(user_input)
        try:
            response = response.text
        except Exception as e:
            # print("exception:", e)
            response = "I don't know"

        return response

    def get_history(self):

        chat_data = []

        for chat_item in self.__chat__._curated_history:
            chat_entry = {"role": chat_item.role, "parts": []}

            for i, part in enumerate(chat_item.parts):
                part_data = {
                    "function_call": str(part.function_call),
                    "function_response": str(part.function_response),
                    "text": part.text,
                }
                chat_entry["parts"].append(part_data)

            chat_data.append(chat_entry)

        # Writing to JSON file
        with open("complete_workflow_history.json", "w", encoding="utf-8") as f:
            json.dump(chat_data, f, indent=4, ensure_ascii=False)

        print("Chat history saved to chat_history.json")





# agent2= GeminiAgentWithRAGTool()
# # response = agent2.send_msg("""insert invoice {
# #             "id": 888,
# #             "customer_name": "swathy",
# #             "date": "2025-02-07",
# #             "total_amount": 630,
# #             "items": []
# #         }""")
# # print(response)
# response = agent2.send_msg("""get summary of invoices""")
# print(response)

# response = agent2.send_msg("""yes""")

# print(response)