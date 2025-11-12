from flask import Flask, jsonify, request

import scripts.internal as host

api = Flask(__name__)

############################################
###### APIs for Device Configurations ######
############################################

#######################################################
########## MANAGE NetworkManger CONNECTIONS ###########
@api.route("/internal/network/", methods=["GET"])
def getNetwork():
    devices = host.getDevices()
    deviceDetails = []
    for device in devices:
        deviceDetails.append(host.getDevice(device["name"]))

    profiles = host.getProfiles()
    profileDetails = []
    for profile in profiles:
        profileDetails.append(host.getProfile(profile["name"]))
    
    return jsonify(success=True, devices=deviceDetails, profiles=profileDetails)

# modifies the connection profile
@api.route("/internal/<profile>/", methods=["POST"])
def setProfile(profile):
    data = request.json
    newName = data.get("name")
    newIP = data.get("ip")
    newGateway = data.get("gateway")
    newInterface = data.get("interface")
    
    args = ["con-name", newName, "ipv4.address", newIP, "ipv4.gateway", newGateway, "ifname", newInterface]
    return jsonify(host.modifyProfile(profile, args))

# activates a profile
@api.route("/internal/<profile>/activate/", methods=["POST"])
def activateProfile(profile):
    return jsonify(host.activateProfile(profile))

# deactivates a profile
@api.route("/internal/<profile>/deactivate/", methods=["POST"])
def deactivateProfile(profile):
    return jsonify(host.deactivateProfile(profile))


###################################################
########## MANAGE NetworkManger DEVICES ###########
@api.route("/internal/devices/", methods=["GET"])
def getDevices():
    return {}
