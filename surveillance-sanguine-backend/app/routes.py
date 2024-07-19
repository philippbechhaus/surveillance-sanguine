from flask import Blueprint, request, jsonify, current_app, send_from_directory
from werkzeug.utils import secure_filename
from . import db
from .models import User, Test, Biomarker
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
import os
import logging

bp = Blueprint('routes', __name__)

logging.basicConfig(level=logging.INFO)

@bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        hashed_password = generate_password_hash(data['password'])
        new_user = User(username=data['username'], email=data['email'], password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        logging.info("User registered successfully")
        return jsonify({'message': 'User registered successfully'})
    except Exception as e:
        logging.error(f"Registration failed: {str(e)}")
        return jsonify({'message': 'Registration failed', 'error': str(e)}), 400

@bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        user = User.query.filter_by(email=data['email']).first()
        if user and check_password_hash(user.password_hash, data['password']):
            access_token = create_access_token(identity={'username': user.username, 'email': user.email})
            logging.info("Login successful")
            return jsonify(access_token=access_token)
        logging.warning("Invalid credentials")
        return jsonify({'message': 'Invalid credentials'}), 401
    except Exception as e:
        logging.error(f"Login failed: {str(e)}")
        return jsonify({'message': 'Login failed', 'error': str(e)}), 400

@bp.route('/upload', methods=['POST'])
@jwt_required()
def upload():
    try:
        current_user = get_jwt_identity()
        user = User.query.filter_by(email=current_user['email']).first()
        if 'file' not in request.files:
            logging.warning("No file part")
            return jsonify({'message': 'No file part'}), 400
        file = request.files['file']
        if file.filename == '':
            logging.warning("No selected file")
            return jsonify({'message': 'No selected file'}), 400
        filename = secure_filename(file.filename)
        save_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(save_path)

        # Save test information in the database
        new_test = Test(user_id=user.id)
        db.session.add(new_test)
        db.session.commit()

        logging.info(f"File uploaded successfully: {save_path}")
        return jsonify({'message': 'File uploaded successfully', 'filename': filename})
    except Exception as e:
        logging.error(f"File upload failed: {str(e)}")
        return jsonify({'message': str(e)}), 400

@bp.route('/file-url/<filename>', methods=['GET', 'OPTIONS'])
@jwt_required()
def get_file_url(filename):
    if request.method == 'OPTIONS':
        return jsonify({'message': 'CORS preflight request'}), 200

    file_url = f'http://127.0.0.1:5000/uploads/{filename}'
    return jsonify({'file_url': file_url})


@bp.route('/uploads/<filename>', methods=['GET'])
def get_uploaded_file(filename):
    try:
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        logging.info(f"Retrieving file from: {file_path}")
        return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)
    except Exception as e:
        logging.error(f"File retrieval failed: {str(e)}")
        return jsonify({'message': str(e)}), 404

@bp.route('/tests', methods=['GET'])
@jwt_required()
def get_user_tests():
    try:
        current_user = get_jwt_identity()
        user = User.query.filter_by(email=current_user['email']).first()
        if not user:
            return jsonify({'message': 'User not found'}), 404

        tests = Test.query.filter_by(user_id=user.id).order_by(Test.test_date.desc()).all()
        tests_data = [{'id': test.id, 'test_date': test.test_date} for test in tests]
        return jsonify(tests_data)
    except Exception as e:
        logging.error(f"Fetching tests failed: {str(e)}")
        return jsonify({'message': str(e)}), 400