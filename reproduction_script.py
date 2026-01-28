
import sys
import os

# Simulate api/index.py path manipulation
# api/index.py is in api/ directory.
# This script is in root.
# So we need to simulate running from api/ directory or just ensure sys.path is correct.

# In api/index.py:
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# If __file__ is /.../api/index.py, dirname is /.../api, dirname(dirname) is /.../ (project root).
# So it appends project root.

# When running this script from root, project root is already in path usually.
# But let's be explicit to match api/index.py logic if we were in api/ folder.
# But simply trying to import app from here should be enough if we are in root.

print("Current sys.path:", sys.path)
print("Attempting to import app...")

try:
    from app import app
    print("Successfully imported app.")
    print("App config:", app.config)
except Exception as e:
    print("Failed to import app:", e)
    import traceback
    traceback.print_exc()

# Also try to import the routes to be sure
try:
    from app.routes import chat_gpt_routes, form_routes
    print("Routes imported successfully.")
except Exception as e:
    print("Failed to import routes:", e)
    import traceback
    traceback.print_exc()
