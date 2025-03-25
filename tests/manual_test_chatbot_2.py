import asyncio
import websockets


async def interactive_chatbot():
    uri = "ws://127.0.0.1:8000/ws/1/ice_cream_preferences"  # Change the survey ID as needed
    max_retries = 3  # Maximum number of retries for RPC failures
    retry_count = 0  # Current retry attempt

    async with websockets.connect(uri) as websocket:
        print("Connected to the chatbot! Waiting for the first question...\n")

        while True:
            # Receive a message from the chatbot
            message = await websocket.recv()
            print(message)

            # Check if the survey was not found
            if "Survey not found" in message:
                print("\nThe requested survey does not exist. Please check the survey ID and try again.")
                break

            # Check if there was an RPC failure
            if "We are experiencing technical difficulties." in message:
                retry_count += 1
                if retry_count > max_retries:
                    print("\nThe chatbot encountered repeated technical issues and cannot continue. Please try again later.")
                    break
                else:
                    print(f"\nRetrying... Attempt {retry_count} of {max_retries}")
                    continue  # Retry by waiting for the next message

            # Reset retry count on successful message
            retry_count = 0

            # Check if the conversation is completed
            if "Thank you for your time" in message:
                print("\nConversation ended. Thank you!")
                break

            # Send a manual response
            answer = input("\nYour answer: ")
            await websocket.send(answer)

# Run the script
asyncio.run(interactive_chatbot())