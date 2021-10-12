from dotenv import load_dotenv
from os import getenv

load_dotenv()

config = {
    "MONGO_URI": getenv("MONGO_URI") or "mongodb://localhost:27017/",
    "MAX_FETCH_RETRY": getenv("MAX_FETCH_RETRY") and int(getenv("MAX_FETCH_RETRY")) or 5,
    "GITHUB_TOKEN": getenv("GITHUB_TOKEN")
}
