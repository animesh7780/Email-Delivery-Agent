from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
import json

from database import get_db, init_db, Email, Prompt, Draft
from models import (
    EmailCreate, EmailResponse, PromptCreate, PromptResponse, PromptUpdate,
    DraftCreate, DraftResponse, ProcessEmailRequest, ChatRequest
)
from llm_service import llm_service

app = FastAPI(title="Email Productivity Agent API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    init_db()


# Email Endpoints
@app.get("/api/emails", response_model=List[EmailResponse])
async def get_emails(
    category: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all emails with optional category filter"""
    query = db.query(Email)
    if category:
        query = query.filter(Email.category == category)
    emails = query.offset(skip).limit(limit).all()
    return emails


@app.get("/api/emails/{email_id}", response_model=EmailResponse)
async def get_email(email_id: int, db: Session = Depends(get_db)):
    """Get a specific email by ID"""
    email = db.query(Email).filter(Email.id == email_id).first()
    if not email:
        raise HTTPException(status_code=404, detail="Email not found")
    return email


@app.post("/api/emails", response_model=EmailResponse)
async def create_email(email: EmailCreate, db: Session = Depends(get_db)):
    """Create a new email"""
    db_email = Email(**email.dict())
    db.add(db_email)
    db.commit()
    db.refresh(db_email)
    return db_email


@app.put("/api/emails/{email_id}/read")
async def mark_email_read(email_id: int, db: Session = Depends(get_db)):
    """Mark an email as read"""
    email = db.query(Email).filter(Email.id == email_id).first()
    if not email:
        raise HTTPException(status_code=404, detail="Email not found")
    email.is_read = True
    db.commit()
    return {"message": "Email marked as read"}


@app.post("/api/emails/{email_id}/process")
async def process_email(email_id: int, request: ProcessEmailRequest, db: Session = Depends(get_db)):
    """Process an email with AI tasks"""
    email = db.query(Email).filter(Email.id == email_id).first()
    if not email:
        raise HTTPException(status_code=404, detail="Email not found")
    
    results = {}
    
    # Get custom prompts if available
    categorization_prompt = db.query(Prompt).filter(
        Prompt.prompt_type == "categorization", Prompt.is_active == True
    ).first()
    
    task_extraction_prompt = db.query(Prompt).filter(
        Prompt.prompt_type == "task_extraction", Prompt.is_active == True
    ).first()
    
    auto_reply_prompt = db.query(Prompt).filter(
        Prompt.prompt_type == "auto_reply", Prompt.is_active == True
    ).first()
    
    # Categorize email
    if "categorize" in request.tasks:
        cat_result = await llm_service.categorize_email(
            email.subject, 
            email.body,
            categorization_prompt.content if categorization_prompt else None
        )
        email.category = cat_result.get("category", "Uncategorized")
        email.priority = cat_result.get("priority", "Medium")
        email.sentiment = cat_result.get("sentiment", "Neutral")
        results["categorization"] = cat_result
    
    # Extract action items
    if "extract_tasks" in request.tasks:
        task_result = await llm_service.extract_action_items(
            email.subject,
            email.body,
            task_extraction_prompt.content if task_extraction_prompt else None
        )
        email.has_action_items = task_result.get("has_action_items", False)
        email.action_items = json.dumps(task_result.get("action_items", []))
        results["action_items"] = task_result
    
    # Generate draft reply
    if "generate_draft" in request.tasks:
        draft_result = await llm_service.generate_draft_reply(
            email.subject,
            email.body,
            custom_prompt=auto_reply_prompt.content if auto_reply_prompt else None
        )
        
        # Save draft
        draft = Draft(
            email_id=email.id,
            subject=draft_result.get("subject", f"Re: {email.subject}"),
            body=draft_result.get("body", ""),
            tone="professional"
        )
        db.add(draft)
        results["draft"] = draft_result
    
    db.commit()
    db.refresh(email)
    
    return {
        "email": EmailResponse.from_orm(email),
        "results": results
    }


# Prompt Endpoints
@app.get("/api/prompts", response_model=List[PromptResponse])
async def get_prompts(db: Session = Depends(get_db)):
    """Get all prompts"""
    return db.query(Prompt).all()


@app.get("/api/prompts/{prompt_id}", response_model=PromptResponse)
async def get_prompt(prompt_id: int, db: Session = Depends(get_db)):
    """Get a specific prompt"""
    prompt = db.query(Prompt).filter(Prompt.id == prompt_id).first()
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    return prompt


@app.post("/api/prompts", response_model=PromptResponse)
async def create_prompt(prompt: PromptCreate, db: Session = Depends(get_db)):
    """Create a new prompt"""
    db_prompt = Prompt(**prompt.dict())
    db.add(db_prompt)
    db.commit()
    db.refresh(db_prompt)
    return db_prompt


@app.put("/api/prompts/{prompt_id}", response_model=PromptResponse)
async def update_prompt(prompt_id: int, prompt: PromptUpdate, db: Session = Depends(get_db)):
    """Update a prompt"""
    db_prompt = db.query(Prompt).filter(Prompt.id == prompt_id).first()
    if not db_prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    
    update_data = prompt.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_prompt, key, value)
    
    db.commit()
    db.refresh(db_prompt)
    return db_prompt


@app.delete("/api/prompts/{prompt_id}")
async def delete_prompt(prompt_id: int, db: Session = Depends(get_db)):
    """Delete a prompt"""
    prompt = db.query(Prompt).filter(Prompt.id == prompt_id).first()
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    db.delete(prompt)
    db.commit()
    return {"message": "Prompt deleted"}


# Draft Endpoints
@app.get("/api/drafts", response_model=List[DraftResponse])
async def get_drafts(email_id: Optional[int] = None, db: Session = Depends(get_db)):
    """Get all drafts"""
    query = db.query(Draft)
    if email_id:
        query = query.filter(Draft.email_id == email_id)
    return query.all()


@app.get("/api/drafts/{draft_id}", response_model=DraftResponse)
async def get_draft(draft_id: int, db: Session = Depends(get_db)):
    """Get a specific draft"""
    draft = db.query(Draft).filter(Draft.id == draft_id).first()
    if not draft:
        raise HTTPException(status_code=404, detail="Draft not found")
    return draft


# Chat Endpoint
@app.post("/api/chat")
async def chat(request: ChatRequest, db: Session = Depends(get_db)):
    """Chat with the email assistant"""
    # Get inbox context
    emails = db.query(Email).all()
    context = f"User has {len(emails)} emails. "
    
    unread = sum(1 for e in emails if not e.is_read)
    context += f"{unread} unread. "
    
    categories = {}
    for e in emails:
        categories[e.category] = categories.get(e.category, 0) + 1
    context += f"Categories: {categories}"
    
    response = await llm_service.chat_about_inbox(request.message, context)
    return {"response": response}


# Statistics Endpoint
@app.get("/api/stats")
async def get_stats(db: Session = Depends(get_db)):
    """Get inbox statistics"""
    emails = db.query(Email).all()
    
    stats = {
        "total_emails": len(emails),
        "unread_count": sum(1 for e in emails if not e.is_read),
        "categories": {},
        "priorities": {},
        "action_items_count": sum(1 for e in emails if e.has_action_items),
        "drafts_count": db.query(Draft).count()
    }
    
    for email in emails:
        stats["categories"][email.category] = stats["categories"].get(email.category, 0) + 1
        stats["priorities"][email.priority] = stats["priorities"].get(email.priority, 0) + 1
    
    return stats


if __name__ == "__main__":
    import uvicorn
    from config import settings
    uvicorn.run(app, host=settings.host, port=settings.port)
