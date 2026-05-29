# 📚 Flashcard Feature - Documentation

## Overview

The Flashcard feature has been successfully migrated from a static HTML/JavaScript application to a full-stack web application powered by:
- **Backend**: Python Flask with SQLAlchemy ORM
- **Database**: SQLite (`flashcard.db`)
- **Frontend**: HTML/CSS/JavaScript with API integration
- **Authentication**: Two-tier access control (View/Admin)

## Architecture

### Database Schema

#### Tab (Danh mục nhóm thẻ)
```
- id (Primary Key): t1, t2, ...
- name (String): "Khải 1:1-8", etc.
- created_at (DateTime)
- updated_at (DateTime)
```

#### Card (Thẻ Flashcard)
```
- id (Primary Key): c1, c2, ...
- tab_id (Foreign Key): Links to Tab
- ref (String): "Khải 1:1" - Reference label
- title (Text): Face 1 - Main content
- verse (Text): Face 2 - Quote/Scripture (HTML supported)
- analysis (Text): Face 3 - Analysis (HTML supported)
- created_at (DateTime)
- updated_at (DateTime)
```

#### CardStatus (Trạng thái học tập)
```
- id (Primary Key)
- card_id (Foreign Key): Links to Card
- user_id (String): Username/Session identifier
- status (String): '', 'g' (passed), 'r' (review), 'h' (hard)
- created_at (DateTime)
- updated_at (DateTime)
- Unique Constraint: (card_id, user_id)
```

## API Endpoints

### Authentication
- **GET** `/api/flashcard/check-auth` - Check login status and role

### Data Retrieval
- **GET** `/api/flashcard/data` - Get all tabs, cards, and current user's progress
- **GET** `/api/flashcard/stats` - Get learning statistics

### Tab Management (Admin Only)
- **POST** `/api/flashcard/tabs` - Create new tab
- **PUT** `/api/flashcard/tabs/<id>` - Update tab name
- **DELETE** `/api/flashcard/tabs/<id>` - Delete tab

### Card Management (Admin Only)
- **POST** `/api/flashcard/cards` - Create new card
- **PUT** `/api/flashcard/cards/<id>` - Update card content
- **DELETE** `/api/flashcard/cards/<id>` - Delete card

### Status Management (All Users)
- **POST** `/api/flashcard/cards/<id>/status` - Update learning status
  - Payload: `{ "status": "g" | "r" | "h" | "" }`

## Features

### 🎯 Flashcard Learning Interface
- **3-Face Card System**:
  - Face 1: Title/Main content
  - Face 2: Scripture/Quote (italic, HTML formatted)
  - Face 3: Analysis/Interpretation
- **Card Flip Animation**: 120° rotation for smooth 3D transitions
- **Progress Tracking**: Visual progress bar + statistics

### 📊 Status Management
- **Passed (✓ Thuộc)**: Green status - thoroughly learned
- **Review (⟲ Ôn)**: Yellow status - needs periodic review
- **Hard (✗ Khó)**: Red status - difficult, needs more practice
- **Unstudied**: Default - not yet studied

### 👤 Role-Based Access
- **View Role** (`dongan`):
  - View all cards and tabs
  - Mark learning status
  - View personal statistics
  - Cannot edit or create cards

- **Admin Role** (`donganadmin`):
  - All View role permissions
  - Create, edit, delete tabs
  - Create, edit, delete cards
  - Manage all content

### 📈 Statistics
- Total cards count
- Passed cards count
- Cards needing review
- Difficult cards
- Overall progress percentage

### 📝 Rich Content Support
- HTML formatting in verse and analysis fields
- Support for bold, italic, underline, colors
- Bullet lists and other HTML structures

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Initialize Database
```bash
python init_flashcard_db.py
```

This script will:
- Create the SQLite database (`flashcard.db`)
- Parse the existing Flashcard HTML file
- Populate the database with initial data from DEFAULT_DATA

### 3. Run the Application
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Usage

### Accessing Flashcard
1. Navigate to `http://localhost:5000/flashcard/login`
2. Enter password:
   - `dongan` - View mode (study only)
   - `donganadmin` - Admin mode (edit content)

### Learning (View Mode)
1. Select a tab from the top tabs bar
2. Click on the card to flip through the 3 faces
3. Use navigation buttons (← Trước / Sau →) to move between cards
4. Mark your progress using status buttons:
   - ✓ Thuộc (Passed)
   - ⟲ Ôn (Review)
   - ✗ Khó (Hard)
5. View statistics in the right sidebar

### Content Management (Admin Mode)
1. Login with `donganadmin` password
2. All View mode features plus:
3. Click "✎" button on any card to edit
4. Click "+ Thêm Thẻ" button to create new card
5. Manage tabs (rename, create, delete)

