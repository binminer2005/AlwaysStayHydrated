import json
import random
import re
import os
from functools import wraps
from flask import Flask, render_template, render_template_string, jsonify, request, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import shutil, pathlib, tempfile
from flashcard_models import db, Tab, Card, CardStatus, init_db

src = pathlib.Path('BD Lifeless Grotesk')
dst = pathlib.Path('static/fonts')
dst.mkdir(parents=True, exist_ok=True)
for p in src.rglob('*.woff2'):
    shutil.copy2(p, dst)

app = Flask(__name__)
app.secret_key = "khai_huyen_1925_secret"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flashcard.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db.init_app(app)
init_db(app)

# Load data
with open("khai_huyen_data.json", encoding="utf-8") as f:
    BIBLE_DATA = json.load(f)

def make_blank_question(verse_text):
    """Chọn ngẫu nhiên một cụm từ quan trọng để tạo câu hỏi điền vào chỗ trống."""
    # Tách câu thành các đoạn có nghĩa (3-6 từ)
    words = verse_text.split()
    if len(words) < 5:
        return None, None

    # Chọn vị trí ngẫu nhiên để tạo chỗ trống (tránh đầu và cuối)
    max_blank_len = min(4, len(words) // 3)
    blank_len = random.randint(2, max(2, max_blank_len))
    start = random.randint(1, len(words) - blank_len - 1)

    answer_words = words[start:start + blank_len]
    answer = " ".join(answer_words)

    blanked = words[:start] + ["___________"] + words[start + blank_len:]
    question_text = " ".join(blanked)

    return question_text, answer


USERS_FILE = os.path.join(os.path.dirname(__file__), "users.json")


def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, encoding="utf-8") as f:
        try:
            return json.load(f)
        except Exception:
            return {}


def save_users(users):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)


def login_required(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        if session.get("user"):
            return f(*args, **kwargs)
        # If it's an API call, return JSON 401
        if request.path.startswith("/api/"):
            return jsonify({"error": "Unauthorized"}), 401
        return redirect(url_for("login", next=request.path))
    return wrapped


def flashcard_api_required(f):
    """Decorator for flashcard API endpoints - requires user authentication"""
    @wraps(f)
    def wrapped(*args, **kwargs):
        if not session.get("flashcard_user"):
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs)
    return wrapped


def flashcard_admin_required(f):
    """Decorator for flashcard admin API endpoints - requires admin role"""
    @wraps(f)
    def wrapped(*args, **kwargs):
        user = session.get("flashcard_user")
        role = session.get("flashcard_role")
        
        if not user:
            return jsonify({"error": "Unauthorized"}), 401
        
        if role != "admin":
            return jsonify({"error": "Forbidden - admin access required"}), 403
        
        return f(*args, **kwargs)
    return wrapped


@app.route("/")
@login_required
def index():
    return render_template("index.html")


@app.route("/flashcard")
@login_required
def flashcard():
    """Flashcard learning page"""
    if not session.get("flashcard_user"):
        return redirect(url_for("flashcard_login"))
    
    user = session.get("flashcard_user")
    role = session.get("flashcard_role", "view")
    
    return render_template("flashcard.html", user=user, role=role)


@app.route("/register", methods=["GET", "POST"])
def register():
    msg = None
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        if not username or not password:
            msg = "Vui lòng nhập tên đăng nhập và mật khẩu."
        else:
            users = load_users()
            if username in users:
                msg = "Tài khoản đã tồn tại."
            else:
                users[username] = {"pw": generate_password_hash(password)}
                save_users(users)
                session["user"] = username
                return redirect(url_for("index"))
    return render_template("register.html", msg=msg)


@app.route("/login", methods=["GET", "POST"])
def login():
    msg = None
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        users = load_users()
        user = users.get(username)
        if not user or not check_password_hash(user.get("pw", ""), password):
            msg = "Tên đăng nhập hoặc mật khẩu không đúng."
        else:
            session["user"] = username
            next_url = request.args.get("next") or url_for("index")
            return redirect(next_url)
    return render_template("login.html", msg=msg)


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))


@app.route("/flashcard/login", methods=["GET", "POST"])
def flashcard_login():
    """Flashcard login page with static passwords"""
    msg = None
    if request.method == "POST":
        password = request.form.get("password", "").strip()
        
        # Check static passwords for flashcard
        if password == "donganadmin":
            session["flashcard_user"] = "flashcard_admin"
            session["flashcard_role"] = "admin"
            return redirect(url_for("flashcard"))
        elif password == "dongan":
            session["flashcard_user"] = "flashcard_user"
            session["flashcard_role"] = "view"
            return redirect(url_for("flashcard"))
        else:
            msg = "Mật khẩu không đúng. Sử dụng 'dongan' hoặc 'donganadmin'."
    
    return render_template("flashcard_login.html", msg=msg)


@app.route("/flashcard/logout")
def flashcard_logout():
    """Flashcard logout"""
    session.pop("flashcard_user", None)
    session.pop("flashcard_role", None)
    return redirect(url_for("flashcard_login"))


