from django.urls import path
from .views import StockLTPView, EquityDeliveryDetailsView, LargeDealsView, HistoricalLargeDealsView, ResultsView, PastResultsView, BlockDealWatchView, MarketStatusView, FiiDiiView,BetaView,BetaComparisonView,StockQuoteView,IndexDataView,AdvancesDeclinesView,TopGainersView,BlockDealsView,BhavCopyView
from .views import most_active


urlpatterns = [
    path('stock_ltp/<symbol>/', StockLTPView.as_view(), name='stock_ltp'),
    path('equity_delivery_details/<symbol>/<section>/', EquityDeliveryDetailsView.as_view(), name='equity_delivery_details'),
    path('large_deals/<mode>/', LargeDealsView.as_view(), name='large_deals'),
    path('historical_large_deals/<from_date>/<to_date>/<mode>/', HistoricalLargeDealsView.as_view(), name='historical_large_deals'),
    path('results/<index>/<period>/', ResultsView.as_view(), name='results'),
    path('past_results/<symbol>/', PastResultsView.as_view(), name='past_results'),
    path('block_deal_watch/', BlockDealWatchView.as_view(), name='block_deal_watch'),
    path('market_status/', MarketStatusView.as_view(), name='market_status'),
    path('fii_dii/', FiiDiiView.as_view(), name='fii_dii'),
    path('beta/<symbol>/', BetaView.as_view(), name='beta'),
    path('beta_comparison/<symbol1>/<symbol2>/', BetaComparisonView.as_view(), name='beta_comparison'),
    path('most_active/', most_active, name='most_active'),
    path('stock_quote/<str:symbol>/', StockQuoteView.as_view(), name='stock_quote'),
    path('index_data/', IndexDataView.as_view(), name='index_data'),
    path('advances-declines/', AdvancesDeclinesView.as_view(), name='advances_declines'),
    path('top_gainers/', TopGainersView.as_view(), name='top_gainers'),
    path('block_deals/', BlockDealsView.as_view(), name='block_deals'),
    path('bhavcopy/<str:date>/', BhavCopyView.as_view(), name='bhavcopy'),
]
