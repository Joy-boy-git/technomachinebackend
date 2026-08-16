from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import QuotationViewSet


# ============================================================
# ROUTER
# ============================================================

router = DefaultRouter()

router.register(
    r"quotations",
    QuotationViewSet,
    basename="quotation"
)


# ============================================================
# URLS
# ============================================================

urlpatterns = [
    path(
        "",
        include(router.urls)
    ),
]