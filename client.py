import socket
import os
import threading

SERVER_IP = '127.0.0.1'
PUBLIC_FOLDER = './public'
DOWNLOAD_FOLDER = './downloads'

os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

def connect_to_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((SERVER_IP, 1234))
    my_ip = get_local_ip()
    s.sendall(f"JOIN {my_ip}\n".encode())
    print(s.recv(1024).decode().strip())
    for file in os.listdir(PUBLIC_FOLDER):
        path = os.path.join(PUBLIC_FOLDER, file)
        if os.path.isfile(path):
            size = os.path.getsize(path)
            s.sendall(f"CREATEFILE {file} {size}\n".encode())
            print(s.recv(1024).decode().strip())
    return s

def handle_file_requests():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('0.0.0.0', 1235))
        s.listen()
        while True:
            conn, addr = s.accept()
            threading.Thread(target=send_file, args=(conn,)).start()

def send_file(conn):
    with conn:
        request = conn.recv(1024).decode().strip()
        print("Request:", request)
        tokens = request.split()
        if tokens[0] == "GET":
            filename = tokens[1]
            offset_range = tokens[2].split("-")
            offset_start = int(offset_range[0])
            offset_end = None
            if len(offset_range) > 1 and offset_range[1].isdigit():
                offset_end = int(offset_range[1])
            filepath = os.path.join(PUBLIC_FOLDER, filename)
            if os.path.isfile(filepath):
                with open(filepath, 'rb') as f:
                    f.seek(offset_start)
                    if offset_end is not None:
                        data = f.read(offset_end - offset_start)
                    else:
                        data = f.read()
                    conn.sendall(data)
            else:
                conn.sendall(b"")  # envia vazio se o arquivo não for encontrado

def search_file_on_server(s, pattern):
    s.settimeout(0.5)
    s.sendall(f"SEARCH {pattern}\n".encode())
    found = False
    try:
        while True:
            response = s.recv(1024).decode()
            if not response:
                break
            lines = response.strip().split("\n")
            for line in lines:
                if line.strip():
                    print(line.strip())
                    found = True
    except socket.timeout:
        pass
    finally:
        s.settimeout(None)
    if not found:
        print("Nenhum arquivo encontrado.")

def download_file(ip, filename, offset_start=0, offset_end=None):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((ip, 1235))
            offset = f"{offset_start}-"
            if offset_end is not None:
                offset += f"{offset_end}"
            s.sendall(f"GET {filename} {offset}\n".encode())
            output_path = os.path.join(DOWNLOAD_FOLDER, filename)
            with open(output_path, 'wb') as f:
                while True:
                    data = s.recv(4096)
                    if not data:
                        break
                    f.write(data)
        print(f"Arquivo '{filename}' baixado com sucesso em '{DOWNLOAD_FOLDER}/'.")
    except Exception as e:
        print(f"Erro ao baixar o arquivo: {e}")

if __name__ == "__main__":
    threading.Thread(target=handle_file_requests, daemon=True).start()
    client_socket = connect_to_server()

    while True:
        cmd = input("Comando (SEARCH/DELETE/LEAVE/DOWNLOAD): ").strip()
        if cmd.startswith("SEARCH"):
            parts = cmd.split(maxsplit=1)
            if len(parts) == 2:
                search_file_on_server(client_socket, parts[1])
            else:
                print("Uso correto: SEARCH <termo>")
        elif cmd.startswith("DELETE"):
            parts = cmd.split(maxsplit=1)
            if len(parts) == 2:
                client_socket.sendall(f"DELETEFILE {parts[1]}\n".encode())
                print(client_socket.recv(1024).decode().strip())
            else:
                print("Uso correto: DELETE <nome-do-arquivo>")
        elif cmd == "LEAVE":
            client_socket.sendall(b"LEAVE\n")
            print(client_socket.recv(1024).decode().strip())
            break
        elif cmd.startswith("DOWNLOAD"):
            parts = cmd.split()
            if len(parts) >= 3:
                ip = parts[1]
                filename = parts[2]
                offset_start = int(parts[3]) if len(parts) >= 4 else 0
                offset_end = int(parts[4]) if len(parts) >= 5 else None
                download_file(ip, filename, offset_start, offset_end)
            else:
                print("Uso correto: DOWNLOAD <ip> <arquivo> [inicio] [fim]")
        else:
            print("Comando não reconhecido. Use: SEARCH, DELETE, DOWNLOAD ou LEAVE.")
