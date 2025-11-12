import subprocess


#######################################################
########## MANAGE NetworkManger CONNECTIONS ###########

def getProfiles():
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
        payload = {e.stderr}

    return payload

# gets the details about the connection profile
def getProfile(profile):
    command = ["nmcli", "-t", "connection", "show", profile]
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
        payload = {e.stderr}

    return payload

# modifies a connection profile
# sudo nmcli connection add type ethernet ifname eth0 con-name static-eth0 \
#   ipv4.addresses 192.168.1.100/24 \
#   ipv4.gateway 192.168.1.1 \
#   ipv4.dns 8.8.8.8 \
#   ipv4.method manual \
#   autoconnect yes
def modifyProfile(profile, args):
    command = ["nmcli", "connection", "modify", profile] + args
    payload = {}
    try: 
        subprocess.run(command, shell=False, capture_output=True, check=False)
        payload = {"success": True}
                
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        print(f"Stderr: {e.stderr}")
        payload = {e.stderr}

    return payload

def activateProfile(profile):
    command = ["nmcli", "connection", "up", profile]
    payload = {}
    try: 
        subprocess.run(command, shell=False, capture_output=True, check=False)
        payload = {"success": True}
                
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        print(f"Stderr: {e.stderr}")
        payload = {e.stderr}

    return payload

def deactivateProfile(profile):
    command = ["nmcli", "connection", "down", profile]
    payload = {}
    try: 
        subprocess.run(command, shell=False, capture_output=True, check=False)
        payload = {"success": True}
                
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        print(f"Stderr: {e.stderr}")
        payload = {e.stderr}

    return payload

# bulk modifies the connection profile
def activateProfile(profile):
    return {}

# bulk modifies the connection profile
def disableProfile(profile):
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
        payload = {e.stderr}

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
        payload = {e.stderr}

    return payload