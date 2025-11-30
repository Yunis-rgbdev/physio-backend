# operators/routing.py
from django.urls import path
from .views import OperatorServiceView

operator_view = OperatorServiceView.as_view({
    "get": "search",
    "post": "search",
})

active_sessions_view = OperatorServiceView.as_view({
    "get": "active_sessions",
    "post": "active_sessions",
})

urlpatterns = [
    path("<str:national_code>/search/", operator_view),
    path("<str:national_code>/active-sessions/", active_sessions_view),
]