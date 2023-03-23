# Slow compilation of openwrt
> 建议使用gitee来加快编译的速度

https://gitee.com/harvey520/openwrt.git <br>
该仓库每天自动从官方源拉取更新一次，不会存在更新不及时问题
1. clone Source Code 到本地
``` shell
git clone https://gitee.com/harvey520/openwrt.git
```
2. 修改 feeds.conf.default
修改 openwrt 源码目录的 feeds.conf.default 文件中的镜像源
- 将 https://git.openwrt.org/feed/packages.git 改为 https://gitee.com/harvey520/packages.git
- 将 https://git.openwrt.org/project/luci.git 改为 https://gitee.com/harvey520/luci.git
- 将 https://git.openwrt.org/feed/routing.git 改为 https://gitee.com/harvey520/routing.git
- 将 https://git.openwrt.org/feed/telephony.git 改为 https://gitee.com/harvey520/telephony.git

1. 进入 openwrt 源码目录中，执行以下命令
``` shell
git clone https://e.coding.net/yao7778899/openwrt-dependent-dl.git dl
```
