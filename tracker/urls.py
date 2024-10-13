from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='base'),
    path('delete-transaction/<int:id>/', views.delete_transaction, name="delete_transaction"),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
]
