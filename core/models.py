from django.db import models

class InteractionRecord(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    stored_value = models.TextField()

