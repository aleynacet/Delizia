from flask import Blueprint, render_template, redirect, url_for, request, flash, session

bp = Blueprint('main', __name__)

# Statische Benutzerdaten (zur Demo)
users = {
    "test@example.com": {"password": "password123", "username": "testuser"}
}

@bp.route('/')
def home():
    return render_template('index.html')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash('Passwords do not match', 'danger')
        elif email in users:
            flash('Email already registered', 'danger')
        else:
            users[email] = {"password": password, "username": username}
            flash('Registration successful, please log in', 'success')
            return redirect(url_for('main.login'))
    
    return render_template('register.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = users.get(email)

        if user and user["password"] == password:
            session['user'] = user
            flash('Login successful', 'success')
             # leitet zu categories weiter
            return redirect(url_for('main.categories'))  
        else:
            flash('Login unsuccessful. Check your email and password', 'danger')
    
    return render_template('login.html')

@bp.route('/logout')
def logout():
    session.pop('user', None)
    flash('Logged out successfully', 'success')
    return redirect(url_for('main.home'))

@bp.route('/categories')
def categories():
    # man muss eingeloggt sein, um diese Seite zu sehen
    if 'user' not in session:
        flash('Please log in to view this page', 'danger')
        return redirect(url_for('main.login'))
    return render_template('categories.html')

@bp.route('/category/asian')
def asian():
    return render_template('asian.html')
