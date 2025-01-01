from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('checkout/<int:product_id>/', views.checkout, name='checkout'),
]



