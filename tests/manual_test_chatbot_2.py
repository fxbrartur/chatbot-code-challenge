import asyncio
import websockets


async def interactive_chatbot():
    uri = "ws://127.0.0.1:8000/ws/2/customer_satisfaction"  # Replace "2" with the desired customer ID and customer_satisfaction with the desired survey ID
    async with websockets.connect(uri) as websocket:
        print("Connected to the chatbot! Waiting for the first question...\n")

        while True:
            # Receive a message from the chatbot
            message = await websocket.recv()
            print(message)

            # Check if the conversation is completed
            if "Thank you for your time" in message:
                print("\nConversation ended. Thank you!")
                break

            # Send a manual response
            answer = input("\nYour answer: ")
            await websocket.send(answer)

# Run the script
asyncio.run(interactive_chatbot())