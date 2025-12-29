import argparse
import asyncio
import json
import logging
import threading
from typing import Any, Dict, Set

from flask import Flask, jsonify, request
from flask_cors import CORS
import websockets

from gcode_parser import GCodeParser


LOGGER = logging.getLogger(__name__)
CONNECTED: Set[websockets.WebSocketServerProtocol] = set()
CONNECTED_LOCK = asyncio.Lock()
EVENT_LOOP: asyncio.AbstractEventLoop | None = None
STATE = {"status": "stopped"}


def parse_gcode_payload(gcode_text: str) -> Dict[str, Any]:
    parser = GCodeParser()
    return parser.parse_to_json(gcode_text)


async def register_client(websocket: websockets.WebSocketServerProtocol) -> None:
    async with CONNECTED_LOCK:
        CONNECTED.add(websocket)
    LOGGER.info("WebSocket connected: %s", websocket.remote_address)


async def unregister_client(websocket: websockets.WebSocketServerProtocol) -> None:
    async with CONNECTED_LOCK:
        CONNECTED.discard(websocket)
    LOGGER.info("WebSocket disconnected: %s", websocket.remote_address)


async def broadcast(payload: Dict[str, Any]) -> None:
    message = json.dumps(payload)
    async with CONNECTED_LOCK:
        clients = list(CONNECTED)
    if not clients:
        return
    send_tasks = [client.send(message) for client in clients]
    results = await asyncio.gather(*send_tasks, return_exceptions=True)
    for client, result in zip(clients, results):
        if isinstance(result, Exception):
            LOGGER.warning("Failed to send to %s: %s", client.remote_address, result)


async def handle_message(message: str) -> None:
    try:
        payload = json.loads(message)
    except json.JSONDecodeError:
        LOGGER.warning("Received non-JSON message: %s", message)
        return

    message_type = payload.get("type")
    data = payload.get("data")
    if message_type == "command" and isinstance(data, dict):
        action = data.get("action")
        if action in {"play", "pause", "stop"}:
            STATE["status"] = action
            await broadcast({"type": "status", "data": action})
    elif message_type == "status" and isinstance(data, str):
        STATE["status"] = data
        await broadcast({"type": "status", "data": data})


async def websocket_handler(websocket: websockets.WebSocketServerProtocol, path: str) -> None:
    if path != "/ws":
        await websocket.close(code=1008, reason="Unsupported WebSocket endpoint")
        return
    await register_client(websocket)
    try:
        await websocket.send(json.dumps({"type": "status", "data": STATE["status"]}))
        async for message in websocket:
            await handle_message(message)
    except websockets.ConnectionClosedError as exc:
        LOGGER.info("WebSocket closed: %s", exc)
    finally:
        await unregister_client(websocket)


def create_app() -> Flask:
    app = Flask(__name__)
    CORS(app)

    @app.post("/upload")
    def upload_gcode():
        if "file" not in request.files:
            return jsonify({"error": "Missing file upload."}), 400
        file_storage = request.files["file"]
        gcode_text = file_storage.read().decode("utf-8", errors="ignore")
        result = parse_gcode_payload(gcode_text)
        message = {"type": "gcode_data", "data": result}
        if EVENT_LOOP is not None:
            asyncio.run_coroutine_threadsafe(broadcast(message), EVENT_LOOP)
        return jsonify({"ok": True, "commands": result["metadata"]["total_commands"]})

    @app.post("/api/send-gcode")
    def send_gcode():
        payload = request.get_json(silent=True) or {}
        gcode_text = payload.get("gcode")
        if not gcode_text:
            return jsonify({"error": "Missing 'gcode' payload."}), 400

        result = parse_gcode_payload(gcode_text)
        message = {"type": "gcode_data", "data": result}
        if EVENT_LOOP is not None:
            asyncio.run_coroutine_threadsafe(broadcast(message), EVENT_LOOP)
        return jsonify({"ok": True, "commands": result["metadata"]["total_commands"]})

    return app


def run_flask(app: Flask, host: str, port: int) -> None:
    LOGGER.info("Starting Flask on %s:%s", host, port)
    app.run(host=host, port=port, debug=False, use_reloader=False)


def main() -> None:
    parser = argparse.ArgumentParser(description="Vizualizer HTTP/WebSocket bridge.")
    parser.add_argument("--ws-host", default="0.0.0.0", help="WebSocket host")
    parser.add_argument("--ws-port", type=int, default=8765, help="WebSocket port")
    parser.add_argument("--http-host", default="0.0.0.0", help="HTTP host for Flask")
    parser.add_argument("--http-port", type=int, default=5000, help="HTTP port for Flask")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    app = create_app()
    flask_thread = threading.Thread(
        target=run_flask,
        args=(app, args.http_host, args.http_port),
        daemon=True,
    )
    flask_thread.start()

    loop = asyncio.new_event_loop()
    global EVENT_LOOP
    EVENT_LOOP = loop
    asyncio.set_event_loop(loop)
    server = websockets.serve(
        websocket_handler,
        args.ws_host,
        args.ws_port,
        ping_interval=20,
        ping_timeout=20,
    )
    loop.run_until_complete(server)
    LOGGER.info("WebSocket server listening on %s:%s", args.ws_host, args.ws_port)
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        LOGGER.info("Shutting down...")
    finally:
        loop.stop()
        loop.close()


if __name__ == "__main__":
    main()
