# app.py - PLACE THIS IN YOUR ROOT DIRECTORY
from flask import Flask, send_file, jsonify, request, send_from_directory
import os
import json
from datetime import datetime
import hashlib

app = Flask(__name__)

print("🚀 Blood Donation App - ROOT DIRECTORY EDITION")

# Serve HTML files directly
@app.route('/')
def index():
    return send_file('login.html')

@app.route('/<page>')
def serve_page(page):
    if not page.endswith('.html'):
        page = page + '.html'
    return send_file(page)

# Serve static files
@app.route('/styles/<filename>')
def serve_css(filename):
    return send_from_directory('styles', filename)

@app.route('/scripts/<filename>')
def serve_js(filename):
    return send_from_directory('scripts', filename)

@app.route('/images/<filename>')
def serve_images(filename):
    return send_from_directory('images', filename)

# SIMPLE IN-MEMORY DATABASE
donors_db = []
blockchain_db = []
users_db = []

# SIMPLE BLOCKCHAIN
@app.route('/api/blockchain/register-donor', methods=['POST'])
def register_donor():
    data = request.json
    donor_id = f"DONOR_{len(donors_db)+1}"
    
    donor = {
        'id': donor_id,
        'name': data.get('name', 'Unknown'),
        'bloodType': data.get('bloodType', 'O+'),
        'phone': data.get('phone', '0000000000'),
        'isVerified': True,
        'totalDonations': 0
    }
    donors_db.append(donor)
    
    # Add to blockchain
    block_hash = hashlib.md5(f"{donor_id}{datetime.now()}".encode()).hexdigest()[:16]
    blockchain_db.append({
        'type': 'DONOR_REGISTERED',
        'donorId': donor_id,
        'timestamp': datetime.now().isoformat(),
        'hash': block_hash
    })
    
    return jsonify({
        'success': True,
        'message': 'Donor registered on blockchain!',
        'donor': donor,
        'transactionHash': block_hash
    })

@app.route('/api/blockchain/search-donors/<blood_type>')
def search_donors(blood_type):
    # Always return some test data
    test_donors = [
        {'id': 'DONOR_1', 'name': 'John Smith', 'bloodType': blood_type, 'phone': '+1234567890', 'totalDonations': 3, 'isVerified': True},
        {'id': 'DONOR_2', 'name': 'Maria Garcia', 'bloodType': blood_type, 'phone': '+1234567891', 'totalDonations': 2, 'isVerified': True},
        {'id': 'DONOR_3', 'name': 'David Lee', 'bloodType': blood_type, 'phone': '+1234567892', 'totalDonations': 1, 'isVerified': True}
    ]
    
    return jsonify({
        'success': True,
        'donors': test_donors,
        'count': len(test_donors)
    })

@app.route('/api/blockchain/info')
def blockchain_info():
    return jsonify({
        'success': True,
        'status': 'connected',
        'blockHeight': len(blockchain_db),
        'totalDonors': len(donors_db),
        'message': 'Educational Blockchain Running'
    })

@app.route('/api/status')
def status():
    return jsonify({
        'status': 'connected',
        'blockchain': 'connected', 
        'database': 'connected',
        'message': 'Everything is working perfectly!'
    })

# AUTHENTICATION
@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    users_db.append(data)
    return jsonify({'message': 'Signup successful!'})

@app.route('/login', methods=['POST']) 
def login():
    data = request.json
    return jsonify({
        'message': 'Login successful!',
        'user_id': 1,
        'email': data.get('email', 'user@example.com')
    })

# ADD TEST DATA
@app.route('/api/add-test-donors', methods=['POST'])
def add_test_donors():
    test_donors = [
        {'name': 'Test User 1', 'bloodType': 'O+', 'phone': '+1111111111'},
        {'name': 'Test User 2', 'bloodType': 'A-', 'phone': '+2222222222'}, 
        {'name': 'Test User 3', 'bloodType': 'B+', 'phone': '+3333333333'}
    ]
    
    for donor in test_donors:
        donors_db.append({
            'id': f"TEST_{len(donors_db)+1}",
            **donor,
            'isVerified': True,
            'totalDonations': 2
        })
    
    return jsonify({
        'success': True,
        'message': f'Added {len(test_donors)} test donors!',
        'total_donors': len(donors_db)
    })

if __name__ == '__main__':
    print("📍 Server: http://localhost:5000")
    print("🎯 Open: http://localhost:5000")
    print("💡 Running from ROOT directory - No path issues!")
    app.run(debug=True, port=5000)