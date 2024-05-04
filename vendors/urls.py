from django.urls import path
from . import views

urlpatterns = [
    path('vendors/', views.VendorListCreateAPIView.as_view()),
    path('vendors/<int:pk>/', views.VendorDetailAPIView.as_view()),
    path('purchase_orders/', views.PurchaseOrderListCreateAPIView.as_view()),
    path('purchase_orders/<str:po_id>/', views.PurchaseOrderDetailAPIView.as_view()),
    path('vendors/<int:vendor_id>/performance/', views.VendorPerformanceAPIView.as_view()),
    path('signup/', views.UserSignup.as_view(), name='signup'),
    path('login/', views.UserLogin.as_view(), name='login'),
]
