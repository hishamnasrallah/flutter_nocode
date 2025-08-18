from django.urls import path
from . import views

app_name = 'mock_payment'

urlpatterns = [
    path('payment-intent/', views.mock_create_payment_intent, name='payment_intent'),
    path('confirm/', views.mock_confirm_payment, name='confirm_payment'),
    path('webhook/', views.mock_stripe_webhook, name='webhook'),
    path('payment-methods/', views.mock_payment_methods, name='payment_methods'),
    path('payment-methods/add/', views.mock_add_payment_method, name='add_payment_method'),
]