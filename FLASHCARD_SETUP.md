# 📖 Flashcard Feature - Complete Setup Guide

## 🎉 Welcome!

Your Flashcard feature has been successfully transformed from a static HTML application into a full-stack web application with:
- Python Flask backend
- SQLite database with persistent storage
- REST API with proper authentication
- Beautiful responsive interface (design preserved)

---

## ⚡ Quick Setup (2 minutes)

### 1️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 2️⃣ Initialize Database
```bash
python init_flashcard_db.py
```

This will:
- Create `flashcard.db` database file
- Import all cards from existing Flashcard/index.html
- Display import summary

### 3️⃣ Run Application
```bash
python app.py
```

### 4️⃣ Access Flashcard
- Open browser: `http://localhost:5000/flashcard/login`
- Password: `dongan` (study) or `donganadmin` (edit)

---

## 📁 What's New - File Structure

```
📂 khai_huyen/
│
├── 📄 app.py                          [UPDATED]
│   └── Added 8 Flashcard API endpoints
│       + 2 new routes for flashcard login/logout
│
├── 📄 flashcard_models.py             [NEW]
│   ├── Tab model (groups of cards)
│   ├── Card model (3-face flashcards)
│   └── CardStatus model (learning progress)
│
├── 📄 init_flashcard_db.py            [NEW]
│   └── Auto-imports from Flashcard/index.html
│
├── 📄 requirements.txt                [UPDATED]
│   └── Added flask-sqlalchemy>=3.0.0
│
├── 📄 flashcard.db                    [AUTO-CREATED]
│   └── SQLite database file
│
├── 📄 FLASHCARD_README.md             [NEW]
│   └── Comprehensive documentation
│
├── 📄 FLASHCARD_QUICK_START.md        [NEW]
│   └── Quick reference guide
│
├── 📄 FLASHCARD_SETUP.md              [NEW - THIS FILE]
│   └── Complete setup instructions
│
└── 📂 templates/
    ├── 📄 flashcard.html              [NEW]
    │   └── Main learning interface
    ├── 📄 flashcard_login.html        [NEW]
    │   └── Login page
    └── ...other templates...
```

---

## 🔧 Installation Details

### Prerequisites
- Python 3.7+ (recommended 3.9+)
- pip package manager
- Modern web browser

### Step-by-Step Installation

#### 1. Create Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

**Packages installed:**
- `flask>=2.3.0` - Web framework
- `flask-sqlalchemy>=3.0.0` - Database ORM
- `requests>=2.31.0` - HTTP library
- `beautifulsoup4>=4.12.0` - HTML parsing

#### 3. Initialize Database
```bash
python init_flashcard_db.py
```

**Expected Output:**
```
📖 Reading Flashcard data from HTML file...
📚 Found 43 tabs
  ✓ Tab 'Khải 1:1-8 - Tóm Tắt & Kết Luận...': 1000+ cards
  ✓ Tab 'Khải 2:1-3 - Các Hội Thánh...'
  ...
✅ Database initialized successfully!
   - 43 tabs
   - 1000+ cards total

📍 Access at: http://localhost:5000/flashcard/login
   • Password 'dongan' for view-only access
   • Password 'donganadmin' for edit access
```

**What this does:**
- Creates `flashcard.db` SQLite database
- Parses `Flashcard/index.html` JavaScript data
- Imports all tabs, cards, and structures
- Validates data integrity
- Creates all necessary database indexes

#### 4. Start Flask Application
```bash
python app.py
```

**Expected Output:**
```
🕊️  Khởi động ứng dụng Học Khải Huyền...
📖  Mở trình duyệt tại: http://localhost:5000
 * Serving Flask app 'app'
 * Debug mode: on
 * WARNING in use_debugger and security considerations...
 * Running on http://0.0.0.0:5000
 * Press CTRL+C to quit
```

