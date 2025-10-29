


# WHITELIST = {
#     "network.addInterface": ,
#     "network.modifyInterface":,
#     "nework."
#     "network.restart": lambda body: ["/usr/sbin/service", "networking", "restart"],
#     "wifi.set-ssid": set_ssid_args,
# }

# class WifiBody(BaseModel):
#     ssid: constr(strip_whitespace=True, min_length=1, max_length=32)
#     channel: conint(ge=1, le=165)

# TASKS = {}

def run_cmd(argv, timeout=20):
    # No shell, bounded env, capture output
    res = subprocess.run(argv, capture_output=True, timeout=timeout, check=False, env={"PATH":"/usr/sbin:/usr/bin"})
    return {"code": res.returncode, "stdout": res.stdout.decode(), "stderr": res.stderr.decode()}

# Example whitelist: verb -> executable + arg builder
def set_ssid_args(body):  # validate and map to argv
    return ["/usr/sbin/wifi_tool", "set-ssid", body.ssid, "--channel", str(body.channel)]

# lsusb | grep -i net
# nmcli device

# sudo nmcli connection add type ethernet ifname eth0 con-name dhcp-eth0 \
#   ipv4.method auto \
#   autoconnect yes

# sudo nmcli connection add type ethernet ifname eth0 con-name static-eth0 \
#   ipv4.addresses 192.168.1.100/24 \
#   ipv4.gateway 192.168.1.1 \
#   ipv4.dns 8.8.8.8 \
#   ipv4.method manual \
#   autoconnect yes