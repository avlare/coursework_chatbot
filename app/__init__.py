from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from tokens import MONGODB_TOKEN

uri = (f"mongodb+srv://megan15chatbot:{MONGODB_TOKEN}@cluster0.03aah.mongodb.net/"
       f"?retryWrites=true&w=majority&appName=Cluster0")

client = MongoClient(uri, server_api=ServerApi('1'))

db = client['Chatbot']
user_messages = db['user_messages']

try:
    client.admin.command('ping')
    print("Connected to MongoDB!")
except Exception as e:
    print(e)