
from flask import render_template
from app.init import app  # Import von app.init, um die Flask-App zu verwenden

@app.route('/')
def index():
    return render_template('index.html')

