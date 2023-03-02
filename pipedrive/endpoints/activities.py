class Activities(object):
    def __init__(self, client):
        self._client = client

    def get_activity(self, activity_id, **kwargs):
        url = f"activities/{activity_id}"
        return self._client._get(self._client.BASE_URL + url, **kwargs)

    def get_all_activities(self, params=None, **kwargs):
        url = "activities"
        return self._client._get(self._client.BASE_URL + url, params=params, **kwargs)
    
    def get_all_activities_with_filter(self, filter_id, params=None, **kwargs):
        url = f"activities?filter_id={filter_id}"
        return self._client._get(self._client.BASE_URL + url, params=params, **kwargs)

    def create_activity(self, data, **kwargs):
        url = "activities"
        return self._client._post(self._client.BASE_URL + url, json=data, **kwargs)

    ############################################################################################
    def count_of_email(self):
        params = {"type": "email"}
        activities = self.get_all_activities_with_filter(50, params=params)["data"]
        
        result = {"count_of_email": len(activities)}
        self._client.results.update(result)
        return result
    
    def count_of_meeting(self):
        params = {"type": "meeting"}
        activities = self.get_all_activities_with_filter(52, params=params)["data"]
        
        result = {"count_of_meeting": len(activities)}
        self._client.results.update(result)
        return result
    
    def count_of_call(self):
        params = {"type": "call"}
        activities = self.get_all_activities_with_filter(41, params=params)["data"]
        
        result = {"count_of_call": len(activities)}
        self._client.results.update(result)
        return result
    
    def activities_completed_by_agents(self):
        params = {"user_id": "0"}
        activities = self.get_all_activities_with_filter(51, params=params)["data"]
        user_ids = list({i["assigned_to_user_id"] for i in activities})
        
        completed = []
        for uid in user_ids:
            params = {"user_id": uid, "done": 1}
            activity = self.get_all_activities_with_filter(51, params=params)["data"]
            try:
                name = activity[0]["owner_name"]
                task_completed = len(activity)
                data = {"user_id": uid, "name": name, "task_completed": task_completed}
                completed.append(data)
            except TypeError:
                continue
            
        result = {"activities_completed_by_agents": completed}
        self._client.results.update(result)
        return result
