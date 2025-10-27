# Hospital Records Management - Web Application

Flask web version of the PyQt5 hospital records management system.

## Features

- User login/authentication
- Search patient records
- View and download patient records
- Upload new patient records
- Update existing patient records
- ABE encryption for access control

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Copy the background image:
```bash
mkdir -p static/images
cp ../client/bg.jpg static/images/
```

3. Make sure the Trusted Authority and Cloud Storage servers are running:
```bash
# Terminal 1 - Trusted Authority
cd ../trusted_authority/server
python3 app.py

# Terminal 2 - Cloud Storage
cd ../cloud_storage/server
python3 app.py
```

4. Run the web application:
```bash
python3 app.py
```

5. Access the application at: http://localhost:3000

## Default Login Credentials

Same as the PyQt5 application - check with your system administrator.

## File Structure

```
web/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── templates/          # HTML templates
│   ├── base.html
│   ├── login.html
│   ├── menu.html
│   ├── search.html
│   ├── view.html
│   ├── upload.html
│   └── update.html
├── static/             # Static files
│   ├── css/
│   │   └── style.css
│   └── images/
│       └── bg.jpg
└── downloads/          # Downloaded files (auto-created)
```

## Notes

- Downloaded files are saved in the `downloads/` folder
- The application uses the same ABE encryption as the PyQt5 client
- Sessions are stored server-side with Flask sessions
- Background image must be placed in `static/images/bg.jpg`
