from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from .models import Exchanges
import csv
from .models import Currency
from binance.client import Client
from django.conf import settings
import requests
from django.http import HttpResponseRedirect
from django.urls import reverse


def load_currencies(request):
    if request.method == "POST":
        try:
            # Запрос к CoinGecko API для получения списка криптовалют
            url = "https://api.coingecko.com/api/v3/coins/list"
            response = requests.get(url)
            response.raise_for_status()  # Проверка на ошибки HTTP
            data = response.json()

            added_count = 0  # Количество добавленных записей
            for coin in data:
                symbol = coin['symbol'].upper()
                name = coin['name']

                # Создаем запись только если такой symbol еще нет в базе
                currency, created = Currency.objects.get_or_create(
                    symbol=symbol,
                    defaults={'name': name}
                )
                if created:
                    added_count += 1

            success_message = f"Успешно добавлено {added_count} новых криптовалют."
            return render(request, 'main/data.html', {'success_message': success_message})
        except Exception as e:
            error_message = f"Произошла ошибка: {str(e)}"
            return render(request, 'main/data.html', {'error_message': error_message})

    # Если GET-запрос, просто отобразить страницу
    return render(request, 'main/data.html')


def index(request):
    return render(request, 'main/index.html')

def data(request):
    return render(request, 'main/data.html')

def trade(request):
    return render(request, 'main/trade.html')

def exchanges(request):
    return render(request, 'main/exchanges.html')

def APIdata(request):
    return render(request, 'main/APIdata.html')


# Загрузка данных из файла
def upload_exchanges(request):
    if request.method == "POST" and request.FILES.get('file'):
        csv_file = request.FILES['file']
        if not csv_file.name.endswith('.csv'):
            messages.error(request, "Файл должен быть в формате CSV.")
            return redirect('/exchanges/')

        try:
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.reader(decoded_file)
            next(reader, None)  # Пропускаем заголовок, если есть

            new_entries = 0
            skipped_entries = 0

            for row in reader:
                if len(row) != 2:
                    # Пропустить строки с неправильным форматом
                    skipped_entries += 1
                    continue

                name, api_url = row[0].strip(), row[1].strip()

                # Проверяем дубликаты в базе
                if Exchanges.objects.filter(name=name).exists() or Exchanges.objects.filter(api_url=api_url).exists():
                    skipped_entries += 1
                    continue

                # Добавляем новую запись
                Exchanges.objects.create(name=name, api_url=api_url)
                new_entries += 1

            # Вывод результатов
            messages.success(
                request,
                f"Загрузка завершена: добавлено {new_entries}, пропущено {skipped_entries} записей."
            )
        except Exception as e:
            messages.error(request, f"Ошибка загрузки данных: {str(e)}")

        return redirect('/exchanges/')

    return HttpResponse("Неправильный запрос", status=400)


# Добавление биржи вручную
def add_exchange(request):
    if request.method == "POST":
        name = request.POST.get('name')
        api_url = request.POST.get('api_url')
        if name and api_url:
            Exchanges.objects.create(name=name, api_url=api_url)
            messages.success(request, "Биржа добавлена.")
        else:
            messages.error(request, "Все поля обязательны.")
        return redirect('/exchanges/')
    return HttpResponse("Неправильный запрос", status=400)


# Редактирование биржи
def edit_exchange(request, exchange_id):
    exchange = get_object_or_404(Exchanges, id=exchange_id)
    if request.method == "POST":
        exchange.name = request.POST.get('name')
        exchange.api_url = request.POST.get('api_url')
        exchange.save()
        messages.success(request, "Данные биржи обновлены.")
        return redirect('/exchanges/')
    return render(request, 'main/edit_exchange.html', {'exchange': exchange})


# Удаление биржи
def delete_exchange(request, exchange_id):
    exchange = get_object_or_404(Exchanges, id=exchange_id)
    if request.method == "POST":
        exchange.delete()
        messages.success(request, "Биржа удалена.")
        return redirect('/exchanges/')
    return HttpResponse("Неправильный запрос", status=400)


# Просмотр списка бирж
def list_exchanges(request):
    exchanges = Exchanges.objects.all()
    return render(request, 'main/exchanges.html', {'exchanges': exchanges})

