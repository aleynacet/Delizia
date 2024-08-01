import logging
from flask import Flask, render_template, redirect, url_for, request, flash, session, jsonify
from firebase_auth import firebase_register, firebase_login

# Für die API Calls zu Yelp ausklammern für flask run
from .save_to_firestore import save_data_to_firestore
from firebase_admin import firestore
 
# folgendes damit die Daten aus Firebase in der Webapp angezeigt werden
db = firestore.client()
 
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'  
 
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
                flash('Invalid Login', 'danger')
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
        try:
            # holt die Daten aus Firestore
            restaurants_ref = db.collection('yelp_businesses')
            docs = restaurants_ref.stream()

            restaurants_list = []
            for doc in docs:
                restaurants_list.append(doc.to_dict())

            # kontrolliert ob Restaurants gefunden wurden
            if not restaurants_list:
                return "No restaurants found", 404

            # zeigt die Restaurants in der Webapp an
            return render_template('all.html', restaurants=restaurants_list, category="All")
        except Exception as e:
            return f"An error occurred while fetching data: {e}", 500

 
    @app.route('/category/asian')
    def asian():
        try:
            # holt die Daten aus Firestore
            restaurants_ref = db.collection('yelp_businesses')
            docs = restaurants_ref.stream()

            restaurants_list = []
            for doc in docs:
                restaurant_data = doc.to_dict()
                categories = restaurant_data.get('categories', [])
                if any(cat.get('title') in ['Japanese', 'Chinese', 'Korean'] for cat in categories):
                    restaurants_list.append(restaurant_data)

           
            if not restaurants_list:
                return "No restaurants found for category 'asian'", 404

            
            return render_template('asian.html', restaurants=restaurants_list, category="Asian")
        except Exception as e:
            return f"An error occurred while fetching data: {e}", 500
    
    @app.route('/category/vegan')
    def vegan():
        try:
            
            restaurants_ref = db.collection('yelp_businesses')
            docs = restaurants_ref.stream()

            restaurants_list = []
            for doc in docs:
                restaurant_data = doc.to_dict()
                categories = restaurant_data.get('categories', [])
                if any(cat.get('title') == 'Vegan' for cat in categories):
                    restaurants_list.append(restaurant_data)

            
            if not restaurants_list:
                return "No restaurants found for category 'vegan'", 404

            
            return render_template('vegan.html', restaurants=restaurants_list, category="Vegan")
        except Exception as e:
            return f"An error occurred while fetching data: {e}", 500
        
    @app.route('/category/vegetarian')
    def vegetarian():
        try:
            restaurants_ref = db.collection('yelp_businesses')
            docs = restaurants_ref.stream()

            restaurants_list = []
            for doc in docs:
                restaurant_data = doc.to_dict()
                categories = restaurant_data.get('categories', [])
                if any(cat.get('title') == 'Vegetarian' for cat in categories):
                    restaurants_list.append(restaurant_data)

            if not restaurants_list:
                return "No restaurants found for category 'vegetarian'", 404

            return render_template('vegetarian.html', restaurants=restaurants_list, category="Vegetarian")
        except Exception as e:
            return f"An error occurred while fetching data: {e}", 500
        
    @app.route('/category/mexican')
    def mexican():
        try:
            restaurants_ref = db.collection('yelp_businesses')
            docs = restaurants_ref.stream()

            restaurants_list = []
            for doc in docs:
                restaurant_data = doc.to_dict()
                categories = restaurant_data.get('categories', [])
                if any(cat.get('title') == 'Mexican' for cat in categories):
                    restaurants_list.append(restaurant_data)

            if not restaurants_list:
                return "No restaurants found for category 'mexican'", 404

            return render_template('mexican.html', restaurants=restaurants_list, category="Mexican")
        except Exception as e:
            return f"An error occurred while fetching data: {e}", 500
        

    @app.route('/category/italian')
    def italian():
        try:
            restaurants_ref = db.collection('yelp_businesses')
            docs = restaurants_ref.stream()

            restaurants_list = []
            for doc in docs:
                restaurant_data = doc.to_dict()
                categories = restaurant_data.get('categories', [])
                if any(cat.get('title') == 'Italian' for cat in categories):
                    # fügt die Bewertung und die Anzahl der Bewertungen hinzu
                    restaurant_data['rating'] = restaurant_data.get('rating', 0)
                    restaurant_data['review_count'] = restaurant_data.get('review_count', 0)
                    restaurants_list.append(restaurant_data)

        
            if not restaurants_list:
                return "No restaurants found for category 'italian'", 404

            return render_template('italian.html', restaurants=restaurants_list, category="Italian")
        except Exception as e:
            return f"An error occurred while fetching data: {e}", 500

    @app.route('/category/german')
    def german():
        try:
            restaurants_ref = db.collection('yelp_businesses')
            docs = restaurants_ref.stream()

            restaurants_list = []
            for doc in docs:
                restaurant_data = doc.to_dict()
                categories = restaurant_data.get('categories', [])
                if any(cat.get('title') == 'German' for cat in categories):
                    restaurants_list.append(restaurant_data)

            if not restaurants_list:
                return "No restaurants found for category 'german'", 404

            return render_template('german.html', restaurants=restaurants_list, category="German")
        except Exception as e:
            return f"An error occurred while fetching data: {e}", 500
 
    @app.route('/choosediner', methods=['GET', 'POST'])
    def choosediner():
        category = request.args.get('category', 'all').lower()
        
        if request.method == 'POST':
            selected_diners = request.form.get('selected_diners')
            if selected_diners:
                session['selected_diners'] = selected_diners.split(',')
                session['votes'] = {diner: 0 for diner in session['selected_diners']}  # Macht die Votes wieder auf 0
                return redirect(url_for('createpoll'))
        
        try:
            category_mapping = {
                'asian': ['japanese', 'chinese', 'korean'],
                'italian': ['italian'],
                'mexican': ['mexican'],
                'vegan': ['vegan'],
                'vegetarian': ['vegetarian'],
                'german': ['german']
            }

            restaurants_ref = db.collection('yelp_businesses')
            docs = restaurants_ref.stream()
            
            restaurants_list = []
            for doc in docs:
                restaurant_data = doc.to_dict()
                categories = restaurant_data.get('categories', [])
                
                if category == 'all':
                    restaurants_list.append(restaurant_data)
                else:
                    valid_categories = category_mapping.get(category, [category])
                    if any(cat.get('title').lower() in valid_categories for cat in categories):
                        restaurants_list.append(restaurant_data)
            
            if not restaurants_list:
                flash(f'No restaurants found for category {category}', 'danger')
                return render_template('choosediner.html', restaurants=[], category=category)
            
            return render_template('choosediner.html', restaurants=restaurants_list, category=category.capitalize())
        except Exception as e:
            flash(f"An error occurred while fetching data: {e}", 'danger')
            return render_template('choosediner.html', restaurants=[], category=category.capitalize())

        
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
    
    @app.route('/submit_vote', methods=['POST'])
    def submit_vote():
        selected_diner = request.form.get('selected_diner')
        if not selected_diner:
            flash('Please select a restaurant to vote for', 'danger')
            return redirect(url_for('vote'))

        # speichert die Votes in der Session
        votes = session.get('votes', {})
        if selected_diner in votes:
            votes[selected_diner] += 1
        else:
            votes[selected_diner] = 1
        session['votes'] = votes

        # speichert den gewählten Diner in der Session
        session['voted_diner'] = selected_diner

        return redirect(url_for('vote_results'))
    
    @app.route('/vote_results')
    def vote_results():
        voted_diner = session.get('voted_diner')
        if not voted_diner:
            flash('No vote found', 'danger')
            return redirect(url_for('vote'))

        diners = session.get('selected_diners')
        votes = session.get('votes', {})
        return render_template('vote_results.html', voted_diner=voted_diner, diners=diners, votes=votes)
    
    @app.route('/final_results')
    def final_results():
        diners = session.get('selected_diners')
        votes = session.get('votes', {})
        return render_template('final_results.html', diners=diners, votes=votes)
    
 
    @app.route('/update_yelp_data', methods=['GET'])
    def update_yelp_data():
        try:
            data = fetch_yelp_data('restaurants', 'Berlin', 'italian', 5000)
            save_data_to_firestore(data)
            return jsonify({"message": "Data updated successfully."}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
 
    return app