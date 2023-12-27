from rest_framework.views import APIView
from rest_framework.response import Response
from nsepython import nse_eq, nse_quote, nse_largedeals, nse_largedeals_historical, nse_results, nse_past_results, nse_blockdeal, nse_marketStatus, nse_fiidii, get_beta
from rest_framework import serializers

# class StockLTPSerializer(serializers.Serializer):
#     last_price = serializers.FloatField()
#     open = serializers.FloatField()
#     intra_day_low = serializers.FloatField()
#     intra_day_high = serializers.FloatField()
#     close = serializers.FloatField()
#     pd_sector_pe = serializers.FloatField()
#     pd_sector_ind = serializers.FloatField()

class StockLTPSerializer(serializers.Serializer):
    last_price = serializers.SerializerMethodField()

    def get_last_price(self, obj):
        try:
            return float(obj.get('priceInfo', {}).get('lastPrice', 0))
        except (ValueError, TypeError):
            return 0.0


class EquityDeliveryDetailsSerializer(serializers.Serializer):
    delivery_quantity = serializers.FloatField()
    delivery_percentage = serializers.FloatField()
    delivery_to_traded_quantity = serializers.FloatField()
    delivery_at_bid_quantity = serializers.FloatField()
    delivery_at_bid_percentage = serializers.FloatField()
    delivery_at_offer_quantity = serializers.FloatField()
    delivery_at_offer_percentage = serializers.FloatField()

class LargeDealsSerializer(serializers.Serializer):
    time = serializers.DateTimeField()
    price = serializers.FloatField()
    quantity = serializers.FloatField()
    value = serializers.FloatField()
    buyer = serializers.CharField()
    seller = serializers.CharField()

class HistoricalLargeDealsSerializer(serializers.Serializer):
    date = serializers.DateField()
    time = serializers.TimeField()
    price = serializers.FloatField()
    quantity = serializers.FloatField()
    value = serializers.FloatField()
    buyer = serializers.CharField()
    seller = serializers.CharField()

class ResultsSerializer(serializers.Serializer):
    result_field1 = serializers.CharField()
    result_field2 = serializers.CharField()
    # Add necessary fields based on the actual data structure returned by ResultsView

class PastResultsSerializer(serializers.Serializer):
    result_field1 = serializers.CharField()
    result_field2 = serializers.CharField()
    # Add necessary fields based on the actual data structure returned by PastResultsView

class BlockDealWatchSerializer(serializers.Serializer):
    block_deal_date = serializers.DateField()
    security_name = serializers.CharField()
    symbol = serializers.CharField()
    high_price = serializers.FloatField()
    low_price = serializers.FloatField()
    close_price = serializers.FloatField()
    quantity = serializers.FloatField()
    value = serializers.FloatField()

class MarketStatusSerializer(serializers.Serializer):
    is_market_open = serializers.BooleanField()
    market_status = serializers.CharField()
    market_status_message = serializers.CharField()

class FiiDiiSerializer(serializers.Serializer):
    fii_value = serializers.FloatField()
    dii_value = serializers.FloatField()
    fii_dii_ratio = serializers.FloatField()

class BetaSerializer(serializers.Serializer):
    beta_value = serializers.FloatField()

class BetaComparisonSerializer(serializers.Serializer):
    symbol1 = serializers.CharField(source='symbol1_input')
    symbol2 = serializers.CharField(source='symbol2_input')
    beta_value1 = serializers.FloatField()
    beta_value2 = serializers.FloatField()


class MostActiveSerializer(serializers.Serializer):
    symbol = serializers.CharField()
    identifier = serializers.CharField()
    lastPrice = serializers.FloatField()
    pChange = serializers.FloatField()
    quantityTraded = serializers.IntegerField()
    totalTradedVolume = serializers.IntegerField()
    totalTradedValue = serializers.FloatField()
    previousClose = serializers.FloatField()
    exDate = serializers.CharField(allow_null=True)
    purpose = serializers.CharField(allow_null=True)
    yearHigh = serializers.FloatField()
    yearLow = serializers.FloatField()
    change = serializers.FloatField()
    open = serializers.FloatField()
    closePrice = serializers.FloatField()
    dayHigh = serializers.FloatField()
    dayLow = serializers.FloatField()
    lastUpdateTime = serializers.CharField()


