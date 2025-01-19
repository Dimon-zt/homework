from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('data/', views.data, name='data'),
    path('trade/', views.trade, name='trade'),
      #  path('exchanges/', views.exchanges, name='exchanges'),
    path('APIdata/', views.APIdata, name='APIdata'),
    path('exchanges/', views.list_exchanges, name='list_exchanges'),
    path('exchanges/upload/', views.upload_exchanges, name='upload_exchanges'),
    path('exchanges/add/', views.add_exchange, name='add_exchange'),
    path('exchanges/edit/<int:exchange_id>/', views.edit_exchange, name='edit_exchange'),
    path('exchanges/delete/<int:exchange_id>/', views.delete_exchange, name='delete_exchange'),
    #path('load-cryptos/', views.load_currencies, name='load_currencies'),
    path('load_currencies/', views.load_currencies, name='load_cryptos'),
]
