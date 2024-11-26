from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import random
import string
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Models
class Code(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), unique=True, nullable=False)
    duration = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), default="Active")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100))
    phone_number = db.Column(db.String(20))
    payment_status = db.Column(db.String(20), default="Pending")
    code_issued = db.Column(db.String(10))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/generate_code', methods=['POST'])
def generate_code():
    duration = request.form.get('duration')
    duration_mapping = {"1 hour": 1, "1 day": 24, "1 week": 168}
    hours = duration_mapping.get(duration, 1)
    
    new_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    expires_at = datetime.utcnow() + timedelta(hours=hours)
    
    code = Code(code=new_code, duration=duration, expires_at=expires_at)
    db.session.add(code)
    db.session.commit()
    
    return jsonify({'code': new_code, 'expires_at': expires_at.strftime('%Y-%m-%d %H:%M:%S')})

@app.route('/get_codes', methods=['GET'])
def get_codes():
    codes = Code.query.all()
    code_list = [{'id': c.id, 'code': c.code, 'duration': c.duration, 'status': c.status, 
                  'created_at': c.created_at, 'expires_at': c.expires_at} for c in codes]
    return jsonify(code_list)

@app.route('/log_transaction', methods=['POST'])
def log_transaction():
    customer_name = request.form.get('customer_name')
    phone_number = request.form.get('phone_number')
    code_issued = request.form.get('code_issued')
    
    transaction = Transaction(customer_name=customer_name, phone_number=phone_number, 
                               payment_status="Completed", code_issued=code_issued)
    db.session.add(transaction)
    db.session.commit()
    
    return jsonify({'status': 'success', 'message': 'Transaction logged successfully'})

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
