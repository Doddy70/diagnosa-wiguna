import os
import sys

# Ensure the project root is in sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

# Vercel serverless function entry point
if __name__ == "__main__":
    app.run()
