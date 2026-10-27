# URL Shortener API

## About the Project

This project is a URL Shortener API developed using Python and FastAPI. It converts long URLs into short links and stores URL information in an SQLite database.

## Technologies Used

* Python
* FastAPI
* SQLite
* Pydantic

## Features

* Shorten long URLs
* Generate unique short codes
* Store URLs in an SQLite database
* Redirect users to the original URL

## Requirements

Install the required libraries:

```bash
pip install fastapi uvicorn pydantic
```

## How to Run

1. Save the Python code as `main.py`.
2. Open the terminal in the project folder.
3. Run the following command:

```bash
uvicorn main:app --reload
```

4. Open this URL in your browser:

```text
http://127.0.0.1:8000/docs
```

## Author

Anurag Kumar

## License

This project is created for learning purposes.
