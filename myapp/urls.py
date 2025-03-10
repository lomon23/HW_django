from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView
from .views.home import home
from .views.Book_List_API import BookListView, BookDetailView, BookViewSet
from .views.auth_DRF import RegisterView, blacklist_token, auth_drf, CustomTokenRefreshView

# Create a router for v2 API
router = DefaultRouter()
router.register('books', BookViewSet, basename='v2-books')

urlpatterns = [
    # Home page
    path('', home, name='home'),
    
    # Book APIs v1
    path('api/v1/books/', BookListView.as_view(), name='book-list-v1'),
    path('api/v1/books/<int:book_id>/', BookDetailView.as_view(), name='book-detail-v1'),
    
    # Book APIs v2
    path('api/v2/', include(router.urls)),
    
    # Authentication
    path('register/', RegisterView.as_view(), name='register'),
    path('users/', auth_drf, name='user-list'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('token/blacklist/', blacklist_token, name='token_blacklist'),
]