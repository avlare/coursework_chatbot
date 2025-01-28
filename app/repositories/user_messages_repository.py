from app import db


class UserMessagesRepository:
    def __init__(self):
        self.db = db

    def find_user_by_id(self, user_id):
        return self.db.user_messages.find_one({"_id": user_id})

    def get_all_messages(self, user_id):
        user = self.find_user_by_id(user_id)
        return user["messages"]

    def create_user(self, user_id):
        user = {"_id": user_id, "messages": [
            {
                "role": "system",
                "content": "You are a compassionate and conversational psychological support assistant."
                           "If the user greets you or asks a simple question (e.g., 'Hi', 'How are you?', 'Hello'), "
                           "respond briefly with a greeting and offer to help."
                           "Don't use idioms. "
                           "Respond in a natural, heartfelt tone, avoiding robotic responses. "
                           "Provide support and understanding."
                           "be thankful, acknowledge, validate and name possible or explicitly expressed user's emotions. "
                           "Show that you truly care about user and the issue. "
                           "Treat user like psychotherapist treats the client. "
                           "Ask clarifying questions to get more details about user's situation or issue. "
                           "Answer with respect to every user's text. Your priority is to provide emotional support. "
                           "Underline that user already has his/her own inner strength and capable of going through "
                           "the situation the user described. "
                           "Do not give any pieces of advice; alternatively, provide recommendations on resilience. "
                           "Optionally, suggest books, films that user might find helpful on the topic. "
                           "In case of a serious issue such as death, loss, trauma, rape, physical abuse, suicide, "
                           "severe psychiatric conditions, and other criminal issues respond with extra care, acknowledgement, "
                           "and underline the vitality of seeing the health care specialist."
            }
        ]}
        self.db.user_messages.insert_one(user)
        return user

    def update_messages(self, user_id, new_messages):
        self.db.user_messages.update_one(
            {"_id": user_id},
            {"$push": {"messages": new_messages}}
        )
        return None