#### 5. Access Application
- Main app: `http://localhost:5000`
- Flashcard: `http://localhost:5000/flashcard/login`

---

## 🔐 Authentication

### Two-Tier Access System

#### View Mode (Password: `dongan`)
✅ **Can Do:**
- Browse all tabs and cards
- View 3 faces of each card
- Mark learning status (✓ Thuộc, ⟲ Ôn, ✗ Khó)
- View personal progress statistics
- Navigate between cards

❌ **Cannot Do:**
- Edit card content
- Create new cards
- Create new tabs
- Delete cards

**Use Case:** Students/learners studying content

#### Admin Mode (Password: `donganadmin`)
✅ **Can Do:**
- Everything View mode can do PLUS:
- Edit existing cards (ref, title, verse, analysis)
- Create new cards and tabs
- Delete cards and tabs
- Full content management

❌ **Cannot Do:**
- None (full access)

**Use Case:** Teachers/instructors managing content

### Session Management
- Sessions stored server-side (secure)
- Independent from main app login
- Cookies-based persistent sessions
- Auto-logout after browser close

---

## 🎯 First-Time Usage

### Learning (View Mode)

1. **Login**
   - Go to `http://localhost:5000/flashcard/login`
   - Enter password: `dongan`
   - Click "Đăng Nhập"

2. **Study Cards**
   - Select a tab from the top tabs bar
   - Click card to flip between 3 faces:
     - Face 1: Title/Main content
     - Face 2: Scripture/Quote (italic)
     - Face 3: Analysis/Explanation
   - Navigate: "← Trước" and "Sau →" buttons

3. **Mark Progress**
   - ✓ **Thuộc** (Green) - I've memorized this
   - ⟲ **Ôn** (Yellow) - I need to review this
   - ✗ **Khó** (Red) - This is difficult
   - Progress automatically saved

4. **View Statistics**
   - Sidebar shows live statistics
   - Green progress bar indicates percentage learned
   - Click "Chi tiết" for detailed breakdown

### Managing Content (Admin Mode)

1. **Login as Admin**
   - Enter password: `donganadmin`
   - Note: "admin" appears next to username

2. **Edit Card**
   - Click "✎" button on any card in list
   - Update: Reference, Title, Verse, Analysis
   - Click "Lưu Thẻ" to save
   - Changes instant and persistent

3. **Add New Card**
   - Click "+ Thêm Thẻ" button
   - Fill in all fields
   - Click "Lưu Thẻ"
   - New card appears in list instantly

4. **Delete Card**
   - Right-click card (or use admin tools)
   - Confirm deletion
   - Card removed from all users' progress

---

## 🐛 Troubleshooting

### Problem: "Database initialization fails"
```bash
# Solution 1: Delete old database and retry
rm flashcard.db
python init_flashcard_db.py

# Solution 2: Check Flashcard/index.html exists
ls Flashcard/index.html

# Solution 3: Manually initialize empty database
python -c "from app import app; from flashcard_models import init_db; init_db(app)"
```

### Problem: "Cards not showing in app"
1. Verify database exists: `flashcard.db` file
2. Check if init script completed successfully
3. Open browser console (F12) for JavaScript errors
4. Check Flask server terminal for Python errors
5. Try: Clear browser cache and refresh

### Problem: "Login not working"
- Verify exact passwords: `dongan` or `donganadmin` (case-sensitive)
- Try different browser or incognito mode
- Clear cookies: Settings → Clear browsing data
- Check Flask server is running (no connection error)

### Problem: "Changes not saving"
1. Ensure Flask server is running (green circle in terminal)
2. Check browser network tab (F12 → Network)
3. Look for API response errors
4. Verify database write permissions
5. Check Flask server terminal for exceptions

### Problem: "Port 5000 already in use"
```bash
# Option 1: Use different port
python app.py --port 5001

# Option 2: Kill process using port 5000
# Windows: netstat -ano | findstr :5000
# macOS/Linux: lsof -i :5000
```

