import socket
import threading

all_files = {}

def add_file(ip, file):
    if ip not in all_files:
        all_files[ip] = []
    all_files[ip].append(file)

def delete_file(ip, filename):
    if ip in all_files:
        all_files[ip] = [f for f in all_files[ip] if f['filename'] != filename]

def user_leave(ip):
    if ip in all_files:
        del all_files[ip]

def search_files(pattern):
    result = []
    print(all_files)
    for ip, files in all_files.items():
        for f in files:
            if pattern in f["filename"]:
                result.append(f"FILE {f['filename']} {ip} {f['size']}")
    return result

def handle_client(conn, addr):
    ip = None
    with conn:
        while True:
            try:
                data = conn.recv(1024).decode().strip()
                if not data:
                    break

                print(f"Received: {data}")
                tokens = data.split()

                if tokens[0] == "JOIN":
                    ip = tokens[1]
                    conn.sendall(b"CONFIRMJOIN\n")

                elif tokens[0] == "CREATEFILE":
                    filename = tokens[1]
                    size = int(tokens[2])
                    add_file(ip, {"filename": filename, "size": size})
                    conn.sendall(f"CONFIRMCREATEFILE {filename}\n".encode())

                elif tokens[0] == "DELETEFILE":
                    filename = tokens[1]
                    before = len(all_files.get(ip, []))
                    delete_file(ip, filename)
                    after = len(all_files.get(ip, []))
                    if before > after:
                        conn.sendall(f"CONFIRMDELETEFILE {filename}\n".encode())
                    else:
                        conn.sendall(f"ERRORDELETEFILE {filename} - not found\n".encode())


                elif tokens[0] == "SEARCH":
                    pattern = tokens[1]
                    result = search_files(pattern)
                    for line in result:
                        conn.sendall((line + "\n").encode())

                elif tokens[0] == "LEAVE":
                    user_leave(ip)
                    conn.sendall(b"CONFIRMLEAVE\n")
                    break
            except Exception as e:
                print("Erro:", e)
                break

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('0.0.0.0', 1234))
        s.listen()
        print("Servidor esperando conexões na porta 1234...")
        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_client, args=(conn, addr)).start()

if __name__ == "__main__":
    start_server()
