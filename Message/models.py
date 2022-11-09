from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    subject = models.CharField(max_length=50)
    message = models.TextField()
    creation_date = models.DateField(auto_now=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return self.subject