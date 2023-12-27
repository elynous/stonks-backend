import pandas as pd
from rest_framework.views import APIView
from rest_framework.response import Response
from nsepython import nse_eq, nse_quote, nse_largedeals, nse_largedeals_historical, nse_results, nse_past_results, nse_blockdeal, nse_marketStatus, nse_fiidii, get_beta,nse_most_active,nsetools_get_quote,nse_index,nse_get_advances_declines,nse_get_top_gainers,get_blockdeals,get_bhavcopy
from .serializers import StockLTPSerializer, EquityDeliveryDetailsSerializer, BetaComparisonSerializer, MostActiveSerializer,StockQuoteSerializer,IndexSerializer,AdvancesDeclinesSerializer,TopGainersSerializer,BlockDealSerializer,BhavCopySerializer
from django.views import View
from django.http import HttpResponse
import json
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from rest_pandas import PandasView
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import GenericAPIView


class StockLTPView(APIView):
    def get(self, request, symbol):
        data = nse_eq(symbol)
        print("API Response:", data)  # Add this line to print the response
        serializer = StockLTPSerializer(data)
        return Response(serializer.data)


class EquityDeliveryDetailsView(APIView):
    def get(self, request, symbol, section):
        payload = nse_quote(symbol, section)
        serializer = EquityDeliveryDetailsSerializer(payload)
        return Response(serializer.data)

class LargeDealsView(APIView):
    def get(self, request, mode):
        payload = nse_largedeals(mode)
        return Response(payload)

class HistoricalLargeDealsView(APIView):
    def get(self, request, from_date, to_date, mode):
        payload = nse_largedeals_historical(from_date, to_date, mode)
        return Response(payload)

class ResultsView(APIView):
    def get(self, request, index, period):
        payload = nse_results(index, period)
        return Response(payload)

class PastResultsView(APIView):
    def get(self, request, symbol):
        payload = nse_past_results(symbol)
        return Response(payload)

class BlockDealWatchView(APIView):
    def get(self, request):
        payload = nse_blockdeal()
        return Response(payload)

class MarketStatusView(APIView):
    def get(self, request):
        payload = nse_marketStatus()
        return Response(payload)

class FiiDiiView(APIView):
    def get(self, request):
        payload = nse_fiidii()
        return Response(payload)

class BetaView(APIView):
    def get(self, request, symbol):
        payload = get_beta(symbol)
        return Response(payload)

class BetaComparisonView(APIView):
    def get(self, request, symbol1, symbol2):
        beta_value1 = get_beta(symbol1, 255, symbol2)
        beta_value2 = get_beta(symbol2, 255, symbol1)

        data = {
            'symbol1_input': symbol1,
            'symbol2_input': symbol2,
            'beta_value1': beta_value1,
            'beta_value2': beta_value2,
        }

        serializer = BetaComparisonSerializer(data)
        return Response(serializer.data)

@api_view(['GET'])
def most_active(request):
    most_active_stocks = nse_most_active(type="securities", sort="value")

    # Check if there is any data
    if most_active_stocks.empty:
        return Response({'error': 'No data available'}, status=404)

    # Convert DataFrame to list of dictionaries
    stocks_data = most_active_stocks.to_dict(orient='records')

    # Serialize the data
    serializer = MostActiveSerializer(data=stocks_data, many=True)
    serializer.is_valid()

    # Check if the request wants JSON or HTML
    if 'application/json' in request.headers.get('Accept', ''):
        return Response(serializer.data)
    else:
        # Render HTML template
        return render(request, 'most_active.html', {'stocks_data': serializer.data})
    

class StockQuoteView(APIView):
    def get(self, request, symbol):
        stock_data = nsetools_get_quote(symbol)
        serializer = StockQuoteSerializer(data=stock_data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
    
class IndexDataView(APIView):
    def get(self, request, *args, **kwargs):
        index_data = nse_index()

        # Check if there is any data
        if index_data.empty:
            return Response({"detail": "No data available"}, status=status.HTTP_404_NOT_FOUND)

        # Convert DataFrame to dictionary
        index_data_dict = index_data.to_dict(orient='records')

        # Serialize the data
        serializer = IndexSerializer(data=index_data_dict, many=True)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)
    
