from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from rest_framework_simplejwt.views import TokenRefreshView

from .auth_views import AdminLoginView


urlpatterns = [

    # Django Admin
    path(
        "admin/",
        admin.site.urls,
    ),

    # Products
    path(
        "api/",
        include("products.urls"),
    ),

    # Documents / Historical Records
    path(
        "api/",
        include("documents.urls"),
    ),

    # Orders
    path(
        "api/orders/",
        include("orders.urls"),
    ),
    # billing
    path(
    "api/billing/",
    include("billing.urls"),
),
    
     path(
        "api/quotation/",
        include("quotation.urls")
    ),

    path(
    "api/production/",
    include("production.urls")
),
    
  path(
        "api/employees/",
        include("employees.urls")
    ),
    
    # path(
    #     "api/",
    #     include("service.urls")
    # ),

    # Admin Login
    path(
        "api/auth/login/",
        AdminLoginView.as_view(),
        name="admin-login",
    ),
    
     path(
        "api/customers/",
        include("customers.urls")
    ),

    # JWT Refresh
    path(
        "api/auth/refresh/",
        TokenRefreshView.as_view(),
        name="token-refresh",
    ),
]


urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT,
)