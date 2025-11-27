# operators/routing.py
from django.urls import path
from .views import OperatorServiceView

urlpatterns = [
    path("<str:mode>/<str:national_code>/", OperatorServiceView.as_view(), name="operator_service"),
    # path("search/", views.search_operator, name="operator_detail"),
]