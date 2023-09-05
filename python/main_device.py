#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2023-03-23
@author: hz157
remarks: 网卡采用device声明的版本
"""

import paramiko
import random
import os
from scp import SCPClient

# Router Params Info
config = {
      'host': '192.168.99.1',
      'port': 22,
      'username': 'root',
      'password': 'password'
}

PPPoE = {"username": "", "password": ""}
Ruijie = {"username": "", "password": ""}
SSID_2G = {"SSID": "", "password": ""}
SSID_5G = {"SSID": "", "password": ""}

mentohust_path = 'files\mentohust-master\mentohust'

shell = None


def randomMAC():
    """
        随机MAC生成
    """
    mac = [random.randint(0x00, 0x7f), 
           random.randint(0x00, 0x7f), 
           random.randint(0x00, 0x7f), 
           random.randint(0x00, 0x7f), 
           random.randint(0x00, 0xff), 
           random.randint(0x00, 0xff)]
    return ':'.join(map(lambda x: "%02x" % x, mac))


def setInfo():
    """
        用户参数设定
    """
    global PPPoE,Ruijie,SSID_2G,SSID_5G
    PPPoE['username'] = input("请输入ISP提供的PPPoE拨号用户名(一般为手机号): ")
    PPPoE['password'] = input("请输入ISP提供的PPPoE拨号密码: ")
    Ruijie['username'] = input("请输入锐捷认证用户名(学号): ")
    Ruijie['password'] = input("请输入锐捷认证密码: ")
    SSID_2G['SSID'] = input("请输入无线网络名称(不建议使用中文): ")
    SSID_2G["password"] = input("请输入无线网络密码(不可低于8位字符): ")
    while len(SSID_2G["password"]) < 8:
        SSID_2G["password"] = input("请重新输入无线网络密码(不可低于8位字符): ")
    flag = input("是否区分2.4GHz与5GHz的Wi-Fi信号(Y/N): ")
    while len(flag) != 1:
        flag = input("是否区分2.4GHz与5GHz的Wi-Fi信号(Y/N): ")
    if len(flag) == 1:
        if str.lower(flag) == "y":
            SSID_5G['SSID'] = input("请输入5GHz无线网络名称(不建议使用中文): ")
            while SSID_5G['SSID'] == SSID_2G['SSID']:
                SSID_5G['SSID'] = input("5GHz无线网络名称与2.4G相同，请重新输入(不建议使用中文): ")
            SSID_5G['password'] = input("请输入5GHz无线网络密码: ")
            while len(SSID_5G["password"]) < 8:
                SSID_5G["password"] = input("请重新输入5GHz无线网络密码(不可低于8位字符): ")
        else:
            SSID_5G = SSID_2G


def createShell():
    """
        生成shell文件
    """
    global shell
    param = f"""#!/bin/bash
PPPoE_username="{PPPoE['username']}"
Ruijie_username="{Ruijie['username']}"
PPPoE_password="{PPPoE['password']}"
Ruijie_password="{Ruijie['password']}"
SSID2G="{SSID_2G['SSID']}"
SSID5G="{SSID_5G['SSID']}"
PWD2G="{SSID_2G['password']}"
PWD5G="{SSID_5G['password']}"
mac_addr="{randomMAC()}"
network_config="/etc/config/network"
cron_config="/etc/crontabs/root"
interface_line_start=$(sed -n "/config interface 'wan'/=" "$network_config")
interface_line_end=0


line_feed=$(sed -n '/^$/=' /etc/config/network)
        """ + r"""
        
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

sed -i "/config interface 'wan'/a\ \toption proto 'pppoe'" "$network_config"
sed -i "/config interface 'wan'/a\ \toption device '$device'" "$network_config"
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
        """
    # 判断文件是否存在
    # if not os.path.exists(r'files/ConfigurationScripts.sh'):
    #     os.mknod(r'files/ConfigurationScripts.sh')  # 创建文件
    # 写入脚本
    with open(os.path.join(os.getcwd(), 'ConfigurationScripts.sh'), "w",encoding="utf-8") as f:
        f.write(param)
    shell = param


def upload():
    try:
        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(
            hostname = config['host'],
            port = config['port'],
            username = config['username'],
            password = config['password']
        )
        stdin,stdout,stderr = ssh.exec_command('chmod a+x /bin/mentohust')
        scp = SCPClient(ssh.get_transport())
        scp.put(mentohust_path, recursive=True, remote_path='/bin/mentohust')
        scp.close()
        print('file upload success')
        ssh.close()
        return True
    except Exception as e:
        print(f'file upload error. Error content: {e}')
        return False


def secureShell():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(
        hostname = config['host'],
        port = config['port'],
        username = config['username'],
        password = config['password']
    )
    stdin,stdout,stderr = ssh.exec_command(shell)    #   远程执行命令
    # 按字节返回结果
    result = stdout.read().decode()
    print(result)
    stdin,stdout,stderr = ssh.exec_command("mentohust")    #   远程执行命令
    result = stdout.read().decode()
    if 'Configuration complete' in result:
        print('Success')
    else:
        print('error?')
    ssh.close()


if __name__ == '__main__':
    print("""
                                                                 
 __ __  _____  _____  _____    _____            _        
|  |  ||     ||  |  ||_   _|  | __  | ___  _ _ | |_  ___ 
|-   -|| | | ||  |  |  | |    |    -|| . || | ||  _|| -_|
|__|__||_|_|_||_____|  |_|    |__|__||___||___||_|  |___|
    Xiamen University of Technology Wireless Router Configuration Shell
                                                明理精工，与时偕行
    """)
    setInfo()   # 配置用户信息
    createShell()   # 生成shell文件
    # flag = input('是否需要上传MentoHUST插件(Y/N): ')
    flag = "n"
    if str.lower(flag) == "y":
        if upload():
            secureShell()
        else:
            print('plug upload error, please reset program. ')
    else:
        secureShell()
