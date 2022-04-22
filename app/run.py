import os

from app.main import create_app

app = create_app()


if __name__ == "__main__":
    app.run(host='0.0.0.0',  port=os.getenv('API_PORT', 8000), debug=True)


