from fastapi import FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
import database
import uvicorn

app = FastAPI(title="SupportDesk CRM")

# Serve frontend
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def root():
    return FileResponse("static/index.html")

# ── Schemas ──────────────────────────────────────────────

class CreateTicket(BaseModel):
    customer_name: str
    customer_email: str
    subject: str
    description: str

class UpdateTicket(BaseModel):
    status: Optional[str] = None
    note: Optional[str] = None

# ── Routes ───────────────────────────────────────────────

@app.post("/api/tickets", status_code=201)
def create_ticket(body: CreateTicket):
    ticket = database.create_ticket(
        body.customer_name, body.customer_email,
        body.subject, body.description
    )
    return ticket

@app.get("/api/tickets")
def list_tickets(
    status: Optional[str] = Query(None),
    search: Optional[str] = Query(None)
):
    return database.get_tickets(status=status, search=search)

@app.get("/api/tickets/{ticket_id}")
def get_ticket(ticket_id: str):
    ticket = database.get_ticket(ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket

@app.put("/api/tickets/{ticket_id}")
def update_ticket(ticket_id: str, body: UpdateTicket):
    ticket = database.get_ticket(ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    result = database.update_ticket(ticket_id, body.status, body.note)
    return result

# ── Dev server ───────────────────────────────────────────

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
