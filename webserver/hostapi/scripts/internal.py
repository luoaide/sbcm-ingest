import subprocess


#######################################################
########## MANAGE NetworkManger CONNECTIONS ###########

def getConnections():
    command = ["nmcli", "-t", "-f", "NAME,TYPE,DEVICE,STATE", "connection"]
    payload = []
    try: 
        output = subprocess.run(command, shell=False, capture_output=True, check=False)
        print(output.stdout.decode())
        lines = output.stdout.decode().splitlines()
        for line in lines:
            name, kind, device, state = line.split(":")
            if kind != "bridge":
                payload.append({"name": name, "type": kind, "device": device, "state": state})

    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        print(f"Stderr: {e.stderr}")
        payload = {"error"}

    return payload

# gets the details about the connection profile
def getConnection(connection):
    command = ["nmcli", "-t", "connection", "show", connection]
    payload = {}
    try: 
        output = subprocess.run(command, shell=False, capture_output=True, check=False)
        print(output.stdout.decode())
        lines = output.stdout.decode().splitlines()
        for line in lines:
            setting, value = line.split(":", 1)
            payload[setting] = value
                
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        print(f"Stderr: {e.stderr}")
        payload = {"error"}

    return payload

# bulk modifies the connection profile
def setConnection(connection):
    return {}

###################################################
########## MANAGE NetworkManger DEVICES ###########
def getDevices():
    command = ["nmcli", "-t", "-f", "DEVICE,TYPE,STATE,CONNECTION", "device"]
    payload = []
    try: 
        output = subprocess.run(command, shell=False, capture_output=True, check=False)
        print(output.stdout.decode())
        lines = output.stdout.decode().splitlines()
        for line in lines:
            device, kind, state, connection = line.split(":")
            if kind != "bridge" and device[0] != "v" and kind == "ethernet":
                payload.append({"name": device, "type": kind, "state": state, "connection": connection})
                
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        print(f"Stderr: {e.stderr}")
        payload = {"error"}

    return payload

def getDevice(device):
    command = ["nmcli", "-t", "device", "show", device]
    payload = {}
    try: 
        output = subprocess.run(command, shell=False, capture_output=True, check=False)
        print(output.stdout.decode())
        lines = output.stdout.decode().splitlines()
        for line in lines:
            setting, value = line.split(":", 1)
            payload[setting] = value
                
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        print(f"Stderr: {e.stderr}")
        payload = {"error"}

    return payload

# @api.route("/internal/<device>/<connection>", methods=["POST"])
# def setConnection(device, connection):
#     return {}

# @app.route("/uas/announceStreamEnd/<nodeID>/<pathName>", methods=["GET"])
# def announceStreamEnd(nodeID, pathName):
#     return {}
