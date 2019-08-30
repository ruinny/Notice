"""Notice URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path, re_path
from webpack import views
from django.conf.urls import url, include

urlpatterns = {
    path('admin/', admin.site.urls),
    path('', views.index),
    path('show/', views.show),
    #path('showall/',views.showall),
    path('lists/',views.lists),
    #path('singup/', views.signup),
    path('logout/', views.logout),
    re_path(r'^dep-', views.dep_index),
    re_path(r'^login', views.LoginView, name='login'),
    re_path(r'^send_message$', views.send_message, name='send_message'),
    re_path(r'^pc-geetest/register', views.pcgetcaptcha, name='pcgetcaptcha'),

}

handler400 = views.bad_request
handler403 = views.permission_denied
handler404 = views.page_not_found
handler500 = views.error