import os
import dotenv

from server.server import Server

dotenv.load_dotenv()

HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", 5000))
BUFF_SIZE = int(os.getenv("BUFF_SIZE", 512))


if __name__ == "__main__":
    Server(HOST, PORT, BUFF_SIZE)
