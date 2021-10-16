from dotenv import load_dotenv
from os import getenv

load_dotenv()

config = {
    "MONGO_URI": getenv("MONGO_URI") or "mongodb://localhost:27017/",
    "GITHUB_TOKEN": getenv("GITHUB_TOKEN")
}
