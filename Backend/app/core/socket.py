# app/core/socket.py

import socketio

# Create the Socket.IO server first
sio = socketio.AsyncServer(
    cors_allowed_origins=["http://localhost:3000"],
    async_mode="asgi"
)

# Create the ASGI app
sio_app = socketio.ASGIApp(sio)

# Store online users { user_id: socket_id }
user_socket_map = {}

@sio.event
async def connect(sid, environ):
    query_params = environ.get("QUERY_STRING", "")
    user_id = None
    if "userId=" in query_params:
        user_id = query_params.split("userId=")[1].split("&")[0]

    if user_id:
        user_socket_map[user_id] = sid

    await sio.emit("getOnlineUsers", list(user_socket_map.keys()))


@sio.event
async def disconnect(sid):
    user_id_to_remove = None
    for uid, socket_id in list(user_socket_map.items()):
        if socket_id == sid:
            user_id_to_remove = uid
            break

    if user_id_to_remove:
        del user_socket_map[user_id_to_remove]

    await sio.emit("getOnlineUsers", list(user_socket_map.keys()))


def get_receiver_socket_id(user_id: str):
    return user_socket_map.get(user_id)
