# Coding Challenge: **Survey Response Chatbot Server**

## Objective  
This project is a FastAPI-based application designed to handle survey responses through a chatbot interface and provide admin controls for managing surveys and responses. The project is structured to ensure scalability, maintainability, and separation of concerns.

---

## Project Structure
The project is organized as follows:

![alt text](<project-structure.png>)

## Setup Instructions
Follow these steps to set up and run the project:
#### 1. Create a Virtual Environment
It is recommended to use a virtual environment to manage dependencies:
```
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate 
```
#### 2. Install Dependencies
Install the required Python packages using pip:
```
pip install -r requirements.txt
```
#### 3. Run the Application
Start the FastAPI application:
```
uvicorn app.main:app --reload
```
---
## Usage  

### Chatbot WebSocket
The chatbot interface is accessible via WebSocket at:
```
ws://127.0.0.1:8000/ws/{customer_id}/{survey_id}
```
Replace {customer_id} and {survey_id} with the appropriate values. For example (using WebSocket client `websocat`):
```
websocat ws://127.0.0.1:8000/ws/1/ice_cream_preferences
```

### Admin REST API
The admin API provides endpoints for managing surveys and responses. You can use tools like curl, Postman, or any HTTP client to interact with these endpoints:
<details>
  <summary>List all surveys: GET /admin/surveys</summary>

```
curl -X GET http://127.0.0.1:8000/admin/surveys
```

</details>
<details>
  <summary>Create a survey: POST /admin/surveys</summary>
  
```
curl -X POST http://127.0.0.1:8000/admin/surveys \
     -H "Content-Type: application/json" \
     -d '{"survey_id": "car_preferences", "questions": [{"id": 1, "question": "What is your favorite car brand?", "options": ["Lexus", "Audi", "BMW"]}]}'
```

</details>
<details>
  <summary>Update a survey: PUT /admin/surveys/{survey_id}</summary>
  
```
curl -X PUT http://127.0.0.1:8000/admin/surveys/car_preferences \
     -H "Content-Type: application/json" \
     -d '{"questions": [{"id": 1, "question": "What is your favorite car color?", "options": ["White", "Black", "Silver"]}]}'
```

</details>
<details>
  <summary>Delete a survey: DELETE /admin/surveys/{survey_id}</summary>
  
```
curl -X DELETE http://127.0.0.1:8000/admin/surveys/ice_cream_preferences
```

</details>
<details>
  <summary>List all survey responses: GET /admin/survey_responses</summary>
  
```
curl -X GET http://127.0.0.1:8000/admin/survey_responses
```

</details>

---

## Testing

The project includes both manual and automated tests.  

#### 1. Run Automated Tests
To run the unit tests, use pytest: 
```
pytest
```
This will execute all automated test files in the tests/ directory, including:

- `test_admin_router.py`: Tests for admin API routes.
- `test_chatbot_router.py`: Tests for chatbot API routes.

#### 2. Manual Testing
For manual testing of the chatbot, use the `manual_test_chatbot.py` script:
```
python tests/manual_test_chatbot.py
```
This script simulates a WebSocket interaction with the chatbot.

---

## Design Decisions

#### 1. Separation of Concerns
The project is structured to separate routing, business logic, and utility functions:

- **Routers**: Handle API endpoints (`admin_router.py`, `chatbot_router.py`).
- **Services**: Contain business logic (`admin_service.py`, `chatbot_service.py`).
- **Utilities**: Provide reusable helper functions (`rpc_retrier_wrapper.py`, `surveys.py`).

This ensures that the code is modular, maintainable, and easy to extend. 

#### 2. Retry Logic
The *RPCRetrier* utility is used to handle transient failures in RPC calls. It retries failed operations up to a configurable number of attempts, improving the system's resilience.

#### 3. Mock Database
I kept the Mock Database in use with the same RPC failure rate but organized the file for better clarity and added more functionalities.

#### 4. WebSocket for Chatbot
The chatbot uses WebSocket for real-time interaction with users. This allows for a conversational interface that is responsive and user-friendly.

---

## Future Improvements  

- **Database Integration:** Replace the mock database with a real database (e.g., PostgreSQL, MongoDB).
- **Unit Tests:** Create unit tests for additional layers beyond just routers and their responses.
- **Authentication:** Add authentication and authorization for admin and chatbot endpoints.
- **Frontend:** Develop a frontend interface for interacting with the chatbot and admin controls.
- **Error Handling:** Enhance error handling and logging for better debugging and monitoring.

---

## Video Explanation

