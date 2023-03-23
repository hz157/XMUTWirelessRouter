# 厦门理工学院 无线路由
<p align="left">🇨🇳 中文简体  |  <a title="English" href="README.md">🇬🇧 English</a></p>


> 使用[openwrt-lede](https://github.com/coolsnowwolf/lede)和[mentohust](https://github.com/tkkcc/mentohust)开发。

使用该方法需要具有一些的计算机方面的知识以及一定的动手能力。

## 下载
- [python 源代码](https://github.com/hz157/XMUTWirelessRouter/tree/python)
- [shell_script (ifname)](https://github.com/hz157/XMUTWirelessRouter/blob/script/script/shell_ifname.sh)
- [shell_script (device)](https://github.com/hz157/XMUTWirelessRouter/blob/script/script/shell_device.sh)

## 介绍
该方法采用openwrt作为路由的系统，使用中科大学生所开发的MentoHUST进行锐捷认证。<br>
So, 使用该方法前，你需要有下述的设备及账号
- 一台支持openwrt刷机的无线路由器 [支持列表](https://github.com/hz157/XMUTWirelessRouter/blob/doc/doc/support_openwrt_list.md)
- 你的学生账号（**校园锐捷账号仅限单台设备登录，校园内的无线账号与锐捷认证账号是分离的不受影响**）

如果你刚好拥有以上两样，恭喜你，很快就可以享用到宿舍无线的快乐了。

### 脚本语言
- Python 3.10 & higher
- Shell

### 支持芯片 

这主要取决于你的芯片是否支持openwrt。

[芯片支持列表](https://github.com/hz157/XMUTWirelessRouter/blob/doc/doc/support_chip_list.md) (持续更新)

**提示： 对于其他芯片，请手动编译固件**。


### 经过验证的设备
[已经过验证可用设备列表](https://github.com/hz157/XMUTWirelessRouter/blob/doc/doc/validated_products.md)

请帮助完成型号列表，您可以告诉我们该方法支持哪些设备。



## FAQ
1. [固件编译速度慢](https://github.com/hz157/XMUTWirelessRouter/blob/doc/doc/slow_compilation_zh.md)
2. [网卡名称问题](https://github.com/hz157/XMUTWirelessRouter/blob/doc/doc/nic_name_zh.md)

## LICENSE
  **[GNU GENERAL PUBLIC LICENSE Version 3](LICENSE)**