## File Structure

```
├── app.py                          # Main Flask application
├── flashcard_models.py             # SQLAlchemy database models
├── init_flashcard_db.py            # Database initialization script
├── requirements.txt                # Python dependencies
├── flashcard.db                    # SQLite database (auto-created)
├── templates/
│   ├── flashcard_login.html       # Login page
│   ├── flashcard.html             # Main interface
│   └── ...other templates...
├── static/
│   └── ...static files...
└── Flashcard/
    ├── index.html                 # Original static flashcard (for data import)
    └── ...
```

## Technical Details

### Session Management
- Flashcard uses separate session keys: `flashcard_user` and `flashcard_role`
- Sessions are independent from the main app login system
- Sessions are stored in Flask server memory

### Data Format
- All text content supports HTML formatting
- Status values: empty string (default), 'g', 'r', 'h'
- Card references use format like "Khải 1:1"

### API Response Format
All APIs return JSON with this structure:
```json
{
  "data": { /* endpoint-specific data */ },
  "error": null // Only if error occurred
}
```

### Error Handling
- **401 Unauthorized**: User not logged in to flashcard
- **403 Forbidden**: User lacks admin privileges
- **404 Not Found**: Resource not found
- **400 Bad Request**: Invalid request data

## Migration from Static Version

### Original Structure (Static HTML)
- Data stored in `DEFAULT_DATA` constant in HTML
- Client-side only logic
- Static passwords checked in JavaScript
- No persistent user progress

### New Structure (Dynamic)
- Data stored in SQLite database
- Backend handles all business logic
- Secure server-side authentication
- Persistent user progress tracking
- Real-time data updates

### Data Import
The `init_flashcard_db.py` script automatically:
1. Reads the existing `Flashcard/index.html`
2. Extracts `DEFAULT_DATA` from JavaScript
3. Parses and validates the JSON structure
4. Populates the database

## Customization

### Adding New Tabs
1. Login as admin
2. Tabs are managed through API (UI feature can be added)
3. Or use init script with modified data

### Custom Styling
- All CSS variables defined in `:root`
- Colors follow design system (accent, gold, rose, etc.)
- Responsive design included for mobile devices

### Adding Rich Text Editor
The frontend currently supports:
- Plain text input
- HTML paste for complex formatting
- Direct HTML editing in textarea

To add a WYSIWYG editor:
1. Install editor library (e.g., TinyMCE, Quill)
2. Replace textarea with editor instance
3. Update form submission to get HTML from editor

## Performance Considerations

### Database Optimization
- Indexes on frequently queried fields (card_id, user_id)
- Lazy loading for related records
- Card list cached in frontend after initial load

### Frontend Optimization
- Minimal API calls (single data fetch per page load)
- Progress updates only when status changes
- Card flip uses CSS transforms (GPU accelerated)

### Caching Suggestions
- Cache stats calculations for performance
- Implement card list pagination for large datasets
- Use database query optimization for >10,000 cards

## Troubleshooting

### Database Won't Initialize
```bash
# Delete old database and reinitialize
rm flashcard.db
python init_flashcard_db.py
```

### Cards Not Showing
1. Check if `init_flashcard_db.py` was run
2. Verify `Flashcard/index.html` exists
3. Check browser console for API errors
4. Ensure Flask server is running

### Login Issues
- Verify passwords: `dongan` or `donganadmin`
- Check browser cookies/session
- Clear browser cache and try again

### Data Not Persisting
- Ensure `flashcard.db` file has write permissions
- Check Flask server logs for database errors
- Verify SQLAlchemy connection string

## Security Notes

⚠️ **Important**: This is a local/internal application. For production deployment:
1. Use environment variables for sensitive data
2. Implement proper user authentication system
3. Add CSRF protection
4. Use HTTPS/TLS
5. Add rate limiting
6. Implement audit logging
7. Use strong session management
8. Add input validation and sanitization

## Future Enhancements

Possible improvements:
- [ ] WYSIWYG rich text editor for card editing
- [ ] Export/import functionality (Excel, JSON)
- [ ] Card review scheduling (spaced repetition)
- [ ] Multiple user support with separate progress
- [ ] Search and filter functionality
- [ ] Card tagging/categorization
- [ ] Progress analytics and charts
- [ ] Mobile app version
- [ ] Offline mode support
- [ ] Collaborative editing

## Support & Questions

For issues or questions:
1. Check the troubleshooting section above
2. Review error messages in browser console
3. Check Flask server logs
4. Examine database structure with SQLite viewer

---

**Version**: 1.0  
**Last Updated**: 2026-05-29  
**Status**: Production Ready ✅
