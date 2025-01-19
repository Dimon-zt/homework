from django.db import models

class PriceData(models.Model):
    exchanges_id = models.ForeignKey(
        'main.Exchanges',  # Указываем приложение и модель
        on_delete=models.CASCADE,
        related_name='arbitration_price_data'
    )
    pair_id = models.ForeignKey(
        'main.TradingPair',  # Указываем приложение и модель
        on_delete=models.CASCADE,
        related_name='arbitration_price_data'
    )
    price_ask = models.DecimalField(max_digits=20, decimal_places=8)
    price_bid = models.DecimalField(max_digits=20, decimal_places=8)
    volume_24h = models.DecimalField(max_digits=20, decimal_places=8)
    timestamp = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Price for {self.pair_id} at {self.timestamp}"
