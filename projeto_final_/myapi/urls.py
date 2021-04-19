#myapi/urls.py


from django.urls import include, path
from rest_framework import routers
from . import views 
from knox import views as knox_views

# router = routers.DefaultRouter()
# router.register(r'testes', views.registerViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.


urlpatterns = [
    #path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    #path('register/', views.registration_view, name="register")
    path('api/register/', views.RegisterAPI.as_view(), name='register'),
    path('api/login/', views.LoginAPI.as_view(), name='login'),
    path('api/logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('api/logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
    path('api/getAuthToken/', views.getAuthToken.as_view(), name="getAuthToken"),
    path('api/agreementRequestAccept/', views.agreementRequestAcceptAPI.as_view(), name="agreementRequestAccept"),
    path('api/agreementRequest/', views.agreementRequestAPI.as_view(), name="agreement_request"),
    path('api/imageTest/', views.imageTest.as_view(), name="imageTest"),
    path('api/User/<int:pk>/', views.UserAPI.as_view(), name="User"),
]