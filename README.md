# SupportDesk CRM

A lightweight customer support ticket management system built with FastAPI, SQLite, and plain HTML/Tailwind CSS.

## Features

- Create support tickets with customer info, subject, and description
- List all tickets with clean table view
- Live search across names, emails, IDs, and descriptions
- Filter tickets by status (Open / In Progress / Closed)
- View ticket details and full history
- Add notes and update ticket status
- Auto-generated ticket IDs (TKT-001, TKT-002…)

## Tech Stack

| Layer    | Choice               |
|----------|----------------------|
| Backend  | Python + FastAPI     |
| Database | SQLite (built-in)    |
| Frontend | HTML + Tailwind CSS  |
| Deploy   | Railway.app          |

## Local Setup

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/support-crm.git
cd support-crm
```

### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate      # Mac/Linux
venv\Scripts\activate         # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the server
```bash
python main.py
```

Open http://localhost:8000 in your browser.

The SQLite database (`supportdesk.db`) is created automatically on first run.

## API Endpoints

| Method | Endpoint                  | Description              |
|--------|---------------------------|--------------------------|
| POST   | `/api/tickets`            | Create a new ticket      |
| GET    | `/api/tickets`            | List tickets (with optional `?status=` and `?search=`) |
| GET    | `/api/tickets/{ticket_id}`| Get ticket detail + notes|
| PUT    | `/api/tickets/{ticket_id}`| Update status / add note |

Interactive API docs: http://localhost:8000/docs

## Deploy to Railway

1. Push code to GitHub
2. Go to [railway.app](https://railway.app) → New Project → Deploy from GitHub
3. Select your repo — Railway auto-detects Python
4. It reads the `Procfile` and deploys automatically
5. Your app is live at `https://your-app.up.railway.app`

## Project Structure

```
support-crm/
├── main.py            # FastAPI app and routes
├── database.py        # SQLite setup and queries
├── static/
│   └── index.html     # Full frontend (single file)
├── requirements.txt
├── Procfile           # For Railway deployment
├── .env.example
├── .gitignore
└── README.md
```

## Database Schema

**tickets**
```
id, ticket_id (TKT-001), customer_name, customer_email,
subject, description, status, created_at, updated_at
```

**notes**
```
id, ticket_id (FK), note_text, created_at
```
