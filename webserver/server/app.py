from flask import Flask, jsonify, request
from flask import render_template
import requests

app = Flask(__name__)

API_URL = "http://host-api:8173/"
# todo
# API_URL = os.getenv(ASDLFK)

conn = None

#########################
###### MAIN ROUTES ######
#########################
@app.route("/network")
def network():
    networkUrl = API_URL + "internal/network/"
    networkReq = None
    try:
        networkReq = requests.get(
            networkUrl,
            headers={
                "Content-type": "application/json; charset=UTF-8"
            }
        )
        networkReq.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        print("Http Error:",errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:",errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:",errt)
    except requests.exceptions.RequestException as err:
        print("OOps: Something Else",err)
    except:
        print("OK")

    received = networkReq.json()
    devices = received["devices"]
    profiles = received["profiles"]

    cleanedDevices = []
    clearnedProfiles = []
    for device in devices:
        cleanedDevices.append({
            "active": (device.get("GENERAL.STATE","not defined")  == "100 (connected)"),
            "name": device.get("GENERAL.DEVICE","not defined"),
            "ipAddress": device.get("IP4.ADDRESS[1]", "not defined"),
            "gateway": device.get("IP4.GATEWAY","not defined"),
            "profile": device.get("GENERAL.CONNECTION","not defined") 
        })
    for profile in profiles:
        clearnedProfiles.append({
            "id": profile.get("connection.uuid","not defined"),
            "active": (profile.get("GENERAL.STATE","not defined") == "activated"),
            "name": profile.get("connection.id","not defined"),
            "dhcp": (profile.get("ipv4.method","not defined") == "auto"),
            "ipAddress": profile.get("IP4.ADDRESS[1]","not defined"),
            "gateway": profile.get("IP4.GATEWAY", "not defined"),
            "device": profile.get("connection.interface-name","not defined")
        })

    return render_template("network.html", data={"devices": cleanedDevices, "profiles": clearnedProfiles})


############################################
###### APIs for Device Configurations ######
############################################

@app.route("/internal/<profile>/", methods=["POST"])
def setProfile(profile):
    data = request.json
    networkUrl = API_URL + "internal/" + profile + "/"
    networkReq = None
    try:
        networkReq = requests.post(
            networkUrl,
            headers={
                "Content-type": "application/json; charset=UTF-8"
            },
            data = data
        )
        networkReq.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        print("Http Error:",errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:",errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:",errt)
    except requests.exceptions.RequestException as err:
        print("OOps: Something Else",err)
    except:
        print("OK")

    return jsonify(success=True)

@app.route("/internal/<profile>/activate", methods=["POST"])
def activateProfile(profile):
    url = API_URL + "internal/" + profile + "/activate/"
    req = None
    try:
        req = requests.post(
            url,
            headers={"Content-type": "application/json; charset=UTF-8"}
        )
        req.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        print("Http Error:",errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:",errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:",errt)
    except requests.exceptions.RequestException as err:
        print("OOps: Something Else",err)
    except:
        print("OK")

    return jsonify(success=True)

@app.route("/internal/<profile>/deactivate", methods=["POST"])
def deactivateProfile(profile):
    url = API_URL + "internal/" + profile + "/deactivate/"
    req = None
    try:
        req = requests.post(
            url,
            headers={"Content-type": "application/json; charset=UTF-8"}
        )
        req.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        print("Http Error:",errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:",errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:",errt)
    except requests.exceptions.RequestException as err:
        print("OOps: Something Else",err)
    except:
        print("OK")

    return jsonify(success=True)