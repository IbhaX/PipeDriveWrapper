class Persons(object):
    def __init__(self, client):
        self._client = client

    def get_person(self, person_id, **kwargs):
        url = "persons/{}".format(person_id)
        return self._client._get(self._client.BASE_URL + url, **kwargs)

    def get_all_persons(self, params=None, **kwargs):
        url = "persons"
        return self._client._get(self._client.BASE_URL + url, params=params, **kwargs)

    def get_all_persons_with_filter(self, filter_id, params=None, **kwargs):
        url = f"persons?filter_id={filter_id}"
        return self._client._get(self._client.BASE_URL + url, params=params, **kwargs)
    
    def create_person(self, data, **kwargs):
        url = "persons"
        return self._client._post(self._client.BASE_URL + url, json=data, **kwargs)
    
    ############################################################################################
    
    def new_contacts_added(self):
        contacts = self.get_all_persons_with_filter(54)["data"]
        
        result = {"new_contacts": len(contacts)}
        self._client.results.update(result)
        return result 
        

    
