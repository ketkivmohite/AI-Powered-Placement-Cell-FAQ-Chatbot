from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import or_

from database import engine, SessionLocal
from models import Base, FAQ, ChatHistory
from schemas import FAQCreate, ChatReq

app = FastAPI()

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create Tables
Base.metadata.create_all(bind=engine)


# =========================
# CREATE FAQ
# =========================
@app.post("/faqs")
def create_faq(
    faq: FAQCreate,
    db: Session = Depends(get_db)
):
    new_faq = FAQ(
        question=faq.question,
        answer=faq.answer,
        category=faq.category
    )

    db.add(new_faq)
    db.commit()
    db.refresh(new_faq)

    return {
        "message": "FAQ created successfully",
        "faq": {
            "id": new_faq.id,
            "question": new_faq.question,
            "answer": new_faq.answer,
            "category": new_faq.category
        }
    }


# =========================
# GET ALL FAQS
# =========================
@app.get("/faqs")
def get_faqs(db: Session = Depends(get_db)):
    return db.query(FAQ).all()


# =========================
# SEARCH FAQ
# =========================
@app.get("/faqs/search")
def search_faq(
    query: str,
    db: Session = Depends(get_db)
):
    results = db.query(FAQ).filter(
        or_(
            FAQ.question.ilike(f"%{query}%"),
            FAQ.category.ilike(f"%{query}%")
        )
    ).all()

    return results


# =========================
# GET FAQ BY ID
# =========================
@app.get("/faqs/{id}")
def get_faq(
    id: int,
    db: Session = Depends(get_db)
):
    faq = db.query(FAQ).filter(FAQ.id == id).first()

    if not faq:
        raise HTTPException(
            status_code=404,
            detail="FAQ not found"
        )

    return faq


# =========================
# UPDATE FAQ
# =========================
@app.put("/faqs/{id}")
def update_faq(
    id: int,
    faq: FAQCreate,
    db: Session = Depends(get_db)
):
    existing_faq = db.query(FAQ).filter(
        FAQ.id == id
    ).first()

    if not existing_faq:
        raise HTTPException(
            status_code=404,
            detail="FAQ not found"
        )

    existing_faq.question = faq.question
    existing_faq.answer = faq.answer
    existing_faq.category = faq.category

    db.commit()
    db.refresh(existing_faq)

    return {
        "message": "FAQ updated successfully",
        "faq": {
            "id": existing_faq.id,
            "question": existing_faq.question,
            "answer": existing_faq.answer,
            "category": existing_faq.category
        }
    }


# =========================
# DELETE FAQ
# =========================
@app.delete("/faqs/{id}")
def delete_faq(
    id: int,
    db: Session = Depends(get_db)
):
    faq = db.query(FAQ).filter(
        FAQ.id == id
    ).first()

    if not faq:
        raise HTTPException(
            status_code=404,
            detail="FAQ not found"
        )

    db.delete(faq)
    db.commit()

    return {
        "message": "FAQ deleted successfully"
    }

# =========================
@app.post("/chat")
def chat(
    chat_request: ChatReq,
    db: Session = Depends(get_db)
):
    print("User Message:", chat_request.message)

    faq = db.query(FAQ).filter(
        FAQ.question.ilike(
            f"%{chat_request.message.strip()}%"
        )
    ).first()

    print("FAQ Found:", faq)

    if faq:
        bot_reply = faq.answer
    else:
        bot_reply = "Sorry, I could not find an answer."

    print("Bot Reply:", bot_reply)

    chat = ChatHistory(
        user_message=chat_request.message,
        bot_response=bot_reply
    )

    db.add(chat)
    db.commit()

    return {
        "answer": bot_reply
    }

# =========================
# CHAT HISTORY
# =========================
@app.get("/chat-history")
def get_chat_history(
    db: Session = Depends(get_db)
):
    return db.query(ChatHistory).all()