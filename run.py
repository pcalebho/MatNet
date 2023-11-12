from app import create_app
import os
from dotenv import load_dotenv

load_dotenv()

app = create_app(test_config=os.environ.get('CONFIG'))

if __name__ == "__main__":
    app.run()