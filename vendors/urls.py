from django.urls import path
from . import views
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Vendors_APIs",
        default_version='v1',
        description="Get the performance of all vendors",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('vendors/', views.VendorListCreateAPIView.as_view()),
    path('vendors/<int:pk>/', views.VendorDetailAPIView.as_view()),
    path('purchase_orders/', views.PurchaseOrderListCreateAPIView.as_view()),
    path('purchase_orders/<str:po_id>/', views.PurchaseOrderDetailAPIView.as_view()),
    path('vendors/<int:vendor_id>/performance/', views.VendorPerformanceAPIView.as_view()),
    path('signup/', views.UserSignup.as_view(), name='signup'),
    path('login/', views.UserLogin.as_view(), name='login'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
