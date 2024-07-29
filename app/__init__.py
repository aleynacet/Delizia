from flask import Flask, render_template, redirect, url_for, request, flash, session, jsonify
from firebase_auth import firebase_register, firebase_login
# Für die API Calls zu Yelp ausklammern für flask run
# from save_to_firestore import save_data_to_firestore, fetch_yelp_data

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'  # for Flask forms and sessions

    @app.route('/')
    def home():
        return render_template('index.html')

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            confirm_password = request.form['confirm_password']

            if password != confirm_password:
                flash('Passwords do not match', 'danger')
            else:
                result = firebase_register(email, password)
                if 'error' in result:
                    error_message = result['error']['message']
                    if error_message == 'EMAIL_EXISTS':
                        flash('This email is already registered.', 'danger')
                    else:
                        flash(error_message, 'danger')
                else:
                    flash('Registration successful, please log in', 'success')
                    return redirect(url_for('login'))

        return render_template('register.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']

            result = firebase_login(email, password)
            if 'error' in result:
                flash(result['error']['message'], 'danger')
            else:
                session['user'] = result['idToken']
                flash('Login successful', 'success')
                return redirect(url_for('categories'))
            
        return render_template('login.html')

    @app.route('/logout')
    def logout():
        session.pop('user', None)
        flash('Logged out successfully', 'success')
        return redirect(url_for('home'))

    @app.route('/categories')
    def categories():
        if 'user' not in session:
            flash('Please log in to view this page', 'danger')
            return redirect(url_for('login'))
        return render_template('categories.html')

    @app.route('/category/all')
    def all():
        return render_template('all.html')

    @app.route('/category/asian')
    def asian():
        return render_template('asian.html')

    @app.route('/category/burgers')
    def burgers():
        return render_template('burgers.html')

    @app.route('/choosediner', methods=['GET', 'POST'])
    def choosediner():
        if request.method == 'POST':
            selected_diners = request.form.get('selected_diners')
            if selected_diners:
                session['selected_diners'] = selected_diners.split(',')
                return redirect(url_for('createpoll'))
        return render_template('choosediner.html')

    @app.route('/createpoll')
    def createpoll():
        diners = session.get('selected_diners')
        if not diners:
            return redirect(url_for('choosediner'))
        return render_template('createpoll.html', diners=diners)

    @app.route('/vote')
    def vote():
        diners = session.get('selected_diners')
        if not diners:
            return redirect(url_for('choosediner'))
        return render_template('vote.html', diners=diners)

    @app.route('/update_yelp_data', methods=['GET'])
    def update_yelp_data():
        try:
            data = fetch_yelp_data('restaurants', 'Berlin', 'italian', 5000)
            save_data_to_firestore(data)
            return jsonify({"message": "Data updated successfully."}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return app