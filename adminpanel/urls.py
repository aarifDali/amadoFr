from django.urls import path
from . import views


urlpatterns = [
    path('', views.redirect_to_login),
    path('login', views.manager_login, name="manager_login"),
    path('logout', views.manager_logout, name='manager_logout'),
    path('dashboard', views.manager_dashboard, name='manager_dashboard'),
    path('manage_user', views.manage_user, name="manage_user"),
    path('manage_product/', views.manage_product, name='manage_product'),
    path('manage_category/', views.manage_category, name='manage_category'),


    path('ban_user/<int:user_id>/', views.ban_user, name='ban_user'),
    path('unban_user/<int:user_id>/', views.unban_user, name='unban_user'),

    path('add_product/', views.add_product, name='add_product'),  
    path('edit_product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('delete_product/<int:product_id>/', views.delete_product, name='delete_product'),

    path('add_category/', views.add_category, name='add_category'),
    path('delete_category/<int:category_id>/', views.delete_category, name="delete_category"),
]