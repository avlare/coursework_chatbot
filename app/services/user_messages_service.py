from app.repositories.user_messages_repository import UserMessagesRepository


class UserMessagesService:
    def __init__(self):
        self.user_messages_repository = UserMessagesRepository()

    def find_user_by_id(self, user_id):
        return self.user_messages_repository.find_user_by_id(user_id)

    def create_user(self, user_id):
        return self.user_messages_repository.create_user(user_id)

    def update_messages(self, user_id, new_messages):
        return self.user_messages_repository.update_messages(user_id, new_messages)

    def get_all_messages(self, user_id):
        return self.user_messages_repository.get_all_messages(user_id)
