from fastapi import FastAPI,HTTPException,Depends
from models import Todo, session,get_db,Chat,Message
from requests import Session

app = FastAPI()

#api for getting the last message of the specified chat id
@app.get("/last_message/{chat_uuid}", summary="Retrieve last message from a user in a chat")
def get_last_message(chat_uuid: int, db: Session = Depends(get_db)):
      
    chat = db.query(Chat).filter(Chat.id == chat_uuid).first()
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    if not chat.messages:
        raise HTTPException(status_code=404, detail="Chat is empty")

    last_message = chat.messages[-1]
    return {
        "text": last_message.text,
        "sender": last_message.sender,
        "created_at": last_message.created_at,
        "system": last_message.is_system_message
    }

#api to insert the messages for the specific id.
@app.post("/messages/", summary="Create a new message")
def create_message(text: str, sender: str, chat_id: int, db: Session = Depends(get_db)):

    chat = db.query(Chat).filter(Chat.id == chat_id).first()
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")

    new_message = Message(text=text, sender=sender, chat_id=chat_id)
    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    return new_message


#initialize the chat with the new chat id
@app.post("/first_message",summary="Initial message with chat id")
def initial_msg(db:Session=Depends(get_db)):
    new_chat = Chat()
    db.add(new_chat)
    db.commit()
    db.refresh(new_chat)
    return new_chat

#api to get all the messages.
@app.get("/messages/", summary="Get all messages")
def get_all_messages(db: Session = Depends(get_db)):

    messages = db.query(Message).all()
    return messages