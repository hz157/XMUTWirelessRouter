# 网卡名称问题
<p align="left">🇨🇳 中文简体  |  <a title="English" href="nic_name.md">🇬🇧 English</a></p>

由于openwrt有众多衍生版本，各类版本的/etc/config/network配置有细微上的差别，因此需提前查看所使用的openwrt版本所使用的网卡名称是device还是ifname.

使用以下命名查看系统采用ifname亦或是device作为网卡名称
``` bash
cat /etc/config/network
```

## 样例
- openWrt by Kiddin' 版本采用**device**作为网卡名称
![device](/doc/images/20230323184122.png)

- Lede版本的openwrt 采用**ifname**作为网卡名称
![ifname](/doc/images/20230323184122.png)
