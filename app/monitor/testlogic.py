import requests
from datetime import datetime


def check_dhis2_instance(base_url, username, password):
    timestamp = None
    try:
        # Check system info
        system_info_url = f"https://{base_url}/api/system/info?"
        response = requests.get(system_info_url, auth=(username, password))
        response.raise_for_status()
        system_info = response.json()
      
        
        # Check if analytics were run today
        last_analytics_success = system_info.get('lastAnalyticsTableSuccess', '')
        timestamp =  datetime.now()
        print(timestamp)   
        analytics_status = "True" if last_analytics_success.startswith(str(timestamp.date())) else "False"
            

        # Check if dashboards are displaying data
        dashboards_status = check_dashboards(base_url, username, password)


        return ["True", analytics_status, dashboards_status, timestamp]
    except requests.exceptions.RequestException as e:
        print(e)
        return ["False", "False", "False", timestamp]

def check_dashboards(base_url, username, password):
    try:
        dashboard_url = f"https://{base_url}/api/dashboards/"
        response = requests.get(dashboard_url, auth=(username, password))
        response.raise_for_status()
        return "True"
    except requests.exceptions.RequestException:
        return "False"


#base_url = "https://emisuganda.org/emis"
#username = "hisp.satibuni"
#password = "Emis@2022"


#desiredOutput = check_dhis2_instance(base_url, username, password)
#print (desiredOutput)