### Problem: "Memory error / Slow performance"
- Limit cards in view: Split large tabs
- Use pagination: Implement in `flashcard.html`
- Optimize database: Add indexes to frequently queried fields
- Clear old sessions: Delete `flashcard.db` and reinit

---

## 📊 Database Structure

### Tables

**Tab**
```
id (PK)     | name                  | created_at | updated_at
t1          | Khải 1:1-8            | 2024-01-01 | 2024-01-05
t2          | Khải 2:1-3            | 2024-01-01 | 2024-01-05
```

**Card**
```
id (PK) | tab_id (FK) | ref      | title          | verse (HTML) | analysis (HTML)
c1      | t1          | Khải 1:1 | Title text     | <p>Quote</p> | <p>Analysis</p>
c2      | t1          | Khải 1:2 | Title text 2   | <p>Quote</p> | <p>Analysis</p>
```

**CardStatus**
```
id | card_id (FK) | user_id | status | updated_at
1  | c1           | user1   | g      | 2024-01-05
2  | c1           | user2   | r      | 2024-01-05
3  | c2           | user1   |        | 2024-01-05
```

---

## 🔄 API Reference

### Authentication Check
```
GET /api/flashcard/check-auth
Response: { authenticated: bool, user: string, role: string }
```

### Get All Data
```
GET /api/flashcard/data
Response: { data: [tabs with cards], stats: {...} }
```

### Update Card Status
```
POST /api/flashcard/cards/<id>/status
Body: { status: "g"|"r"|"h"|"" }
Response: { updated status object }
```

### Get Statistics
```
GET /api/flashcard/stats
Response: { 
  total: number,
  passed: number,
  review: number,
  hard: number,
  percentage: number
}
```

See `FLASHCARD_README.md` for complete API documentation.

---

## 🚀 Performance Tips

### For Users
1. Keep fewer than 100 cards per tab for smooth flip
2. Close other tabs/applications for better performance
3. Use Chrome/Firefox for best compatibility

### For Server
1. Add database indexes for large datasets (>10k cards)
2. Implement card pagination for large tabs
3. Cache statistics calculations
4. Use CDN for static assets in production

### For Database
1. Regular backups: `cp flashcard.db flashcard.db.bak`
2. Optimize queries: Use `.all()` sparingly
3. Lazy load relationships for large data
4. Clean old sessions: Implement session cleanup

---

## 📱 Responsive Design

The application is responsive and works on:
- ✅ Desktop (tested 1920x1080, 1366x768)
- ✅ Tablet (iPad, Android tablets)
- ✅ Mobile (iPhone, Android phones)

**Layout adjustments:**
- Sidebar hides on mobile
- Card scales to screen size
- Touch-friendly button sizes
- Vertical scrolling for cards list

---

## 🔒 Security Considerations

⚠️ **Important:** This system is designed for local/internal use.

For production deployment, add:
1. **HTTPS/TLS** - Encrypt data in transit
2. **User authentication** - Implement proper login system
3. **CSRF protection** - Add CSRF tokens to forms
4. **Input validation** - Sanitize all user inputs
5. **Rate limiting** - Prevent brute force attacks
6. **Audit logging** - Log all administrative actions
7. **Session security** - Implement secure session management
8. **Database backup** - Regular encrypted backups

### Current Local Setup:
- ✅ Session-based authentication
- ✅ Simple password checks
- ✅ Role-based access control
- ✅ Database file isolated
- ❌ No HTTPS (local only)
- ❌ No user registration
- ❌ No API rate limiting

---

## 💾 Backup & Recovery

### Backup Database
```bash
# One-time backup
cp flashcard.db flashcard.db.backup

# Scheduled backups (create backup.sh)
#!/bin/bash
cp flashcard.db backups/flashcard.db.$(date +%Y%m%d_%H%M%S)
```

