import asyncio
import websockets
import json


async def interactive_chatbot():
    uri = "ws://127.0.0.1:8000/ws/1"  # Replace "1" with the desired customer ID
    async with websockets.connect(uri) as websocket:
        print("Connected to the chatbot! Waiting for the first question...\n")

        while True:
            # Receive a message from the chatbot
            message = await websocket.recv()
            try:
                # Try to parse the message as JSON (chatbot question)
                data = json.loads(message)
                if "question" in data:
                    print(f"Bot: {data['question']}")
                    print(f"Options: {', '.join(data.get('options', []))}")
                else:
                    print(f"Bot: {message}")
            except json.JSONDecodeError:
                # If the message is not JSON, display it as plain text
                print(f"Bot: {message}")

            # Check if the conversation is completed
            if "Thank you for completing the survey!" in message:
                print("\nConversation ended. Thank you!")
                break

            # Send a manual response
            answer = input("\nYour answer: ")
            response = {
                "customer_id": "1",  # Replace with the correct customer ID if needed
                "question_id": data.get("id", 0),  # Current question ID
                "answer": answer
            }
            await websocket.send(json.dumps(response))

# Run the script
asyncio.run(interactive_chatbot())