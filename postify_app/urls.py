from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from core import views as core_views # ← idha seru

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')), 
    
    # LOGIN/LOGOUT/SIGNUP - IDHU ILANA 500 VARUM
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('signup/', core_views.signup, name='signup'), # Un signup view name enna nu podu
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)