# NIC Name Problem
<p align="left">🇬🇧 English  |  <a title="English" href="nic_name_zh.md">🇨🇳 中文简体</a></p>

As there are many versions of openwrt, the configuration of /etc/config/network differs slightly from one version to another, so check in advance whether the name of the NIC used in the version of openwrt you are using is device or ifname.

Use the following naming convention to check whether the system uses ifname or device as the name of the network card
``` bash
cat /etc/config/network
```

## Example
- openwrt by Kiddin' Use **device** as the NIC name
![device](/doc/images/20230323184122.png)

- openwrt Lede Use **ifname** as the NIC name
![ifname](/doc/images/20230323184122.png)
