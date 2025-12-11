from django.urls import path

from .views import CheckoutView, WebhookView, PaymentStatusView

app_name = "payments"

urlpatterns = [
    path("checkout/", CheckoutView.as_view(), name="checkout"),
    path("webhook/", WebhookView.as_view(), name="webhook"),
    path("status/", PaymentStatusView.as_view(), name="status"),
]
