from flask import Flask, jsonify, request
from flask import render_template
import requests

import scripts.internal as host

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
    devices = host.getDevices()
    deviceDetails = []
    for device in devices:
        deviceDetails.append(host.getDevice(device["name"]))

    profiles = host.getProfiles()
    profileDetails = []
    for profile in profiles:
        profileDetails.append(host.getProfile(profile["name"]))

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
    newName = data.get("name")
    newIP = data.get("ip")
    newGateway = data.get("gateway")
    newInterface = data.get("interface")
    
    args = ["con-name", newName, "ipv4.address", newIP, "ipv4.gateway", newGateway, "ifname", newInterface]
    return jsonify(host.modifyProfile(profile, args))

@app.route("/internal/<profile>/activate", methods=["POST"])
def activateProfile(profile):
    return jsonify(host.activateProfile(profile))

@app.route("/internal/<profile>/deactivate", methods=["POST"])
def deactivateProfile(profile):
    return jsonify(host.deactivateProfile(profile))