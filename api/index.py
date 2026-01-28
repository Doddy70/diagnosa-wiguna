import os
import sys

# Ensure the project root is in sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

# Vercel serverless function entry point
if __name__ == "__main__":
    app.run()

# Local test helper
if __name__ == "__main__":
    try:
        from wsgiref.simple_server import make_server
        print("Starting diagnostic server on port 8000...")
        with make_server('', 8000, app) as httpd:
            httpd.serve_forever()
    except KeyboardInterrupt:
        pass
