import os
import json

from pipedrive.client import Client

from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("PIPEDRIVE_API_KEY")
client_id= os.getenv("PIPEDRIVE_client_id")
client_secret= os.getenv("PIPEDRIVE_client_secret")

client = Client(client_id=client_id, client_secret=client_secret)
client.authorize()

# client = Client(domain="ibhax-sandbox")
# client.set_api_token(API_KEY)


def assignments():
    deals = client.deals
    deals.deals_won_lost_last_30_days()
    deals.count_of_new_deals()
    deals.deals_won_lost_values_last_30_days()

    activities = client.activities
    activities.count_of_call()
    activities.count_of_email()
    activities.count_of_meeting()
    activities.activities_completed_by_agents()

    persons = client.persons
    persons.new_contacts_added()

    organizations = client.organizations
    organizations.new_organizations_added()

    users = client.users
    users.active_users()

    print(json.dumps(client.results, indent=2))

assignments()
