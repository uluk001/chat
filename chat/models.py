from django.db import models
from users.models import CustomUser

class Chat(models.Model):
    buyer = models.ForeignKey(CustomUser, related_name='buyer_chats', on_delete=models.CASCADE)
    seller = models.ForeignKey(CustomUser, related_name='seller_chats', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.buyer} | {self.seller}"


class Message(models.Model):
    chat = models.ForeignKey(Chat, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    media_file = models.FileField(upload_to='chat_media/', null=True, blank=True)  # Путь к медиафайлам
    is_deleted = models.BooleanField(default=False)  # Флаг для мягкого удаления
    edited_at = models.DateTimeField(null=True, blank=True)  # Время последнего редактирования
    created_at = models.DateTimeField(auto_now_add=True)  # Время создания сообщения

    def __str__(self):
        last_message = self.content[:20]
        return f"{last_message}... | {self.sender}"