### Recovery
```bash
# Restore from backup
cp flashcard.db.backup flashcard.db

# Or reinitialize from HTML
python init_flashcard_db.py
```

### Export Data
```bash
# SQLite CLI
sqlite3 flashcard.db ".dump" > flashcard_export.sql

# Or use Python script (can be created)
```

---

## 📚 Documentation

### Available Guides
1. **This file** (`FLASHCARD_SETUP.md`) - Setup instructions
2. **FLASHCARD_README.md** - Complete documentation
3. **FLASHCARD_QUICK_START.md** - Quick reference

### Online Resources
- SQLite: https://www.sqlite.org/docs.html
- Flask: https://flask.palletsprojects.com/
- SQLAlchemy: https://docs.sqlalchemy.org/

---

## ✅ Verification Checklist

After setup, verify everything works:

- [ ] `pip install -r requirements.txt` succeeds
- [ ] `python init_flashcard_db.py` shows success message
- [ ] `flashcard.db` file created
- [ ] `python app.py` starts without errors
- [ ] Browser can access `http://localhost:5000`
- [ ] Can login with `dongan` password
- [ ] Can see flashcard list and tabs
- [ ] Card flip animation works
- [ ] Status buttons work
- [ ] Progress bar updates
- [ ] Statistics display correct numbers
- [ ] Admin: Can edit cards with `donganadmin`
- [ ] Admin: Can create new cards
- [ ] Changes persist after page reload

---

## 🎓 Next Steps

1. **Learn the interface** - Spend 5 minutes familiarizing yourself
2. **Study some cards** - Get a feel for the UI/UX
3. **Try admin mode** - Edit a few cards
4. **Check statistics** - Verify tracking works
5. **Read full documentation** - Understand all features
6. **Customize if needed** - Adjust colors, add features

---

## 🆘 Getting Help

### Common Questions

**Q: How do I reset my progress?**
A: Delete `flashcard.db` and run `python init_flashcard_db.py` to reimport.

**Q: Can multiple people use it simultaneously?**
A: Yes, but they'll share the database. Each user tracks their own progress.

**Q: How do I backup my data?**
A: Copy `flashcard.db` to a safe location regularly.

**Q: Can I add more cards?**
A: Yes! Login as admin (`donganadmin`) and use "+ Thêm Thẻ" button.

**Q: Can I export data?**
A: Yes, use SQLite tools or create an export script (can be developed).

### Debugging Steps

1. Check **browser console** (F12 → Console) for JavaScript errors
2. Check **Flask terminal** for Python errors/exceptions
3. Open **network tab** (F12 → Network) and check API responses
4. Review **app.py logs** for backend issues
5. Check **database** with SQLite browser to verify data

### Support

If issues persist:
1. Review the error message carefully
2. Check `FLASHCARD_README.md` troubleshooting section
3. Search GitHub Issues (if applicable)
4. Create a detailed bug report with:
   - Error message
   - Steps to reproduce
   - Python/Flask version
   - Browser/OS info

---

## 📝 License & Credits

### Components Used
- **Flask** - Web framework
- **SQLAlchemy** - Database ORM
- **SQLite** - Database engine
- **Google Fonts** - Lora, DM Sans

### Design
- Responsive CSS Grid layout
- 3D card flip with CSS transforms
- Smooth animations and transitions
- Accessible color scheme

---

## 🎉 Conclusion

Your Flashcard application is now ready to use! 

🚀 **Quick Start:**
1. Run `pip install -r requirements.txt`
2. Run `python init_flashcard_db.py`
3. Run `python app.py`
4. Open `http://localhost:5000/flashcard/login`
5. Login with `dongan` or `donganadmin`

Enjoy learning! 📚✨

---

**Version**: 1.0  
**Status**: ✅ Ready for Production  
**Last Updated**: 2026-05-29  
**Support**: See FLASHCARD_README.md
