import requests
import json
import base64
import time

class JSON_Server:

    def __init__(self):
        ############### JSON SERVER SETUP ###############

        # Set your GitHub Personal Access Token and the repository information
        self.access_token = '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'
        self.repository_owner = 'ColeMalinchock1'
        self.repository_name = 'HGT-JSON-Server'

        # Path to local json file and the name of json file on GitHub
        self.file_path = "./HGT_Data.json"
        self.file_backup_path = "./HGT_Backup.json"

        # Define the API endpoint for creating a new file
        self.api_url = f'https://api.github.com/repos/{self.repository_owner}/{self.repository_name}/contents/{self.file_path}'
        self.api_backup_url = f'https://api.github.com/repos/{self.repository_owner}/{self.repository_name}/contents/{self.file_backup_path}'

        self.headers = {
        'Authorization': f'token {self.access_token}'
        }

        self.patient1_name = "Cole Malinchock"
        self.patient1_age = "20"
        self.patient1_guardian = "Mike and Laura Malinchock"
        self.patient1_number = "919-240-4776"

        self.patient2_name = "John Bullock"
        self.patient2_age = "12"
        self.patient2_guardian = "Amy and Kelley Bullock"
        self.patient2_number = "919-547-3245"

        self.patient1_info = {
        "name": self.patient1_name,
        "age": self.patient1_age,
        "guardian": self.patient1_guardian,
        "phone number": self.patient1_number
        }

        self.patient2_info = {
        "name": self.patient2_name,
        "age": self.patient2_age,
        "guardian": self.patient2_guardian,
        "phone number": self.patient2_number
        }

        self.keep_waiting = False
        self.last_time_JSON = time.time()
        self.last_time_get_JSON = time.time()
        self.last_time_put_JSON = time.time()
        self.JSON_connected = False

        # Time in between puts and gets to stay under the 5000 an hour limit
        self.wait_time = 4 # Seconds

    def save_json(self, current_tension, tension_setpoint):
        # Opening the local file and getting the contents
        with open(self.file_path , 'r') as file1 , open(self.file_backup_path , 'r') as file2:
            self.updated_file_content = json.loads(file1.read())
            self.updated_file_backup_content = json.loads(file2.read())

        # Getting time
        timer = time.time()

        # Getting date
        date = str(time.asctime())

        # Formatted so that date is Month , Day , Time (hr:mi:se)
        date = date.split()
        date = date[1:4]

        # Getting tension
        tension = current_tension

        # Tension setpoint
        tension_setpoint = 12

        # Creating new data on tension and time
        patient1_data = {
        "date": date,
        "time": timer,
        "tension": str(tension),
        "tension_setpoint": str(tension_setpoint)
        }

        patient2_data = {
        "date": date,
        "time": timer,
        "tension": str((tension + 1) * 2),
        "tension_setpoint": str(tension_setpoint)
        }
    

        # Range of short graph
        # 1 hour range (Every 0.1 second)
        max_size = 36000

        if len(self.self.updated_file_content["data"][0][self.patient1_name][1]["patient data"]) > max_size:
            self.updated_file_content["data"][0][self.patient1_name][1]["patient data"].pop(0)
            self.updated_file_content["data"][1][self.patient2_name][1]["patient data"].pop(0)
            print("Removing old data")
        else:
            pass

        # Appending new data to current patient
        print("Appending new data to current patient")
        self.updated_file_content["data"][0][self.patient1_name][1]["patient data"].append(patient1_data)
        self.updated_file_content["data"][1][self.patient2_name][1]["patient data"].append(patient2_data)

        # Appending new data to backup content and setting how often it updates
        minutes = 10

        if time.time() - self.last_time_JSON > 60:
                keep_waiting = False

        if int(str(time.asctime()).split()[3][3:5]) % minutes == 0 and not keep_waiting:
                print("Appending new data to backup")
                self.updated_file_backup_content["data"][0][self.patient1_name][1]["patient data"].append(patient1_data)
                self.updated_file_backup_content["data"][1][self.patient2_name][1]["patient data"].append(patient2_data)
                keep_waiting = True
                self.last_time_JSON = time.time()


        # Writing the updated file to the local computer
        with open(self.file_path , 'w') as file1 , open(self.file_backup_path , 'w') as file2:
                json.dump(self.updated_file_content , file1 , indent = 4)
                json.dump(self.updated_file_backup_content , file2 , indent = 4)
                print("Data added to local file")

    def push_to_git(self):

        if time.time() - self.last_time_get_JSON > self.wait_time:
            # Making a GET request for current file from GitHub
            response = requests.get(self.api_url, headers=self.headers)
            response_backup = requests.get(self.api_backup_url , headers = self.headers)
            self.last_time_get_JSON = time.time()

        
            # If GET request is approved
            if (response.status_code == 200 and response_backup.status_code == 200):

                    # Receiving current data
                    current_data = response.json()
                    current_sha = current_data['sha']

                    current_backup_data = response_backup.json()
                    current_backup_sha = current_backup_data['sha']

                    # Create the updated file using local data
                    updated_file = {
                    'message': 'Update JSON file',
                    'content': base64.b64encode(json.dumps(self.updated_file_content).encode()).decode(),
                    'sha': current_sha  # Include the current sha
                    }

                    updated_backup_file = {
                    'message': 'Update backup JSON file',
                    'content': base64.b64encode(json.dumps(self.updated_file_backup_content).encode()).decode(),
                    'sha': current_backup_sha  # Include the current sha
                    }

                    # Send a PUT request to update the file
                    response = requests.put(self.api_url, headers = self.headers , json = updated_file)
                    response_backup = requests.put(self.api_backup_url , headers = self.headers , json = updated_backup_file)
                    self.last_time_put_JSON = time.time()

                    # If statement for put request
                    if response.status_code == 200:
                            print('File successfully updated on GitHub')
                    else:
                            print('Failed to update the file. Status code: ' , response.status_code)
                            print('Response: ' , response.json)

                    # If statement for put request
                    if response_backup.status_code == 200:
                            print('File successfully updated on GitHub')
                    else:
                            print('Failed to update the file. Status code: ' , response_backup.status_code)
                            print('Response: ' , response_backup.json)

            else:
                    print('Failed to retrieve the current file data. Status code:', response.status_code)
                    print('Response:', response.json())
        else:
            print("Waiting to get and put on Github")