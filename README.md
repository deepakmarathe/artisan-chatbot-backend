# artisan-chatbot-backend

## Overview
This is a backend application built using FastAPI, a modern, fast (high-performance), web framework for building APIs with Python 3.6+ based on standard Python type hints.

## Requirements
- Python 3.6+
- pip (Python package installer)

## Installation
1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/artisan-chatbot-backend.git
    cd artisan-chatbot-backend
    ```

2. Create a virtual environment:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Running the Application
To run the application, use the following command:
```sh
uvicorn chatbot.server:app --reload