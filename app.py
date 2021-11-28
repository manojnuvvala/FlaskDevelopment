from src.app import create_app

app = Flask(__name__)
if __name__ == "__main__":
    app = create_app()
    app.run()
