from django.contrib import admin
from django.urls import path, include

from mysite.core import views

from dashing.utils import router


urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('analysis/', views.analysis.as_view(), name='analysis'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path('check/', include(router.urls)),
]
