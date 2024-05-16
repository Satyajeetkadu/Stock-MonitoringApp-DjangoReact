from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WatchlistViewSet, FetchStockDataView

router = DefaultRouter()
router.register(r'watchlists', WatchlistViewSet, basename='watchlist')

urlpatterns = [
    path('', include(router.urls)),
    path('fetch-stock-data/', FetchStockDataView.as_view(), name='fetch-stock-data'),
]