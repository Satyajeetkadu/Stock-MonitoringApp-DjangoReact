# watchlists/models.py
from django.db import models

class Watchlist(models.Model):
    symbol = models.CharField(max_length=10)
    stock_data = models.JSONField(null=True, blank=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.symbol