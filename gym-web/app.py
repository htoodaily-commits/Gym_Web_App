from flask import Flask, render_template, request, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from functools import wraps

app = Flask(__name__)
app.secret_key = 'super-secret-key-12345'  

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gym.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    date_submitted = db.Column(db.DateTime, default=datetime.utcnow)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    join_date = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit-form', methods=['POST'])
def submit_form():
    user_name = request.form['username']
    user_phone = request.form['phone']

    new_contact = Contact(name=user_name, phone=user_phone)
    db.session.add(new_contact)
    db.session.commit()

    return render_template('thankyou.html')            

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return render_template('register.html', error="Email already exists")
        
        new_user = User(name=name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        
        return redirect(url_for('user_login'))
    
    return render_template('register.html', error=None)

@app.route('/user/login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = User.query.filter_by(email=email, password=password).first()
        
        if user:
            session['user_id'] = user.id
            session['user_logged_in'] = True
            return redirect(url_for('user_dashboard'))
        else:
            return render_template('user_login.html', error=True)
    
    return render_template('user_login.html', error=False)

@app.route('/user/dashboard')
def user_dashboard():
    if not session.get('user_logged_in'):
        return redirect(url_for('user_login'))
    
    user = User.query.get(session['user_id'])
    return render_template('user_dashboard.html', user=user)

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        password = request.form['password']
        if password == 'fittime2026':
            session['admin_logged_in'] = True
            return redirect(url_for('admin'))
        else:
            return render_template('admin_login.html', error=True)
    
    return render_template('admin_login.html', error=False)

@app.route('/admin')
@admin_required
def admin():
    all_contacts = Contact.query.all()
    all_users = User.query.all() 
    return render_template('admin.html', contacts=all_contacts, users=all_users)

@app.route('/logout')
def logout():
    session.pop('user_logged_in', None)
    session.pop('admin_logged_in', None)
    session.pop('user_id', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host='0.0.0.0', debug=True)