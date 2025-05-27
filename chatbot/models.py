from django.db import models

class ChatLog(models.Model):
    """Model to store chat interactions"""
    user_message = models.TextField()
    bot_response = models.TextField()
    intent = models.CharField(max_length=50)
    product_id = models.IntegerField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Chat: {self.user_message[:30]}... → {self.bot_response[:30]}..."
    
    class Meta:
        ordering = ['-timestamp']
