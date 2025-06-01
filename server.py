import socket
import threading
import os
import mimetypes
import json

HOST = '0.0.0.0'
PORT = 8080
STATIC_DIR = './static'

def get_mime_type(path):
    mimetype, _ = mimetypes.guess_type(path)
    return mimetype or 'application/octet-stream'

def handle_client(conn, addr):
    try:
        request = conn.recv(4096).decode()
        if not request:
            conn.close()
            return

        print(f"[INFO] İstek: {addr}")
        request_lines = request.split("\r\n")
        request_line = request_lines[0]
        method, path, _ = request_line.split()

        headers = {}
        i = 1
        while request_lines[i]:
            key, value = request_lines[i].split(": ", 1)
            headers[key.lower()] = value
            i += 1
        body = "\r\n".join(request_lines[i+1:])

        if path == '/':
            path = '/static/index.html'

        if method == 'GET':
            if path.startswith('/api/hello'):
                response_body = json.dumps({"message": "Hello, world!"}).encode()
                send_response(conn, '200 OK', 'application/json', response_body)
            elif path.startswith('/static/'):
                file_path = '.' + path
                if os.path.exists(file_path) and os.path.isfile(file_path):
                    with open(file_path, 'rb') as f:
                        body_bytes = f.read()
                        mime = get_mime_type(file_path)
                        send_response(conn, '200 OK', mime, body_bytes)
                else:
                    send_response(conn, '404 Not Found', 'text/plain', b'Dosya bulunamadi')
            else:
                send_response(conn, '404 Not Found', 'text/plain', b'Sayfa bulunamadi')

        elif method == 'POST' and path.startswith('/api/test-post'):
            try:
                data = json.loads(body)
                response_body = json.dumps({"echo": data}).encode()
                send_response(conn, '200 OK', 'application/json', response_body)
            except json.JSONDecodeError:
                send_response(conn, '400 Bad Request', 'text/plain', b'Gecersiz JSON verisi')

        else:
            send_response(conn, '405 Method Not Allowed', 'text/plain', b'Yalnizca GET ve belirli POST destekleniyor')

    except Exception as e:
        print(f"[HATA] {e}")
        send_response(conn, '500 Internal Server Error', 'text/plain', b'Sunucu hatasi')
    finally:
        conn.close()

def send_response(conn, status, content_type, body):
    response = f"HTTP/1.1 {status}\r\n"
    response += f"Content-Type: {content_type}\r\n"
    response += f"Content-Length: {len(body)}\r\n"
    response += "Connection: close\r\n"
    response += "\r\n"
    conn.sendall(response.encode() + body)

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen()
        print(f"[+] Sunucu baslatildi: http://localhost:{PORT}")

        while True:
            conn, addr = server.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()

if __name__ == '__main__':
    start_server()
