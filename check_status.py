import requests
import datetime
import json
import pandas as pd
import html


column_names = ['date' , 'center_name' , 'pincode', 'available_capacity' , 'vaccine']
availability_data = pd.DataFrame(columns = column_names)

#print("State code: ", state_code)

#response = requests.get("https://cdn-api.co-vin.in/api/v2/admin/location/districts/{}".format(state_code))
#json_data = json.loads(response.text)
#for i in json_data["districts"]:
#    print(i["district_id"],'\t', i["district_name"])
#print("\n")

#############################
##### INPUTS ################
#############################
print_flag = 'y'
state_code = 21
DIST_ID = 363 # Pune
numdays = 5
age = 35

#############################
##### AVAILABILITY ################
#############################

base = datetime.datetime.today()
date_list = [base + datetime.timedelta(days=x) for x in range(numdays)]
date_str = [x.strftime("%d-%m-%Y") for x in date_list]

for INP_DATE in date_str:
    URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={}&date={}".format(DIST_ID, INP_DATE)
    response = requests.get(URL)
    if response.ok:
        resp_json = response.json()
        # print(json.dumps(resp_json, indent = 1))
        if resp_json["centers"]:
            #print("Availability on: {}".format(INP_DATE))
            if(print_flag=='y' or print_flag=='Y'):
                for center in resp_json["centers"]:
                    for session in center["sessions"]:      
                        if session["min_age_limit"] <= age & session["available_capacity"] > 0 :
                            #print("center_name : ", center["name"])
                            #print("address : ", center["address"])
                            #print("pincode : ", center["pincode"])
                            #print("\t Price: ", center["fee_type"])
                            #print("\t available_capacity: ", session["available_capacity"])
                            #if(session["vaccine"] != ''):
                            #    print("\t Vaccine: ", session["vaccine"])
                            if availability_data.size > 0 : 
                                ind = len(availability_data.index)
                            else :
                                ind = 0
                            availability_data.loc[ind] = [INP_DATE, center["name"] , center["pincode"], session["available_capacity"],session["vaccine"] ]                                        
        
        else:
            print("No available slots on {}".format(INP_DATE))
            
if availability_data.size > 0 :
    display(availability_data)

else :
    print("No available slots")
