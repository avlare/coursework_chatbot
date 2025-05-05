from app import db

PROMPT = {
            "role": "system",
            "content": (
                    "You are a warm and empathetic psychological support assistant. "
                    "Treat user like psychotherapist treats the client. "
                    "Respond concisely but meaningfully. Avoid repetition and excessive details. "
                    "Acknowledge the user's emotions, validate their feelings, and encourage self-reflection. "
                    "Ask clarifying questions only when necessary. "
                    "Keep your tone natural and heartfelt, avoiding robotic phrasing. "
                    "Offer emotional support rather than advice. "
                    "If relevant, you may briefly suggest books or films on the topic. "
                    "In case of serious issues (loss, trauma, abuse, suicidal thoughts), "
                    "respond with extra care and emphasize "
                    "the importance of seeking professional help."
            )
        }


class UserMessagesRepository:
    def __init__(self):
        self.db = db

    def find_user_by_id(self, user_id):
        return self.db.user_messages.find_one({"_id": user_id})

    def get_all_messages(self, user_id):
        user = self.find_user_by_id(user_id)
        messages = user["messages"]
        if len(messages) > 16:
            return [messages[0]] + messages[-15:]
        return messages

    def create_user(self, user_id):
        user = {"_id": user_id, "messages": [PROMPT]}
        self.db.user_messages.insert_one(user)
        return user

    def update_messages(self, user_id, new_messages):
        self.db.user_messages.update_one(
            {"_id": user_id},
            {"$push": {"messages": new_messages}}
        )
        return None

