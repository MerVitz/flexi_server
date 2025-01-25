from django.urls import path

from .views import LoginView, LogoutView, UserCreate
from .mpesa_views import stk_push_payment, mpesa_webhook

urlpatterns = [
    path('register/', UserCreate.as_view(), name='user-create'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path("stkpush_payment/", stk_push_payment, name="stkpush_payment"),
    path("mpesa_webhook/", mpesa_webhook, name="mpesa_webhook"),
]
