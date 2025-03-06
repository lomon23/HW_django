from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.home import home
from .views.Book_List_API import BookListView, BookDetailView, BookViewSet
from .views.auth_DRF import auth_drf
router = DefaultRouter()
router.register(r'api/v2/books', BookViewSet)

app_name = 'myapp'

urlpatterns = [
    path('', home, name='home'),
    # ============book list api===============
    # API v1 URLs
    path('api/v1/books/', BookListView.as_view(), name='book-list-v1'),
    path('api/v1/books/<int:book_id>/', BookDetailView.as_view(), name='book-detail-v1'),
    # API v2 URLs
    path('', include(router.urls)),
    # ==============auth DRF==================
    path('auth/', auth_drf, name='auth-drf'),
]