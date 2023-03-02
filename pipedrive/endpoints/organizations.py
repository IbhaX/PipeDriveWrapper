class Organizations(object):
    def __init__(self, client):
        self._client = client

    def get_organization(self, organization_id, **kwargs):
        url = f"organizations/{organization_id}"
        return self._client._get(self._client.BASE_URL + url, **kwargs)

    def get_all_organizations(self, params=None, **kwargs):
        url = "organizations"
        return self._client._get(self._client.BASE_URL + url, params=params, **kwargs)
    
    def get_all_organizations_with_filter(self, filter_id, params=None, **kwargs):
        url = f"organizations?filter_id={filter_id}"
        return self._client._get(self._client.BASE_URL + url, params=params, **kwargs)

    def create_organization(self, data, **kwargs):
        url = "organizations"
        return self._client._post(self._client.BASE_URL + url, json=data, **kwargs)
    ################################################################################################
    
    def new_organizations_added(self):
        organizations = self.get_all_organizations_with_filter(8)["data"]
        org_names = [{"name": i["name"]} for i in organizations]
        result = {"organizations_count": len(organizations), "organizations": org_names}
        self._client.results.update(result)
        return result
