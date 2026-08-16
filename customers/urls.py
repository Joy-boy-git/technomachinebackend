from django.urls import path

from .views import (
    CustomerRegisterView,
    CustomerLoginView,
    CustomerProfileView,
    CustomerMeView,
)


urlpatterns = [

    # --------------------------------------------------------
    # CUSTOMER AUTHENTICATION
    # --------------------------------------------------------

    path(
        "register/",
        CustomerRegisterView.as_view(),
        name="customer-register"
    ),

    path(
        "login/",
        CustomerLoginView.as_view(),
        name="customer-login"
    ),

    # --------------------------------------------------------
    # CUSTOMER PROFILE
    # --------------------------------------------------------

    path(
        "profile/",
        CustomerProfileView.as_view(),
        name="customer-profile"
    ),

    path(
        "me/",
        CustomerMeView.as_view(),
        name="customer-me"
    ),
]