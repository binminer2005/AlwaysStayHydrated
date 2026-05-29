# 🚀 Flashcard Feature - Quick Start Guide

## What's New

The Flashcard feature has been transformed from a static HTML app into a full-stack web application:
- ✅ Database backend (SQLite)
- ✅ Python API endpoints (Flask)
- ✅ Authentication system (View/Admin roles)
- ✅ Persistent user progress tracking
- ✅ Same beautiful UI design preserved

## Installation (5 minutes)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Initialize Database
```bash
python init_flashcard_db.py
```

Expected output:
```
📖 Reading Flashcard data from HTML file...
📚 Found 43 tabs
  ✓ Tab 'Khải 1:1-8 - Tóm Tắt...': 1000+ cards
...
✅ Database initialized successfully!
   - 43 tabs
   - 1000+ cards
```

### Step 3: Start the App
```bash
python app.py
```

Expected output:
```
🕊️  Khởi động ứng dụng Học Khải Huyền...
📖  Mở trình duyệt tại: http://localhost:5000
```

### Step 4: Access Flashcard
1. Open browser: `http://localhost:5000/flashcard/login`
2. Enter password:
   - **`dongan`** → Study mode (view only)
   - **`donganadmin`** → Edit mode (admin)

## Features

### 📚 Three-Face Card System
- **Face 1**: Title/Main content
- **Face 2**: Scripture/Quote (formatted HTML)
- **Face 3**: Analysis/Interpretation

### 🎯 Learning Status Tracking
- ✓ **Thuộc** (Passed) - Green
- ⟲ **Ôn** (Review) - Yellow  
- ✗ **Khó** (Hard) - Red

### 📊 Progress Dashboard
- Overall progress percentage
- Statistics by status
- Card counter

### 👥 Two-Role System

| Feature | View (dongan) | Admin (donganadmin) |
|---------|---------------|-------------------|
| Study cards | ✅ | ✅ |
| Mark progress | ✅ | ✅ |
| View stats | ✅ | ✅ |
| Edit cards | ❌ | ✅ |
| Create tabs | ❌ | ✅ |
| Delete cards | ❌ | ✅ |

## File Structure

```
📁 khai_huyen/
├── 📄 app.py                    ← Updated with Flashcard APIs
├── 📄 flashcard_models.py       ← NEW: Database models
├── 📄 init_flashcard_db.py      ← NEW: Initialize DB
├── 📄 requirements.txt           ← Updated with Flask-SQLAlchemy
├── 📄 FLASHCARD_README.md       ← Detailed documentation
├── 📄 flashcard.db              ← NEW: Database (auto-created)
├── 📁 templates/
│   ├── 📄 flashcard.html        ← NEW: Main interface
│   ├── 📄 flashcard_login.html  ← NEW: Login page
│   └── ...other files...
└── 📁 Flashcard/
    └── 📄 index.html            ← Original static version (still available)
```

## Common Tasks

### Studying Cards
1. Login with `dongan`
2. Click card to flip through 3 faces
3. Mark your learning status
4. View progress in sidebar

### Adding New Cards (Admin)
1. Login with `donganadmin`
2. Click "+ Thêm Thẻ" button
3. Fill in reference, title, and content
4. Click "Lưu Thẻ"

### Editing Existing Cards (Admin)
1. Click "✎" button on card in list
2. Update content
3. Click "Lưu Thẻ"

### Viewing Statistics
1. Click "Chi tiết" button in Stats panel
2. See breakdown of learning progress

## Database Structure

### Default Empty
If running first time without data:
- Database initializes as empty
- You can manually create tabs/cards via admin interface
- Or run `init_flashcard_db.py` to import from original HTML

### With Data
If `Flashcard/index.html` exists:
- `init_flashcard_db.py` automatically imports all data
- ~43 tabs with 1000+ cards loaded
- All your original content preserved

## API Overview

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/api/flashcard/data` | Load all cards & progress |
| GET | `/api/flashcard/stats` | Get statistics |
| POST | `/api/flashcard/cards/<id>/status` | Update learning status |
| POST | `/api/flashcard/tabs` | Create tab (admin) |
| POST | `/api/flashcard/cards` | Create card (admin) |
| PUT | `/api/flashcard/cards/<id>` | Edit card (admin) |
| DELETE | `/api/flashcard/cards/<id>` | Delete card (admin) |

See `FLASHCARD_README.md` for full API documentation.

## Troubleshooting

### 🔴 "No data showing"
```bash
# Reinitialize database
python init_flashcard_db.py
```

### 🔴 "Login not working"
- Double-check password: `dongan` or `donganadmin`
- Clear browser cache
- Try different browser

### 🔴 "Changes not saving"
- Ensure Flask server is running
- Check browser console for errors
- Verify database write permissions

### 🔴 "Cards won't load"
- Verify `flashcard.db` exists
- Check if `init_flashcard_db.py` completed successfully
- Check Flask server terminal for errors

## Technology Stack

- **Backend**: Python + Flask
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: HTML5 + CSS3 + JavaScript
- **Authentication**: Session-based
- **API Format**: REST + JSON

## Next Steps

1. **Customize**: Modify CSS colors in `flashcard.html` `:root` section
2. **Extend**: Add new features like search, filters, export
3. **Deploy**: Set up on production server with proper security
4. **Backup**: Regular database backups recommended

## Need Help?

### Check Documentation
- Main guide: `FLASHCARD_README.md`
- This quick start: `FLASHCARD_QUICK_START.md`

### Debug
- Browser DevTools Console (F12)
- Flask server terminal output
- Database: Open `flashcard.db` with SQLite viewer

### Common Questions

**Q: Can I have multiple users with separate progress?**
- A: Current system uses session-based tracking. See `FLASHCARD_README.md` for multi-user setup.

**Q: Can I export my data?**
- A: Database is SQLite. Use any SQLite browser to export. Feature can be added.

**Q: Is my data secure?**
- A: This is local application. For production, add proper security measures (see docs).

---

**Status**: ✅ Ready to Use  
**Version**: 1.0  
**Last Updated**: 2026-05-29
