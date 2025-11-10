from rest_framework.routers import DefaultRouter
from .views import SiteSettingsViewSet

router = DefaultRouter()
router.register('site-settings', SiteSettingsViewSet, basename='site-settings')

urlpatterns = router.urls

