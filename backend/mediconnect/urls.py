from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from core.views import PatientViewSet, RendezVousViewSet, MédecinViewSet
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register(r'patients', PatientViewSet)
router.register(r'appointments', RendezVousViewSet)
router.register(r'doctors', MédecinViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/orthanc/', include('orthanc_integration.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)