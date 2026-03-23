
from django.urls import path
from vineapp import views

urlpatterns = [
    path('', views.index, name='index'),
    path('contact/', views.contact, name='contact'),
    path('checkout/', views.checkout, name='checkout'),
    path('api/products/', views.products_api, name='products_api'),
    path('api/orders/', views.orders_api, name='orders_api'),
    path('api/feedback/', views.feedback_api, name='feedback_api'),
    path('api/feedback/clear/', views.clear_feedback_api, name='clear_feedback_api'),
]
