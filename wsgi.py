import os
from dotenv import load_dotenv, find_dotenv
from wizard import app

load_dotenv(find_dotenv())


if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=5000
    )