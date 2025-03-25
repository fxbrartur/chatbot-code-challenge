import asyncio
import websockets

# WebSocket URL
WEBSOCKET_URL = "ws://localhost:8000/ws/1/ice_cream_preferences"

# Centralized error message
TECHNICAL_DIFFICULTIES_MESSAGE = "We are experiencing technical difficulties. Please try again later."
CUSTOMER_NOT_FOUND_MESSAGE = "Customer not found."
SURVEY_NOT_FOUND_MESSAGE = "Survey not found."

async def interactive_chatbot():
    retry_attempts = 3  # Maximum number of reconnection attempts
    attempt = 0

    while attempt < retry_attempts:
        try:
            # Connect to the WebSocket
            async with websockets.connect(WEBSOCKET_URL) as websocket:
                print("Connected to the chatbot! Waiting for the first question...\n")

                while True:
                    try:
                        # Receive a message from the server
                        message = await websocket.recv()
                        print(message)

                        # Check if the server sent an error message
                        if TECHNICAL_DIFFICULTIES_MESSAGE in message:
                            print("The server is experiencing technical difficulties. Closing connection.")
                            return  # End the manual test

                        # Check if the server sent "Customer not found" or "Survey not found"
                        if CUSTOMER_NOT_FOUND_MESSAGE in message or SURVEY_NOT_FOUND_MESSAGE in message:
                            print("The server could not proceed. Closing connection.")
                            return  # End the manual test

                        # Check if the conversation is completed
                        if "Thank you for your time" in message:
                            print("\nConversation ended. Thank you!")
                            return  # Exit both loops and end the script

                        # Prompt the user for a response
                        user_input = input("Your answer: ")
                        await websocket.send(user_input)

                    except websockets.exceptions.ConnectionClosedOK:
                        print("Connection closed by the server. Ending session.")
                        return  # End the manual test

        except websockets.exceptions.ConnectionClosedError as e:
            print(f"Connection error: {e}. Retrying... Attempt {attempt + 1} of {retry_attempts}")
            attempt += 1
            await asyncio.sleep(1)  # Wait before retrying

        except Exception as e:
            print(f"Unexpected error: {e}")
            return  # End the manual test in case of an unexpected error

    print("Failed to connect after multiple attempts. Please try again later.")

# Run the manual test
if __name__ == "__main__":
    asyncio.run(interactive_chatbot())