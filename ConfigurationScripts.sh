#!/bin/bash
PPPoE_username="17689202223"
Ruijie_username="2012120134"
PPPoE_password="112321"
Ruijie_password="123456"
SSID2G="Abc123"
SSID5G="Abc123"
PWD2G="12345678"
PWD5G="12345678"
mac_addr="5f:47:03:1d:b0:05"
network_config="/etc/config/network"
cron_config="/etc/crontabs/root"
interface_line_start=$(sed -n "/config interface 'wan'/=" "$network_config")
interface_line_end=0


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
device=$(sed -n "${interface_line_start},$ p" "$network_config" | sed -n "/option ifname '/{s///;s/'.*//;p;q}")
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

sed -i "/config interface 'wan'/a\ \toption proto 'pppoe'" "$network_config"
sed -i "/config interface 'wan'/a\ \toption ifname '$device'" "$network_config"
echo "Successfully changed NIC interface: $device"
sed -i "/config interface 'wan'/a\ \toption macaddr '$mac_addr'" "$network_config"
echo "Successfully changed MAC address: $mac_addr"
sed -i "/config interface 'wan'/a\ \toption username '$PPPoE_username'" "$network_config" 
sed -i "/config interface 'wan'/a\ \toption password '$PPPoE_password'" "$network_config" 
sed -i "/config interface 'wan'/a\ \toption peerdns '1'" "$network_config"
sed -i "/config interface 'wan'/a\ \toption defaultroute '1'" "$network_config"
echo "Successfully changed PPPoE protocol"


sed -i "/touch \/etc\/banner \&\& reboot/d" "$cron_config"
sed -i "\$a10 6 * * * sleep 70 && touch /etc/banner && reboot" "$cron_config"
echo "Successfully added automatic reboot task"

chmod a+x /bin/mentohust
mentohust -u"$Ruijie_username" -p"$Ruijie_password"  -a1 -d2 -b0 -n"$device" -w


uci set wireless.@wifi-device[0].disabled=0
uci set wireless.@wifi-device[0].txpower=17
uci set wireless.@wifi-device[0].channel=6
uci set wireless.@wifi-iface[0].mode=ap
uci set wireless.@wifi-iface[0].ssid="$SSID2G"
uci set wireless.@wifi-iface[0].network=lan
uci set wireless.@wifi-iface[0].encryption=psk2
uci set wireless.@wifi-iface[0].key="$PWD2G"

echo "Successfully changed 2.4Ghz SSID & PASSWORD"
uci set wireless.@wifi-device[1].disabled=0
uci set wireless.@wifi-device[1].txpower=17
uci set wireless.@wifi-device[1].channel=6
uci set wireless.@wifi-iface[1].mode=ap
uci set wireless.@wifi-iface[1].ssid="$SSID5G"
uci set wireless.@wifi-iface[1].network=lan
uci set wireless.@wifi-iface[1].encryption=psk2
uci set wireless.@wifi-iface[1].key="$PWD5G"
echo "Successfully changed 5Ghz SSID & PASSWORD"
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
        