@app.route("/api/flashcard/check-auth")
def flashcard_check_auth():
    """Check flashcard authentication status"""
    user = session.get("flashcard_user")
    role = session.get("flashcard_role")
    
    return jsonify({
        'authenticated': bool(user),
        'user': user,
        'role': role
    })


@app.route("/api/question")
@login_required
def get_question():
    chapter = request.args.get("chapter", "random")

    if chapter == "random":
        ch = str(random.randint(1, 22))
    else:
        ch = str(int(chapter))

    verses = BIBLE_DATA.get(ch, [])
    if not verses:
        return jsonify({"error": "Không có dữ liệu"}), 400

    # Chọn ngẫu nhiên một câu
    verse_obj = random.choice(verses)
    verse_text = verse_obj["text"]
    verse_num = verse_obj["verse"]

    question_text, answer = make_blank_question(verse_text)
    if not question_text:
        return get_question()  # thử lại nếu câu quá ngắn

    return jsonify({
        "chapter": int(ch),
        "verse": verse_num,
        "question": question_text,
        "answer": answer,
        "full_verse": verse_text
    })



@app.route("/api/chapters")
@login_required
def get_chapters():
    """Trả về số câu mỗi đoạn."""
    info = {}
    for ch, verses in BIBLE_DATA.items():
        if verses:
            max_v = max(v["verse"] for v in verses)
            info[ch] = {"count": len(verses), "max_verse": max_v}
    return jsonify(info)



@app.route("/api/typing-question")
@login_required
def get_typing_question():
    """Lấy một câu Kinh thánh để luyện gõ."""
    chapter = request.args.get("chapter", "random")

    if chapter == "random":
        ch = str(random.randint(1, 22))
    else:
        ch = str(int(chapter))

    verses = BIBLE_DATA.get(ch, [])
    if not verses:
        return jsonify({"error": "Không có dữ liệu"}), 400

    verse_obj = random.choice(verses)
    verse_text = verse_obj["text"]
    verse_num = verse_obj["verse"]

    return jsonify({
        "chapter": int(ch),
        "verse": verse_num,
        "text": verse_text,
        "word_count": len(verse_text.split())
    })




@app.route("/api/check-typing", methods=["POST"])
@login_required
def check_typing():
    """Kiểm tra kết quả luyện gõ và tính WPM, độ chính xác."""
    data = request.json
    original_text = data.get("original", "").strip()
    typed_text = data.get("typed", "").strip()
    time_seconds = data.get("time_seconds", 0)

    if not original_text or not typed_text:
        return jsonify({"error": "Dữ liệu không hợp lệ"}), 400

    # Tính độ chính xác (character-level)
    correct_chars = 0
    total_chars = max(len(original_text), len(typed_text))
    
    for i in range(min(len(original_text), len(typed_text))):
        if original_text[i] == typed_text[i]:
            correct_chars += 1
    
    accuracy = (correct_chars / total_chars * 100) if total_chars > 0 else 0

    # Tính WPM (Words Per Minute)
    word_count = len(original_text.split())
    time_minutes = time_seconds / 60 if time_seconds > 0 else 1
    wpm = word_count / time_minutes

    # Kiểm tra chính xác toàn bộ
    is_perfect = original_text == typed_text

    return jsonify({
        "is_perfect": is_perfect,
        "accuracy": round(accuracy, 1),
        "wpm": round(wpm, 1),
        "time_seconds": time_seconds,
        "correct_chars": correct_chars,
        "total_chars": total_chars
    })


# ─────────────────────────────────────────────────────
# FLASHCARD API ENDPOINTS
# ─────────────────────────────────────────────────────

@app.route("/api/flashcard/data")
@flashcard_api_required
def get_flashcard_data():
    """Lấy toàn bộ tabs, cards, và trạng thái học tập của user hiện tại"""
    user = session.get("flashcard_user")
    
    tabs = Tab.query.all()
    data = []
    
    for tab in tabs:
        tab_dict = {
            'id': tab.id,
            'name': tab.name,
            'cards': []
        }
        
        for card in tab.cards:
            card_dict = card.to_dict(include_statuses=False)
            
            # Lấy trạng thái của user hiện tại cho card này
            status = CardStatus.query.filter_by(
                card_id=card.id, 
                user_id=user
            ).first()
            card_dict['status'] = status.status if status else ''
            
            tab_dict['cards'].append(card_dict)
        
        data.append(tab_dict)
    
    # Tính thống kê
    stats = _calculate_stats(user)
    
    return jsonify({
        'data': data,
        'stats': stats
    })


@app.route("/api/flashcard/tabs", methods=["POST"])
@flashcard_admin_required
def create_tab():
    """Tạo một tab mới"""
    data = request.json
    name = data.get('name', '').strip()
    
    if not name:
        return jsonify({'error': 'Tab name required'}), 400
    
    # Tạo ID từ name
    tab_id = 't' + str(len(Tab.query.all()) + 1)
    
    tab = Tab(id=tab_id, name=name)
    db.session.add(tab)
    db.session.commit()
    
    return jsonify(tab.to_dict()), 201


