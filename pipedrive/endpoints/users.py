class Users(object):
    def __init__(self, client):
        self._client = client

    def get_user(self, user_id, **kwargs):
        url = f"users/{user_id}"
        return self._client._get(self._client.BASE_URL + url, **kwargs)

    def get_all_users(self, **kwargs):
        url = "users"
        return self._client._get(self._client.BASE_URL + url, **kwargs)

    def get_me(self, **kwargs):
        url = "users/me"
        return self._client._get(self._client.BASE_URL + url, **kwargs)
    ########################################################################
    
    def active_users(self):
        users = self.get_all_users()["data"]
        
        active = [{"id": i["id"], "name": i["name"]} for i in users if i["active_flag"]]
        result = {"active_users": active}
        self._client.results.update(result)
        return result 
        
