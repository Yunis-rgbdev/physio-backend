"""
URL configuration for physioconnect project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from medical_record.views import MedicalFilesView
# from authenticationapp.views import LoginView, RegisterView


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('auth/register/', RegisterView.as_view(), name="register"),
    # path('auth/login/', LoginView.as_view(), name="login"),
    path("api/auth/", include("accounts.routing")),
    path("api/patients/", include("patients.routing")),
    path("api/operators/", include("operators.routing")),
    path('tasks/', include('tasks.router')),
    path('', include('chat_session.urls')),
    path('add-vas-score/', MedicalFilesView.as_view(), name='add-vas-score'),
    path('files/<str:mode>/<str:national_code>/', MedicalFilesView.as_view()),
]
