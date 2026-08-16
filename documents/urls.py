from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    DocumentViewSet,
    document_statistics,
)


router = DefaultRouter()

router.register(
    "documents",
    DocumentViewSet,
    basename="documents"
)


urlpatterns = [

    path(
        "documents/statistics/",
        document_statistics,
        name="document-statistics",
    ),

    path(
        "",
        include(router.urls)
    ),
]