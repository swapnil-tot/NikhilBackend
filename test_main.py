import pytest
from fastapi.testclient import TestClient
from main import app, get_db, Message, Chat
from sqlalchemy.orm import Session
from datetime import datetime


@pytest.fixture(scope="module")
def test_db():
    # Setup
    db = next(get_db())
    message1 = Message(text="Hello", sender="user", chat_id=1, created_at=datetime.utcnow())
    message2 = Message(text="Hi there", sender="system", chat_id=1, created_at=datetime.utcnow())
    chat = Chat(id=1, messages=[message1, message2])
    db.add(chat)
    db.commit()
    yield db
    # Teardown
    db.rollback()
    db.close()


def test_get_last_message(test_db):
    client = TestClient(app)
    response = client.get("/last_message/1")
    assert response.status_code == 200
    assert response.json() == {"text": "Hi there", "sender": "system", "created_at": response.json()["created_at"], "system": True}


def test_get_last_message_chat_not_found(test_db):
    client = TestClient(app)
    response = client.get("/last_message/2")
    assert response.status_code == 404
    assert response.json() == {"detail": "Chat not found"}


def test_get_last_message_chat_empty(test_db):
    client = TestClient(app)
    response = client.get("/last_message/3")
    assert response.status_code == 404
    assert response.json() == {"detail": "Chat is empty"}
