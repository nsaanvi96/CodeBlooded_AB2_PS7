# app.py - NO DATABASE VERSION (100% in-memory)
from flask import Flask, send_file, jsonify, request, send_from_directory
import os
import hashlib
from datetime import datetime

app = Flask(__name__)

print("🚀 Blood Donation App - NO DATABASE NEEDED!")

# Serve files (same as before)
@app.route('/')
def index(): return send_file('login.html')

@app.route('/<page>')
def serve_page(page):
    if not page.endswith('.html'): page = page + '.html'
    return send_file(page)

@app.route('/styles/<filename>')
def serve_css(filename): return send_from_directory('styles', filename)

@app.route('/scripts/<filename>')  
def serve_js(filename): return send_from_directory('scripts', filename)

@app.route('/images/<filename>')
def serve_images(filename): return send_from_directory('images', filename)

# In-memory storage
users = []
donors = []
blockchain = []

# Blockchain routes (same as before)
@app.route('/api/blockchain/register-donor', methods=['POST'])
def register_donor():
    data = request.json
    donor_id = f"DONOR_{len(donors)+1}"
    
    donor = {
        'id': donor_id,
        'name': data.get('name', 'Unknown'),
        'bloodType': data.get('bloodType', 'O+'),
        'phone': data.get('phone', '0000000000'),
        'isVerified': True,
        'totalDonations': 0
    }
    donors.append(donor)
    
    block_hash = hashlib.md5(f"{donor_id}{datetime.now()}".encode()).hexdigest()[:16]
    blockchain.append({'type': 'DONOR_REGISTERED', 'hash': block_hash})
    
    return jsonify({'success': True, 'message': 'Registered!', 'donor': donor, 'transactionHash': block_hash})

@app.route('/api/blockchain/search-donors/<blood_type>')
def search_donors(blood_type):
    test_donors = [
        {'id': 'DONOR_1', 'name': 'John Smith', 'bloodType': blood_type, 'phone': '+1234567890', 'totalDonations': 3, 'isVerified': True},
        {'id': 'DONOR_2', 'name': 'Maria Garcia', 'bloodType': blood_type, 'phone': '+1234567891', 'totalDonations': 2, 'isVerified': True},
    ]
    return jsonify({'success': True, 'donors': test_donors, 'count': len(test_donors)})

@app.route('/api/blockchain/info')
def blockchain_info():
    return jsonify({'success': True, 'status': 'connected', 'blockHeight': len(blockchain), 'totalDonors': len(donors)})

# Auth (in-memory)
@app.route('/signup', methods=['POST'])
def signup():
    users.append(request.json)
    return jsonify({'message': 'Signup successful!'})

@app.route('/login', methods=['POST'])
def login():
    return jsonify({'message': 'Login successful!', 'user_id': 1, 'email': 'user@example.com'})

if __name__ == '__main__':
    print("📍 http://localhost:5000")
    print("💡 No database setup needed!")
    app.run(debug=True, port=5000)