@app.route("/api/flashcard/tabs/<tab_id>", methods=["PUT"])
@flashcard_admin_required
def update_tab(tab_id):
    """Cập nhật thông tin tab (rename)"""
    tab = Tab.query.get(tab_id)
    if not tab:
        return jsonify({'error': 'Tab not found'}), 404
    
    data = request.json
    new_name = data.get('name', '').strip()
    
    if new_name:
        tab.name = new_name
        db.session.commit()
    
    return jsonify(tab.to_dict())


@app.route("/api/flashcard/tabs/<tab_id>", methods=["DELETE"])
@flashcard_admin_required
def delete_tab(tab_id):
    """Xóa một tab"""
    tab = Tab.query.get(tab_id)
    if not tab:
        return jsonify({'error': 'Tab not found'}), 404
    
    db.session.delete(tab)
    db.session.commit()
    
    return jsonify({'message': 'Tab deleted'}), 200


@app.route("/api/flashcard/cards", methods=["POST"])
@flashcard_admin_required
def create_card():
    """Tạo một thẻ flashcard mới"""
    data = request.json
    
    # Validate required fields
    tab_id = data.get('tab_id', '').strip()
    ref = data.get('ref', '').strip()
    title = data.get('title', '').strip()
    
    if not tab_id or not ref or not title:
        return jsonify({'error': 'tab_id, ref, and title required'}), 400
    
    # Check if tab exists
    tab = Tab.query.get(tab_id)
    if not tab:
        return jsonify({'error': 'Tab not found'}), 404
    
    # Create card ID
    card_id = 'c' + str(len(Card.query.all()) + 1)
    
    card = Card(
        id=card_id,
        tab_id=tab_id,
        ref=ref,
        title=title,
        verse=data.get('verse', ''),
        analysis=data.get('analysis', '')
    )
    
    db.session.add(card)
    db.session.commit()
    
    return jsonify(card.to_dict()), 201


@app.route("/api/flashcard/cards/<card_id>", methods=["PUT"])
@flashcard_admin_required
def update_card(card_id):
    """Cập nhật thông tin thẻ"""
    card = Card.query.get(card_id)
    if not card:
        return jsonify({'error': 'Card not found'}), 404
    
    data = request.json
    
    # Update allowed fields
    if 'ref' in data:
        card.ref = data.get('ref', '').strip()
    if 'title' in data:
        card.title = data.get('title', '').strip()
    if 'verse' in data:
        card.verse = data.get('verse', '')
    if 'analysis' in data:
        card.analysis = data.get('analysis', '')
    
    db.session.commit()
    
    return jsonify(card.to_dict())


@app.route("/api/flashcard/cards/<card_id>", methods=["DELETE"])
@flashcard_admin_required
def delete_card(card_id):
    """Xóa một thẻ flashcard"""
    card = Card.query.get(card_id)
    if not card:
        return jsonify({'error': 'Card not found'}), 404
    
    db.session.delete(card)
    db.session.commit()
    
    return jsonify({'message': 'Card deleted'}), 200


@app.route("/api/flashcard/cards/<card_id>/status", methods=["POST"])
@flashcard_api_required
def update_card_status(card_id):
    """Cập nhật trạng thái học thuộc của thẻ"""
    user = session.get("flashcard_user")
    card = Card.query.get(card_id)
    
    if not card:
        return jsonify({'error': 'Card not found'}), 404
    
    data = request.json
    new_status = data.get('status', '').strip()
    
    # Validate status
    if new_status not in ['', 'g', 'r', 'h']:
        return jsonify({'error': 'Invalid status. Must be one of: "", "g", "r", "h"'}), 400
    
    # Find or create CardStatus
    status = CardStatus.query.filter_by(
        card_id=card_id,
        user_id=user
    ).first()
    
    if not status:
        status = CardStatus(card_id=card_id, user_id=user, status=new_status)
        db.session.add(status)
    else:
        status.status = new_status
    
    db.session.commit()
    
    return jsonify(status.to_dict())


@app.route("/api/flashcard/stats")
@flashcard_api_required
def get_flashcard_stats():
    """Lấy thống kê học tập của user"""
    user = session.get("flashcard_user")
    stats = _calculate_stats(user)
    return jsonify(stats)


def _calculate_stats(user):
    """Tính thống kê học tập cho user"""
    total = Card.query.count()
    
    passed = db.session.query(CardStatus).filter_by(
        user_id=user, status='g'
    ).count()
    
    review = db.session.query(CardStatus).filter_by(
        user_id=user, status='r'
    ).count()
    
    hard = db.session.query(CardStatus).filter_by(
        user_id=user, status='h'
    ).count()
    
    not_studied = total - passed - review - hard
    
    return {
        'total': total,
        'passed': passed,
        'review': review,
        'hard': hard,
        'not_studied': not_studied,
        'percentage': round((passed / total * 100) if total > 0 else 0, 1)
    }


if __name__ == "__main__":
    print("🕊️  Khởi động ứng dụng Học Khải Huyền...")
    print("📖  Mở trình duyệt tại: http://localhost:5000")
    app.run(debug=True, host="0.0.0.0", port=5000)
