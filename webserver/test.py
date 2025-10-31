import subprocess

def test(connection="microhard"):
    command = ["nmcli", "-t", "-f", "DEVICE,TYPE,STATE,CONNECTION", "device"]
    payload = []
    try: 
        output = subprocess.run(command, shell=False, capture_output=True, check=False)
        print(output.stdout.decode())
        lines = output.stdout.decode().splitlines()
        for line in lines:
            device, kind, state, connection = line.split(":")
            if kind != "bridge" and device[0] != "v" and kind == "ethernet":
                payload.append({"device": device, "type": kind, "state": state, "connection": connection})
                
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        print(f"Stderr: {e.stderr}")
        payload = {"error"}

    print(payload)
    return jsonify(success=True, payload=payload)


'''
Error: 'device status': invalid field 'none'; allowed fields: 
DEVICE,TYPE,STATE,IP4-CONNECTIVITY,IP6-CONNECTIVITY,DBUS-PATH,CONNECTION,CON-UUID,CON-PATH


nmcli -m multiline device (puts all things prefixed in its own line)
nmcli -f field device lists only that field

manage connections

nmcli connection modify microhard connection.autoconnect no
nmcli connection show microhard
'''

if '__main__' == __name__:
    test()