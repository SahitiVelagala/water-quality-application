from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

app = Flask(__name__, static_folder='../frontend')

# Add CORS support to handle requests from frontend
CORS(app)

# Database config - SQLite file in backend folder
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'appdata.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Volunteer model
class Volunteer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(50))
    location = db.Column(db.String(100))
    interests = db.Column(db.String(200))
    skills = db.Column(db.String(500))
    availability = db.Column(db.String(50))

# Complaint model
class Complaint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    location = db.Column(db.String(100))
    type = db.Column(db.String(100))
    details = db.Column(db.String(1000))

# Serve frontend HTML
@app.route('/')
def serve_frontend():
    return send_from_directory(app.static_folder, 'new.html')

# ADD THIS ROUTE TO SERVE STATIC FILES (IMAGES, VIDEOS)
@app.route('/<path:filename>')
def serve_static_files(filename):
    return send_from_directory(app.static_folder, filename)

# Volunteer submit route
@app.route('/add_volunteer', methods=['POST'])
def add_volunteer():
    try:
        data = request.json
        interests = []
        
        if data.get('interestEducation'):
            interests.append('Education')
        if data.get('interestTesting'):
            interests.append('Testing')
        if data.get('interestDistribution'):
            interests.append('Distribution')
        if data.get('interestFundraising'):
            interests.append('Fundraising')
        
        interests_str = ",".join(interests)
        
        volunteer = Volunteer(
            name=data.get('name'),
            email=data.get('email'),
            phone=data.get('phone'),
            location=data.get('location'),
            interests=interests_str,
            skills=data.get('skills'),
            availability=data.get('availability')
        )
        db.session.add(volunteer)
        db.session.commit()
        return jsonify({'message': 'Volunteer saved successfully.'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Complaint submit route
@app.route('/add_complaint', methods=['POST'])
def add_complaint():
    try:
        data = request.json
        complaint = Complaint(
            name=data.get('name'),
            email=data.get('email'),
            location=data.get('location'),
            type=data.get('type'),
            details=data.get('details'),
        )
        db.session.add(complaint)
        db.session.commit()
        return jsonify({'message': 'Complaint saved successfully.'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)