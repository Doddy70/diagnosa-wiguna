import os
import sys
import traceback

# Ensure the project root is in sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Global variable to hold the initialized Flask app
_flask_app = None

def app(environ, start_response):
    """
    WSGI handler that lazy-loads the Flask app.
    This allows catching import errors that would otherwise crash the Vercel worker startup.
    """
    global _flask_app
    
    if _flask_app is None:
        try:
            # Lazy import
            from app import app as initialized_app
            _flask_app = initialized_app
        except Exception:
            # Catch initialization/import errors and display them
            error_msg = f"Failed to initialize application:\n{traceback.format_exc()}"
            print(error_msg) # Log to Vercel console
            
            status = '500 Internal Server Error'
            response_headers = [('Content-type', 'text/plain; charset=utf-8')]
            start_response(status, response_headers)
            return [error_msg.encode('utf-8')]

    # Dispatch to the real Flask app
    return _flask_app(environ, start_response)

# Vercel serverless function entry point
if __name__ == "__main__":
    # Local development helper
    # Try importing normally for local run
    try:
        from app import app as local_app
        local_app.run(debug=True)
    except Exception as e:
        print(f"Local startup failed: {e}")
        traceback.print_exc()
