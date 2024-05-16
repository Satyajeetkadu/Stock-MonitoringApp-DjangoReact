from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action, api_view
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import Watchlist
from .serializers import WatchlistSerializer
import requests

ALPHA_VANTAGE_API_KEY = ''#Your API Key

def fetch_stock_data(symbol):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=1min&apikey={ALPHA_VANTAGE_API_KEY}'
    response = requests.get(url)
    data = response.json()
    try:
        latest_time = list(data['Time Series (1min)'].keys())[0]
        latest_data = {latest_time: data['Time Series (1min)'][latest_time]}
        return latest_data
    except KeyError:
        return None

@method_decorator(csrf_exempt, name='dispatch')
class WatchlistViewSet(viewsets.ModelViewSet):
    queryset = Watchlist.objects.all()
    serializer_class = WatchlistSerializer

    @action(detail=False, methods=['post'])
    @csrf_exempt
    def add_symbol(self, request):
        symbol = request.data.get('symbol')
        stock_data = fetch_stock_data(symbol)
        if stock_data:
            watchlist_item, created = Watchlist.objects.get_or_create(symbol=symbol)
            watchlist_item.stock_data = stock_data
            watchlist_item.save()
            serializer = self.get_serializer(watchlist_item)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"error": "Invalid symbol"}, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_exempt, name='dispatch')
class FetchStockDataView(APIView):
    @csrf_exempt
    def get(self, request):
        symbol = request.query_params.get('symbol')
        data = fetch_stock_data(symbol)
        if data:
            return Response(data, status=status.HTTP_200_OK)
        return Response({"error": "Invalid symbol"}, status=status.HTTP_400_BAD_REQUEST)