import os
import sys
import traceback

def app(environ, start_response):
    status_msg = "Healthy"
    error_detail = "None"
    debug_info = ""
    
    try:
        # Debug Info Gathering
        cwd = os.getcwd()
        debug_info += f"CWD: {cwd}\n"
        debug_info += f"Sys Path: {sys.path}\n"
        
        try:
            debug_info += f"Root Dir Listing: {os.listdir(cwd)}\n"
        except:
            debug_info += "Could not list root dir\n"
            
        try:
            api_dir = os.path.join(cwd, 'api')
            if os.path.exists(api_dir):
                debug_info += f"API Dir Listing: {os.listdir(api_dir)}\n"
        except:
            pass

        # 1. Setup path
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        sys.path.append(project_root)
        debug_info += f"Project Root inferred: {project_root}\n"
        
        # 2. Try importing the app
        import app
        status_msg = "Import Successful"
    except Exception:
        status_msg = "Import Failed"
        error_detail = traceback.format_exc()

    output = f"Status: {status_msg}\n\nTraceback:\n{error_detail}\n\nDebug Info:\n{debug_info}\n".encode('utf-8')
    
    # Return 200 OK
    status = '200 OK'
    response_headers = [('Content-type', 'text/plain; charset=utf-8')]
    start_response(status, response_headers)
    return [output]

# Local test helper
if __name__ == "__main__":
    try:
        from wsgiref.simple_server import make_server
        print("Starting diagnostic server on port 8000...")
        with make_server('', 8000, app) as httpd:
            httpd.serve_forever()
    except KeyboardInterrupt:
        pass
