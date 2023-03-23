#!/bin/bash
echo "
                                                         
 __ __  _____  _____  _____    _____            _        
|  |  ||     ||  |  ||_   _|  | __  | ___  _ _ | |_  ___ 
|-   -|| | | ||  |  |  | |    |    -|| . || | ||  _|| -_|
|__|__||_|_|_||_____|  |_|    |__|__||___||___||_|  |___|
      厦门理工学院 无线路由配置Shell 
    Xiamen University of Technology Wireless Router Configuration Shell
                                                明理精工，与时偕行
"

# ISP PPPoE username
PPPoE_username=""
# Ruijie Certification username
Ruijie_username=""
# ISP PPPoE password
PPPoE_password=""
# Ruijie Certification password
Ruijie_password=""
# 2.4GHz SSID name
SSID2G=""
# 5GHz SSID name
SSID5G=""
# 2.4GHz Wi-Fi password
PWD2G=""
# 5GHz Wi-Fi password
PWD5G=""
# Random Mac Address
mac_addr="B6:2E:AF:B4:41:36"
# Network config file path
network_config="/etc/config/network"
# crontab file path
cron_config="/etc/crontabs/root"
# Find interface config start line number
interface_line_start=$(sed -n "/config interface 'wan'/=" "$network_config")
# Default interface config end line 0
interface_line_end=0

# Blank lines
line_feed=$(sed -n '/^$/=' /etc/config/network)

for ays in $line_feed
do
  if [ $ays -gt $interface_line_start ]
  then
    interface_line_end=$ays
    break
  fi
done

if [ $interface_line_end -eq 0 ]
then
  interface_line_end=$(sed -n '$=' "$network_config")
fi
device=$(sed -n "${interface_line_start},$ p" "$network_config" | sed -n "/option device '/{s///;s/'.*//;p;q}")
proto=$(sed -n "${interface_line_start},$ p" "$network_config" | sed -n "/option proto '/{s///;s/'.*//;p;q}")
echo "Original NIC interface: $device"
echo "Original network protocol: $proto"
if [ -z "$device" ]
then
  echo "Device not found"
  exit 1
fi

echo "network configuration..."
sed -i "$((interface_line_start+1)),${interface_line_end}d" "$network_config"
# Network configuration PPPoE
# PPPOE_proto
sed -i "/config interface 'wan'/a\ \toption proto 'pppoe'" "$network_config"
# PPPoE_NIC
sed -i "/config interface 'wan'/a\ \toption device '$device'" "$network_config"
echo "Successfully changed NIC interface: $device"
sed -i "/config interface 'wan'/a\ \toption macaddr '$mac_addr'" "$network_config"
echo "Successfully changed MAC address: $mac_addr"
# PPPoE_username
sed -i "/config interface 'wan'/a\ \toption username '$PPPoE_username'" "$network_config" 
# PPPoE_password
sed -i "/config interface 'wan'/a\ \toption password '$PPPoE_password'" "$network_config" 
sed -i "/config interface 'wan'/a\ \toption peerdns '1'" "$network_config"
sed -i "/config interface 'wan'/a\ \toption defaultroute '1'" "$network_config"
# echo display
echo "Successfully changed PPPoE protocol"


sed -i "/touch \/etc\/banner \&\& reboot/d" "$cron_config"
sed -i "\$a10 6 * * * sleep 70 && touch /etc/banner && reboot" "$cron_config"
echo "Successfully added automatic reboot task"

chmod a+x /bin/mentohust
mentohust -u"$Ruijie_username" -p"$Ruijie_password"  -a1 -d2 -b0 -n"$device" -w


# 2.4Ghz wireless
uci set wireless.@wifi-iface[0].mode=ap
uci set wireless.@wifi-iface[0].ssid="$SSID2G"
uci set wireless.@wifi-iface[0].network=lan
uci set wireless.@wifi-iface[0].encryption=psk2
uci set wireless.@wifi-iface[0].key="$PWD2G"

echo "Successfully changed 2.4Ghz SSID & PASSWORD"
# 5Ghz wireless
uci set wireless.@wifi-iface[1].mode=ap
uci set wireless.@wifi-iface[1].ssid="$SSID5G"
uci set wireless.@wifi-iface[1].network=lan
uci set wireless.@wifi-iface[1].encryption=psk2
uci set wireless.@wifi-iface[1].key="$PWD5G"
echo "Successfully changed 5Ghz SSID & PASSWORD"
# save config
uci commit
echo "Network reboot in progress"
/etc/init.d/network restart
echo "Network reboot successful"

echo "Configuration complete"
echo "----------------------------------------------------------"
echo "Please save the following information in case you need it."
echo "Your Ruijie Info"
echo "  username: $Ruijie_username | password: $Ruijie_password"
echo "Your ISP PPPoE Info" 
echo "  username: $PPPoE_username | Password: $PPPoE_password"
echo "Your Wi-Fi Info"
echo "  2.4Ghz: $SSID2G | Password: $PWD2G"
echo "  5Ghz: $SSID5G | Password: $PWD2G"
echo "----------------------------------------------------------"