class StockQuoteSerializer(serializers.Serializer):
    symbol = serializers.CharField()
    identifier = serializers.CharField(required=False, allow_blank=True)
    series = serializers.CharField()
    open = serializers.CharField()
    dayHigh = serializers.CharField()
    dayLow = serializers.CharField()
    lastPrice = serializers.CharField()
    previousClose = serializers.CharField()
    change = serializers.FloatField()
    pChange = serializers.FloatField()
    totalTradedVolume = serializers.IntegerField()
    totalTradedValue = serializers.FloatField()
    lastUpdateTime = serializers.CharField()
    yearHigh = serializers.CharField()
    yearLow = serializers.CharField()
    nearWKH = serializers.FloatField()
    nearWKL = serializers.FloatField()
    perChange365d = serializers.FloatField()
    date365dAgo = serializers.CharField()
    chart365dPath = serializers.CharField()
    date30dAgo = serializers.CharField()
    perChange30d = serializers.FloatField()
    chart30dPath = serializers.CharField()
    chartTodayPath = serializers.CharField()
    meta = serializers.DictField()

class IndexSerializer(serializers.Serializer):
    index = serializers.CharField()
    lastPrice = serializers.FloatField()
    change = serializers.FloatField()
    pChange = serializers.FloatField()
    totalTradedValue = serializers.FloatField()


class AdvancesDeclinesSerializer(serializers.Serializer):
    symbol = serializers.CharField()
    identifier = serializers.CharField()
    series = serializers.CharField()
    open = serializers.FloatField()
    dayHigh = serializers.FloatField()
    dayLow = serializers.FloatField()
    # lastPrice = serializers.FloatField()
    # previousClose = serializers.FloatField()
    # change = serializers.FloatField()
    # pChange = serializers.FloatField()
    # totalTradedValue = serializers.FloatField()
    # nearWKH = serializers.FloatField()
    # nearWKL = serializers.FloatField()
    # perChange365d = serializers.FloatField()
    # date365dAgo = serializers.DateField(format="%Y-%m-%d")
    # chart365dPath = serializers.URLField()
    # date30dAgo = serializers.DateField(format="%Y-%m-%d")
    # perChange30d = serializers.FloatField()
    # chart30dPath = serializers.URLField()
    # chartTodayPath = serializers.URLField()
    # meta = serializers.JSONField()

    # def validate_identifier(self, value):
    #     if not value.strip():
    #         raise serializers.ValidationError("Identifier cannot be blank.")
    #     return value

    # def validate_date365dAgo(self, value):
    #     # You can add additional date validation logic if needed
    #     return value

    # def validate_date30dAgo(self, value):
    #     # You can add additional date validation logic if needed
    #     return value


class TopGainersSerializer(serializers.Serializer):
    symbol = serializers.CharField()
    identifier = serializers.CharField()
    series = serializers.CharField()
    open = serializers.FloatField()
    dayHigh = serializers.FloatField()
    dayLow = serializers.FloatField()
    lastPrice = serializers.FloatField()
    previousClose = serializers.FloatField()
    change = serializers.FloatField()
    pChange = serializers.FloatField()
    nearWKH = serializers.FloatField()
    nearWKL = serializers.FloatField()
    perChange365d = serializers.FloatField()
    date365dAgo = serializers.DateField()
    chart365dPath = serializers.URLField()
    date30dAgo = serializers.DateField()
    perChange30d = serializers.FloatField()
    chart30dPath = serializers.URLField()
    chartTodayPath = serializers.URLField()
    meta = serializers.JSONField()

class BlockDealSerializer(serializers.Serializer):
    date = serializers.DateField()
    symbol = serializers.CharField()
    security_name = serializers.CharField()
    client_name = serializers.CharField()
    buy_sell = serializers.CharField()
    quantity_traded = serializers.IntegerField()
    trade_price = serializers.FloatField()

class BhavCopySerializer(serializers.Serializer):
    SYMBOL = serializers.CharField()
    SERIES = serializers.CharField()
    DATE1 = serializers.DateField()
    PREV_CLOSE = serializers.FloatField()
    OPEN_PRICE = serializers.FloatField()
    HIGH_PRICE = serializers.FloatField()
    LOW_PRICE = serializers.FloatField()
    LAST_PRICE = serializers.FloatField()
    CLOSE_PRICE = serializers.FloatField()
    AVG_PRICE = serializers.FloatField()
    TTL_TRD_QNTY = serializers.IntegerField()
    TURNOVER_LACS = serializers.FloatField()
    NO_OF_TRADES = serializers.IntegerField()
    DELIV_QTY = serializers.IntegerField()
    DELIV_PER = serializers.FloatField()