class IndexDataView(APIView):
    def get(self, request, *args, **kwargs):
        index_data = nse_index()

        # Check if there is any data
        if index_data.empty:
            return Response({"detail": "No data available"}, status=status.HTTP_404_NOT_FOUND)

        # Convert DataFrame to dictionary
        index_data_dict = index_data.to_dict(orient='records')

        # Serialize the data
        serializer = IndexSerializer(data=index_data_dict, many=True)
        
        if not serializer.is_valid():
            print(serializer.errors)  # Add this line to print serializer errors
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.validated_data)
    

class AdvancesDeclinesView(APIView):
    def get(self, request, *args, **kwargs):
        advances_declines_data = nse_get_advances_declines()

        # Convert DataFrame to dictionary
        advances_declines_dict = advances_declines_data.to_dict(orient='records')

        serializer = AdvancesDeclinesSerializer(data=advances_declines_dict, many=True)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.validated_data)
    
class TopGainersPagination(PageNumberPagination):
    page_size = 10  # Adjust the page size as needed

    
class TopGainersView(GenericAPIView):
    pagination_class = TopGainersPagination

    def get(self, request, *args, **kwargs):
        try:
            # Call the function to get top gainers data
            top_gainers_data = nse_get_top_gainers()

            # Check if there is any data
            if top_gainers_data.empty:
                return Response({"detail": "No data available"})

            # Paginate the DataFrame
            page = self.paginate_queryset(top_gainers_data)

            # Convert the paginated DataFrame to dictionary
            top_gainers_data_dict = page.to_dict(orient='records')

            # Serialize the data using the serializer
            serializer = TopGainersSerializer(data=top_gainers_data_dict, many=True)
            serializer.is_valid(raise_exception=True)

            # Return the paginated serialized data in the response
            return self.get_paginated_response(serializer.validated_data)

        except Exception as e:
            # Handle exceptions and return an error response
            return Response({"detail": f"Error: {str(e)}"}, status=500)
        
class BlockDealsView(APIView):
    def get(self, request, *args, **kwargs):
        block_deals_data = get_blockdeals()

        # Check if there is any data
        if block_deals_data.empty:
            return Response({"detail": "No data available"}, status=status.HTTP_404_NOT_FOUND)

        # Assuming get_blockdeals() returns a DataFrame with the required columns
        # If not, modify this part based on the actual structure of the DataFrame
        serialized_data = block_deals_data.to_dict(orient='records')

        # Serialize the data
        serializer = BlockDealSerializer(data=serialized_data, many=True)
        
        # Validate the serializer data
        if serializer.is_valid():
            return Response(serializer.validated_data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
# class BhavCopyView(APIView):
#     def get(self, request, *args, **kwargs):
#         # Replace 'your_module' with the actual module where get_bhavcopy is defined
#         bhavcopy_data = get_bhavcopy("04-06-2021")
#         # Serialize the data
#         serializer = BhavCopySerializer(data=bhavcopy_data, many=True)
#         #serializer.is_valid(raise_exception=True)
#         #return Response(serializer.validated_data)
#         serializer.is_valid(raise_exception=True)
#         return Response(serializer.validated_data, status=status.HTTP_200_OK)
    

class BhavCopyView(APIView):
     def get(self, request, date, *args, **kwargs):
        bhavcopy_data = get_bhavcopy(date)
        print(bhavcopy_data)
        # Check if there is any data
        if bhavcopy_data.empty:
            return Response({"detail": "No data available"}, status=status.HTTP_404_NOT_FOUND)
        

        # Convert DataFrame to dictionary
        bhavcopy_data_dict = bhavcopy_data.to_dict(orient='records')

        # Serialize the data
        serializer = BhavCopySerializer(data=bhavcopy_data_dict, many=True)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)