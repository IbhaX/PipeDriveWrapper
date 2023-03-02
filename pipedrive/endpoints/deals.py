class Deals(object):
    def __init__(self, client):
        self._client = client

    def get_deal(self, deal_id, **kwargs):
        url = f"deals/{deal_id}"
        return self._client._get(self._client.BASE_URL + url, **kwargs)

    def get_all_deals(self, params=None, **kwargs):
        url = "deals"
        return self._client._get(self._client.BASE_URL + url, params=params, **kwargs)

    def get_all_deals_with_filter(self, filter_id, params=None, **kwargs):
        url = f"deals?filter_id={filter_id}"
        return self._client._get(self._client.BASE_URL + url, params=params, **kwargs)

    def create_deal(self, data, **kwargs):
        url = "deals"
        return self._client._post(self._client.BASE_URL + url, json=data, **kwargs)
    
    ###############################################################################
    def count_of_new_deals(self):
        deals = self.get_all_deals_with_filter(48)["data"]
        result = {"new_deals_len": len(deals)}
        self._client.results.update(result)
        return result
    
    def value_of_new_deals(self):
        deals = self.get_all_deals_with_filter(48)["data"]
        result = {"new_deals_sum": sum([int(i["value"]) for i in deals])}
        self._client.results.update(result)
        return result
    
    def deals_won_lost_last_30_days(self):
        params = {"status": "won"}
        deals_won = self.get_all_deals_with_filter(48, params=params)["data"]
        
        params = {"status": "lost"}
        deals_lost = self.get_all_deals_with_filter(48, params=params)["data"]
        
        result = {"deals_won": len(deals_won), "deals_lost": len(deals_lost)}
        self._client.results.update(result)
        return result
    
    def deals_won_lost_values_last_30_days(self):
        params = {"status": "won"}
        deals_won = self.get_all_deals_with_filter(48, params=params)["data"]
        won_values = sum([int(i["value"]) for i in deals_won])
        
        params = {"status": "lost"}
        deals_lost = self.get_all_deals_with_filter(48, params=params)["data"]
        lost_values = sum([int(i["value"]) for i in deals_lost])
        
        result = {"deals_won_values": won_values, "deals_lost_values": lost_values}
        self._client.results.update(result)
        return result
    
    
