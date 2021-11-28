from src.app import create_app
from flask import Flask
app = Flask(__name__)
if __name__ == "__main__":
    app = create_app()
    app.run()
