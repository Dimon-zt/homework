from django.db import models

class Exchanges(models.Model):
    name = models.CharField(max_length=100)
    api_url = models.TextField()


    def __str__(self):
        return self.name

class Currency(models.Model):
    symbol = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)


    def __str__(self):
        return self.name

class Users(models.Model):
    username = models.CharField(max_length=100)
    password = models.TextField()
    api_key = models.TextField()
    api_secret = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username

class TradingPair(models.Model):
    exchanges_id = models.ForeignKey('Exchanges', on_delete=models.CASCADE, related_name='exchange_TradingPair')
    base_currency_id = models.ForeignKey('Currency', on_delete=models.CASCADE, related_name='base_currency_pairs')
    quote_currency_id = models.ForeignKey('Currency', on_delete=models.CASCADE, related_name='quote_currency_pairs')
    pair = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.pair} on {self.exchanges_id.name}"


class PriceData(models.Model):
    exchanges_id = models.ForeignKey('Exchanges', on_delete=models.CASCADE, related_name='exchange_PriceData')
    pair_id = models.ForeignKey(TradingPair, on_delete=models.CASCADE, related_name='price_data')
    price_ask = models.DecimalField(max_digits=20, decimal_places=8)
    price_bid = models.DecimalField(max_digits=20, decimal_places=8)
    volume_24h = models.DecimalField(max_digits=20, decimal_places=8)
    timestamp = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Price for {self.pair_id.ticker} at {self.timestamp}"

class ApiData(models.Model):
    exchanges_id = models.ForeignKey('Exchanges', on_delete=models.CASCADE, related_name='exchange_ApiData')
    name = models.CharField(max_length=100)
    api_url = models.TextField()


    def __str__(self):
        return self.name
