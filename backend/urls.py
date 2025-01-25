from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from backend_app import views

# Register viewsets with the router
router = DefaultRouter()
router.register(r'reviews', views.ReviewViewSet)
router.register(r'comments', views.CommentViewSet)
router.register(r'maintenances', views.MaintenanceViewSet)
router.register(r'notifications', views.NotificationViewSet)
router.register(r'payments', views.PaymentViewSet)
router.register(r'bookings', views.BookingViewSet)
router.register(r'equipment', views.EquipmentViewSet)
router.register(r'users', views.CustomUserViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/mpesa/', include('backend_app.urls')),
    path('api/notifications/<int:pk>/confirm/', views.NotificationConfirmView.as_view(), name='notification-confirm'),
    path('api/check-admin-privileges/', views.CheckAdminPriviledgesView.as_view(), name='check-admin-privileges'),
    path('api/', include('backend_app.urls')),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
