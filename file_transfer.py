import threading
import socket
import pickle


class fileClientThread(threading.Thread):
    def __init__(self, ip, port, conn, file_requested):
        super(fileServer, self).__init__() #CAll Thread.__init__()
        self.terminate_flag = threading.Event()
        self.ip = ip
        self.port = port
        self.sock = sock
        self.file_requested = file_requested

    def SendFile(self, filehash, buffer_size):
        content = json.load("resources.json")
        if filehash not in content:
            print("File requested and connected but we do not have.")
            return
        else:
            file = content[filehash]

        f = open(file, 'rb')
        data = f.read()
        serialized_data = pickle.dumps(data)
        conn.sendall(struct.pack('>I', len(serialized_data)))
        conn.send(file.encode('utf-8'))
        conn.sendall(serialized_data)

    def stop(self):
        self.terminate_flag.set()

    def run(self):
        while not self.terminate_flag.is_set():
            SendFile(file_requested)

class fileServer(threading.Thread):
    def __init__(self, parent, PORT):
        self.terminate_flag = threading.Event()
        super(fileServer, self).__init__() #CAll Thread.__init__()

        self.parent = parent
        self.port = PORT
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(("", self.port))

        self.threads = []

    def stop(self):
        self.terminate_flag.set()

    def run(self):
        while not self.terminate_flag.is_set():  # Check whether the thread needs to be closed
            self.sock.listen(5)
            (conn, (ip, port)) = self.sock.accept()

            self.parent.debug_print('File Server conection from: ', (ip, port))

            file_requested = str(conn.recv(4096).decode('utf-8')) #recieve file hash

            newthread = fileClientThread(ip, port, conn, file_requested)
            newthread.start()

            self.threads.append(newthread)

        for t in self.threads:
            t.join()
            self.parent.debug_print("File Server stopped")

class FileDownloader(threading.Thread):
    def __init__(self, arg):
        super(FileDownloader, self).__init__()
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect((TCP_IP, TCP_PORT))

    def run(self):
        self.data_size = struct.unpack('>I', conn.recv(4))[0]
        filename = str(conn.recv(4096).decode('utf-8')) #recieve file name
        received_payload = b""
        reamining_payload_size = data_size
        while reamining_payload_size != 0:
            received_payload += self.conn.recv(reamining_payload_size)
            reamining_payload_size = self.data_size - len(received_payload)
        data = pickle.loads(received_payload)

        self.conn.close()

        f = open(filename, "w")
        f.write(data)
        f.close()