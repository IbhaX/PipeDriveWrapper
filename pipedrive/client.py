import os
import requests
import json
import webbrowser
from urllib.parse import urlencode
from datetime import datetime, timedelta
from dateutil.parser import parse

from pipedrive import exceptions
from pipedrive.endpoints.activities import Activities
from pipedrive.endpoints.deals import Deals
from pipedrive.endpoints.filters import Filters
from pipedrive.endpoints.organizations import Organizations
from pipedrive.endpoints.persons import Persons
from pipedrive.endpoints.users import Users

base_dir = os.path.dirname(__file__)
token_file_path = os.path.join(base_dir, "token.json")

class Client:
    BASE_URL = "https://api.pipedrive.com/"
    OAUTH_BASE_URL = "https://oauth.pipedrive.com/oauth/"
    REDIRECT_URI = "https://flask-production-1c3f.up.railway.app/callback?format=plain"
    results = {}
    
    def __init__(self, client_id=None, client_secret=None, domain=None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = None
        self.api_token = None
        self.activities = Activities(self)
        self.deals = Deals(self)
        self.filters = Filters(self)
        self.organizations = Organizations(self)
        self.persons = Persons(self)
        self.users = Users(self)

        if domain:
            self.BASE_URL = f"https://{domain}.pipedrive.com/api/v1/"

    def authorize(self, state=None):
        params = {
            "client_id": self.client_id,
            "redirect_uri": self.REDIRECT_URI,
        }

        if state is not None:
            params["state"] = state

        if not os.path.exists(token_file_path):
            input("Hit enter -> Authorize App -> Copy Code -> paste it in Terminal...")
            webbrowser.open(f"{self.OAUTH_BASE_URL}authorize?{urlencode(params)}")
            code = input("Enter copied code from website: ")
            self.access_token = self.exchange_code(code)["access_token"]
            
            with open(token_file_path, "w") as f:
                date = datetime.now() + timedelta(hours=2)
                validity = datetime.strftime(date, "%Y-%m-%d %H:%M:%S")
                token = json.dumps({"access_token": self.access_token, "validity": validity})
                f.write(token)
        else:
            with open(token_file_path) as f:
                data = json.load(f)
                
            if datetime.now() < parse(data["validity"]):
                self.access_token = data["access_token"]
            else:
                print("Token Expired... Authorize once again...")
                os.remove(token_file_path)
                self.authorize()
         
    def exchange_code(self, code):
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": self.REDIRECT_URI,
        }
        return self._post(
            f"{self.OAUTH_BASE_URL}token",
            data=data,
            auth=(self.client_id, self.client_secret),
        )

    def set_access_token(self, access_token):
        self.access_token = access_token

    def set_api_token(self, api_token):
        self.api_token = api_token

    def _get(self, url, params=None, **kwargs):
        return self._request("get", url, params=params, **kwargs)

    def _post(self, url, **kwargs):
        return self._request("post", url, **kwargs)

    def _put(self, url, **kwargs):
        return self._request("put", url, **kwargs)

    def _patch(self, url, **kwargs):
        return self._request("patch", url, **kwargs)

    def _delete(self, url, **kwargs):
        return self._request("delete", url, **kwargs)

    def _request(self, method, url, headers=None, params=None, **kwargs):
        _headers = headers or {}
        _params = params or {}
        if self.access_token:
            _headers["Authorization"] = f"Bearer {self.access_token}"
        if self.api_token:
            _params["api_token"] = self.api_token

        return self._parse(requests.request(method, url, headers=_headers, params=_params, **kwargs))

    def _parse(self, response):
        status_code = response.status_code
        if "Content-Type" in response.headers and "application/json" in response.headers["Content-Type"]:
            r = response.json()
        else:
            return response.text

        if not response.ok:
            error = None
            if "error" in r:
                error = r["error"]
            if status_code == 400:
                raise exceptions.BadRequestError(error, response)
            elif status_code == 401:
                raise exceptions.UnauthorizedError(error, response)
            elif status_code == 403:
                raise exceptions.ForbiddenError(error, response)
            elif status_code == 404:
                raise exceptions.NotFoundError(error, response)
            elif status_code == 410:
                raise exceptions.GoneError(error, response)
            elif status_code == 415:
                raise exceptions.UnsupportedMediaTypeError(error, response)
            elif status_code == 422:
                raise exceptions.UnprocessableEntityError(error, response)
            elif status_code == 429:
                raise exceptions.TooManyRequestsError(error, response)
            elif status_code == 500:
                raise exceptions.InternalServerError(error, response)
            elif status_code == 501:
                raise exceptions.NotImplementedError(error, response)
            elif status_code == 503:
                raise exceptions.ServiceUnavailableError(error, response)
            else:
                raise exceptions.UnknownError(error, response)

        return r
