import os
import sys
import traceback

# Ensure the project root is in sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from app import app
except Exception as e:
    # Fallback WSGI app to display the error
    error_msg = f"Failed to start application:\n{traceback.format_exc()}"
    print(error_msg)  # Ensure it goes to logs too
    
    def app(environ, start_response):
        status = '500 Internal Server Error'
        response_headers = [('Content-type', 'text/plain')]
        start_response(status, response_headers)
        return [error_msg.encode('utf-8')]

# Vercel serverless function entry point
if __name__ == "__main__":
    app.run()
