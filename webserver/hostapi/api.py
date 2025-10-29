from flask import Flask, jsonify
import subprocess

api = Flask(__name__)

############################################
###### APIs for Device Configurations ######
############################################

# Set the current radio network
# Reconfigure the attached radio
# Change network priority?

@api.route("/internal/getInterfaces/", methods=["GET"])
def getInterfaces():
    print("TEST")
    res = subprocess.run("ifconfig", capture_output=True,check=False, env={"PATH":"/usr/sbin:/usr/bin"})
    print(res)
    return jsonify(success=True, code=res.returncode, stdout=res.stdout.decode(), stderr=res.stderr.decode())


# @app.route("/uas/announceStreamEnd/<nodeID>/<pathName>", methods=["GET"])
# def announceStreamEnd(nodeID, pathName):
#     return {}
