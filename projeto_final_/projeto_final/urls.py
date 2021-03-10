"""projeto_final URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import include, path
import django.contrib.auth.views as d_auth
import mainApp

reset_path = 'mainApp/pw_reset.html'
reset_success = '/accounts/login/'
email = 'mainApp/pwd_reset_email.html'
pw_reset = d_auth.PasswordResetView.as_view(template_name = reset_path, success_url = reset_success, email_template_name= email)

email_path = 'mainApp/pwd_reset_confirm.html'
confirm_success = '/accounts/login/'
pw_confirm = d_auth.PasswordResetConfirmView.as_view(template_name = email_path, success_url = confirm_success)

urlpatterns = [
    path('mainApp/', include('mainApp.urls')),
    path('admin/', admin.site.urls),
    path('verification/', include('verify_email.urls')),
    path('accounts/login/', mainApp.views.login_view, name='login_view'),
    path('accounts/logout/', mainApp.views.logout_view, name='logout_view'),
    path('accounts/register/', mainApp.views.register_view, name='register_view'),
    path('accounts/password_reset/', pw_reset , name='password_reset'),
    path('accounts/reset/<uidb64>/<token>/', pw_confirm , name='pwd_reset_confirm'),
    #path('accounts/password_reset/done/', )
    path('accounts/', include('django.contrib.auth.urls')),
]

