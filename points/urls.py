from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('kid_edit', views.kids_list, name='kids_list'),
    path('<int:kid_id>/edit/', views.kid_edit, name='kid_edit'),
    path('<int:kid_id>/delete/', views.kid_delete, name='kid_confirm_delete'),
    path('delete_multiple/', views.kid_delete_multiple, name='kid_delete_multiple'),
    path('kids/<int:kid_id>/deduct/<int:amount>', views.deduct_points_view, name='deduct_points'),
    path('register/', views.register_request, name='register'),
    path('kids_points/',views.kids_points_view, name='kids_points'),
    path('add_points/', views.add_points, name='add_points'),
    path('upload/', views.upload_file, name='upload_file'),
    path('login/', views.login, name='login'),
    path('admin_home/', views.admin_home, name='admin_home'),
    path('index', views.index, name='index'),
    path('store/', views.ProductListView.as_view(), name='store'),
    path('product/new/', views.ProductCreateView.as_view(), name='product_new'),
    path('product/<int:pk>/edit/', views.ProductUpdateView.as_view(), name='product_edit'),
    path('rate/edit/',views.RateUpdateView.as_view(), name='rate_edit'),
    path('checkout/', views.checkout, name='checkout'),
    path('kid/<int:kid_id>/', views.kid_account, name='kid_account'),
    path('add_to_cart/<int:kid_id>/<int:product_id>/', views.add_to_cart, name='add_to_cart'),



    




]

    

    
