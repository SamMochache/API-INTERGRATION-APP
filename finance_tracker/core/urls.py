from django.urls import path
from . import views

urlpatterns = [
    path('plaid/link-token/', views.get_link_token, name='get_link_token'),
    path('add_transaction/', views.add_transaction, name='add_transaction'),
    path('set_budget/', views.set_budget, name='set_budget'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('', views.index, name='index'),
]
