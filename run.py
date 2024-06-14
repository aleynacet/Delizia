# run.py

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app.init import app  # Import von app.init

if __name__ == '__main__':
    app.run(debug=True)

