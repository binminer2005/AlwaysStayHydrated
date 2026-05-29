from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import json
import os

app = Flask(__name__)

# Cấu hình Secret Key bắt buộc cho Session trên Vercel
app.secret_key = 'khaihuyen_flashcard_secret_key_2026'

# FIX ĐƯỜNG DẪN TRÊN VERCEL: Lấy đường dẫn chuẩn xác dựa trên thư mục hiện tại của dự án
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) if 'wsgi' in os.path.abspath(__file__) else os.path.dirname(os.path.abspath(__file__))

USERS_FILE = os.path.join(BASE_DIR, 'users.json')
DATA_FILE = os.path.join(BASE_DIR, 'khai_huyen_data.json')

# Hàm đọc người dùng từ users.json
def load_users():
    # Nếu không tìm thấy file theo đường dẫn động, thử tìm ở thư mục hiện tại
    target_path = USERS_FILE if os.path.exists(USERS_FILE) else 'users.json'
    if not os.path.exists(target_path):
        return {"admin": "admin"} # Tạo sẵn một tài khoản mặc định đề phòng lỗi file
    try:
        with open(target_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {"admin": "admin"}

# Hàm lưu người dùng vào users.json
def save_users(users):
    target_path = USERS_FILE if os.path.exists(USERS_FILE) else 'users.json'
    try:
        with open(target_path, 'w', encoding='utf-8') as f:
            json.dump(users, f, ensure_ascii=False, indent=4)
    except Exception:
        pass # Tránh crash sập web nếu Vercel chặn quyền ghi file

# Hàm đọc dữ liệu flashcard từ khai_huyen_data.json
def load_flashcards():
    target_path = DATA_FILE if os.path.exists(DATA_FILE) else 'khai_huyen_data.json'
    if not os.path.exists(target_path):
        return {}
    try:
        with open(target_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {}

# Hàm lưu dữ liệu flashcard vào khai_huyen_data.json
def save_flashcards(data):
    target_path = DATA_FILE if os.path.exists(DATA_FILE) else 'khai_huyen_data.json'
    try:
        with open(target_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception:
        pass # Tránh crash sập web trên môi trường Serverless

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('flashcard_dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        users = load_users()
        
        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('flashcard_dashboard'))
        else:
            msg = 'Sai tên đăng nhập hoặc mật khẩu!'
    return render_template('login.html', msg=msg)

@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        users = load_users()
        
        if username in users:
            msg = 'Tài khoản đã tồn tại!'
        elif not username or not password:
            msg = 'Vui lòng điền đầy đủ thông tin!'
        else:
            users[username] = password
            save_users(users)
            msg = 'Đăng ký thành công! Vui lòng đăng nhập.'
            return render_template('login.html', msg=msg)
    return render_template('register.html', msg=msg)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/flashcard')
def flashcard_dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    data = load_flashcards()
    provinces = list(data.keys())
    return render_template('flashcard.html', provinces=provinces, username=session['username'])

@app.route('/api/districts/<province>')
def get_districts(province):
    if 'username' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    data = load_flashcards()
    districts_data = data.get(province, {})
    return jsonify(districts_data)

@app.route('/api/save_progress', methods=['POST'])
def save_progress():
    if 'username' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
        
    req_data = request.get_json()
    province = req_data.get('province')
    district = req_data.get('district')
    ward = req_data.get('ward')
    status = req_data.get('status')
    
    data = load_flashcards()
    
    if province in data and district in data[province] and ward in data[province][district]:
        data[province][district][ward]['status'] = status
        save_flashcards(data)
        return jsonify({'success': True})
    
    return jsonify({'success': False, 'message': 'Không tìm thấy đơn vị hành chính'}), 400

# Dành riêng cho Vercel Serverless nhận diện biến app làm điểm chạy chính
id_app = app
