
from django.shortcuts import render, redirect
from django.http import JsonResponse
from main.models import Exchanges, TradingPair
from .models import  PriceData
from .utils import start_price_updating

interval = 60  # Интервал обновления по умолчанию

# Арбитражная страница
def arbitration(request):
    global interval
    exchanges = Exchanges.objects.all()
    pairs = TradingPair.objects.values_list('pair', flat=True).distinct()
    prices = {}  # Здесь добавим логику загрузки цен
    return render(request, 'arbitration/arbitration.html', {
        'exchanges': exchanges,
        'pairs': pairs,
        'prices': prices,
        'interval': interval,
    })

# Добавление биржи
def add_exchange(request):
    if request.method == 'POST':
        name = request.POST['name']
        api_url = request.POST['api_url']
        Exchanges.objects.create(name=name, api_url=api_url)
        return redirect('arbitration')

# Установка интервала
def set_interval(request):
    if request.method == 'POST':
        global interval
        interval = int(request.POST['interval'])
        return redirect('arbitration')
