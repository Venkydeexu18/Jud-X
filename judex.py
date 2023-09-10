from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'
app.secret_key = 'your_secret_key'
db = SQLAlchemy(app)

# Client Table
class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    phone = db.Column(db.String(20), nullable=False, unique=True)
    problem_statement = db.Column(db.String(500), nullable=True)
    lawyer_id = db.Column(db.Integer, db.ForeignKey('lawyer.id'), nullable=True)

# Lawyer Table
class Lawyer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    phone = db.Column(db.String(20), nullable=False, unique=True)
    tagline = db.Column(db.String(200), nullable=False)
    licensed_practice_area = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    clients = db.relationship('Client', backref='lawyer', lazy=True)

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/case_file')
def case_file():
    return render_template('desktop-3.html')

@app.route('/find', methods=['GET', 'POST'])
def find():
    if request.method == 'POST':
        practice_area = request.form.get('practice_area')
        city = request.form.get('city')
        print(f"Practice Area: {practice_area}, City: {city}")

        return redirect(url_for('index'))

    return render_template('search.html')


@app.route('/search', methods=['POST'])
def search_lawyers():
    practice_area = request.form.get('practice_area')
    city = request.form.get('city')
    lawyers = Lawyer.query.filter_by(licensed_practice_area=practice_area, address=city).all()
    return render_template('search_results.html', lawyers=lawyers)

@app.route('/register_lawyer', methods=['GET'])
def show_lawyer_registration_form():
    return render_template('lawyer_registration.html')

@app.route('/register_lawyer', methods=['POST'])
def register_lawyer():
    if request.method == 'POST':
        name = request.form.get('name')
        tagline = request.form.get('tagline')
        practice_area = request.form.get('practice_area')
        address = request.form.get('address')
        email = request.form.get('email')
        phone = request.form.get('phone')
        lawyer = Lawyer(name=name, tagline=tagline, licensed_practice_area=practice_area, address=address, email=email, phone=phone)
        db.session.add(lawyer)
        db.session.commit()
        flash('Lawyer registration successful.')
        return redirect(url_for('index'))

@app.route('/lawyer/<int:lawyer_id>')
def lawyer_details(lawyer_id):
    lawyer = Lawyer.query.get(lawyer_id)
    return render_template('lawyer_details.html', lawyer=lawyer)

@app.route('/consult/<int:lawyer_id>', methods=['POST'])
def consultation_form(lawyer_id):
    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')
        email = request.form.get('email')
        problem_statement = request.form.get('problem_statement')
        client = Client(name=name, email=email, phone=phone, problem_statement=problem_statement, lawyer_id=lawyer_id)
        db.session.add(client)
        db.session.commit()
        return redirect(url_for('success'))

    return render_template('consultation_form.html', lawyer_id=lawyer_id)

@app.route('/client_register', methods=['GET', 'POST'])
def client_register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        password = request.form.get('password')
        problem_statement = request.form.get('problem_statement')
        # Hash the password before storing it in the database
        client = Client(name=name, email=email, phone=phone,problem_statement=problem_statement)
        db.session.add(client)
        db.session.commit()
        flash('Client registration successful. You can now log in.')
        return redirect(url_for('index'))

    return render_template('client_registration.html')

# Lawyer Registration
@app.route('/lawyer_register', methods=['GET', 'POST'])
def lawyer_register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        password = request.form.get('password')
        tagline = request.form.get('tagline')
        practice_area = request.form.get('practice_area')
        address = request.form.get('address')
        # Hash the password before storing it in the database
        lawyer = Lawyer(name=name, email=email, phone=phone, tagline=tagline, licensed_practice_area=practice_area, address=address)
        db.session.add(lawyer)
        db.session.commit()
        flash('Lawyer registration successful. You can now log in.')
        return redirect(url_for('index'))

    return render_template('lawyer_register.html')

# Client Login
@app.route('/client_login', methods=['GET', 'POST'])
def client_login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        client = Client.query.filter_by(email=email).first()

        if client and check_password_hash(client.password_hash, password):
            session['user_id'] = client.id
            flash('Client login successful.')
            return redirect(url_for('index'))
        flash('Invalid email or password. Please try again.')
    return render_template('client_login.html')

# Lawyer Login
@app.route('/lawyer_login', methods=['GET', 'POST'])
def lawyer_login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        lawyer = Lawyer.query.filter_by(email=email).first()
        if lawyer and check_password_hash(lawyer.password_hash, password):
            session['user_id'] = lawyer.id
            flash('Lawyer login successful.')
            return redirect(url_for('index'))
        flash('Invalid email or password. Please try again.')
    return render_template('lawyer_login.html')

@app.route('/kids')
def kids():
    return render_template('kids.html')

@app.route('/under')
def under():
    return render_template('child.html')

@app.route('/fir')
def fir():
    return render_template('fir.html')

@app.route('/schedule')
def schedule():
    return render_template('scheduling.html')

@app.route('/response')
def response():
    return render_template('response.html')

def calculate_court_fee(case_type, claim_amount):
    fee_multipliers = {
        'civil': 0.02,      
        'criminal': 100,    
        'family': 0.015,    
        'property': 0.03,    
        'probate': 0.01,    
        'tax': 0.04,     
        'labor': 0.02,     
        'contract': 0.025, 
    }
    if case_type not in fee_multipliers:
        return "Invalid case type"
    fee = fee_multipliers[case_type] * claim_amount
    return fee

@app.route('/fee', methods=['GET', 'POST'])
def fee():
    court_fee = None 
    if request.method == 'POST':
        case_type = request.form.get('case_type')
        claim_amount = float(request.form.get('claim_amount'))
        court_fee = calculate_court_fee(case_type, claim_amount)
        if court_fee == "Invalid case type":
            return render_template('fee.html', error_message="Invalid case type. Please enter a valid case type.")
        else:
            return render_template('fee.html', court_fee=court_fee) 
    
    return render_template('fee.html', court_fee=court_fee) 


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
