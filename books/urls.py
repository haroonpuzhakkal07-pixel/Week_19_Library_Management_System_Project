from rest_framework.routers import DefaultRouter
from .views import BookViewSet, BorrowRecordViewSet, register
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'books', BookViewSet)
router.register(r'borrow-records', BorrowRecordViewSet)

urlpatterns = router.urls + [
    path('register/', register),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('refresh/', TokenRefreshView.as_view(), name='refresh')
]