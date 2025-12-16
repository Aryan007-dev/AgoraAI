from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from pathlib import Path
from typing import Dict
import json
import asyncio
import uuid

from models import ChatLog, ChatroomLog
from database import SessionLocal
from agents2 import AGENTS


# ------------------------ FASTAPI APP ------------------------
app = FastAPI()


# ------------------------ DB LOGGING ------------------------
def log_chat(db: Session, role: str, content: str, ai_name: str | None = None):
    row = ChatLog(role=role, content=content, ai_name=ai_name)
    db.add(row)
    db.commit()


def log_chatroom(
    db: Session,
    role: str,
    chatroom_id: str,
    message: str,
    ai_name: str | None = None
):
    row = ChatroomLog(
        role=role,
        chatroom_id=chatroom_id,
        message=message,
        ai_name=ai_name
    )
    db.add(row)
    db.commit()


# ------------------------ ROUTES ------------------------
@app.get("/")
async def read_root():
    return {"message": "server is running!"}


@app.get("/chat")
def chat_page():
    html = Path("app/front.html").read_text()
    return HTMLResponse(html)


# ------------------------ CONNECTION MANAGER ------------------------
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []
        self.chatroom: Dict | None = None  # holds active chatroom state

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        print("NEW client connected. Total:", len(self.active_connections))

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        print("Client DISCONNECTED. Remaining:", len(self.active_connections))

    async def broadcast(self, message: Dict):
        for connection in self.active_connections:
            await connection.send_text(json.dumps(message))


manager = ConnectionManager()


# ------------------------ WEBSOCKET ------------------------
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    db = SessionLocal()

    try:
        while True:
            user_msg = await websocket.receive_text()

            # Always show what user typed
            await manager.broadcast({"author": "User", "content": user_msg})
            log_chat(db=db, role="user", content=user_msg)

            # -----------------------------------------------------------
            # CHATROOM CREATE
            # -----------------------------------------------------------
            if user_msg.startswith("/chatroom"):
                parts = user_msg.split()[1:]
                selected_agents = []

                for part in parts:
                    for agent in AGENTS:
                        if part.lower() in agent["name"].lower():
                            selected_agents.append(agent)

                if not selected_agents:
                    await manager.broadcast({
                        "author": "System",
                        "content": "No agents found! Example: /chatroom scientist poet"
                    })
                    continue

                chatroom_id = str(uuid.uuid4())

                manager.chatroom = {
                    "id": chatroom_id,
                    "agents": selected_agents,
                    "last_message": "Start conversation",
                    "agent_index": 0
                }

                await manager.broadcast({
                    "author": "System",
                    "content": f"Chatroom created with: {', '.join(a['name'] for a in selected_agents)}"
                })

                await manager.broadcast({
                    "author": "System",
                    "content": "Chatroom started. Agents are waiting for you to speak..."
                })
                continue

            # -----------------------------------------------------------
            # CHATROOM MESSAGE HANDLING
            # -----------------------------------------------------------
            if manager.chatroom:
                chatroom = manager.chatroom
                chatroom_id = chatroom["id"]

                log_chatroom(
                    db=db,
                    role="user",
                    chatroom_id=chatroom_id,
                    message=user_msg
                )

                agent = chatroom["agents"][chatroom["agent_index"] % len(chatroom["agents"])]
                agent_name = agent["name"]
                agent_func = agent["func"]

                prompt = (
                    f"User said: {user_msg}\n"
                    f"Last message was: {chatroom['last_message']}\n\n"
                    f"You are {agent_name}. Reply naturally and keep the conversation moving."
                )

                reply = agent_func(prompt)

                log_chatroom(
                    db=db,
                    role="ai",
                    chatroom_id=chatroom_id,
                    message=reply,
                    ai_name=agent_name
                )

                await manager.broadcast({
                    "author": agent_name,
                    "content": reply
                })

                chatroom["last_message"] = reply
                chatroom["agent_index"] += 1
                continue

            # -----------------------------------------------------------
            # DIRECT AGENT CHAT
            # -----------------------------------------------------------
            lower = user_msg.lower()
            selected = None
            cleaned = None

            for a in AGENTS:
                key = a["name"].lower().replace("ai", "")
                if lower.startswith(key + " "):
                    selected = a
                    cleaned = user_msg[len(key) + 1:].strip()
                    break

            if selected:
                reply = selected["func"](cleaned)

                log_chat(
                    db=db,
                    role="ai",
                    content=reply,
                    ai_name=selected["name"]
                )

                await manager.broadcast({
                    "author": selected["name"],
                    "content": reply
                })
                continue

            # -----------------------------------------------------------
            # BASE FALLBACK
            # -----------------------------------------------------------
            base_ai = next(a for a in AGENTS if a["name"].lower() == "base")
            reply = base_ai["func"](user_msg)

            log_chat(
                db=db,
                role="ai",
                content=reply,
                ai_name="Base"
            )

            await manager.broadcast({
                "author": "BASE",
                "content": reply
            })

    except WebSocketDisconnect:
        manager.disconnect(websocket)
    finally:
        db.close()

