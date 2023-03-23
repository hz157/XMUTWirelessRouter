# openwrt 编译

## 操作步骤
1. clone openwrt 到本地
``` shell
git clone https://github.com/openwrt/openwrt.git
```
2. 编辑配置
``` shell
make menuconfig
```
此处需要修改芯片型号、设备型号并生成配置文件(.config)只需修改下述三处。<br>
- Target System (芯片厂商)
- Subtarget （芯片型号）
- Target Profile （设备型号）
3. 编译 
``` shell
./scripts/feeds update -a
./scripts/feeds install -a
make V=99
```

## 常见问题
1. 编译速度特别慢
> 解决方案参考 [doc\slow_compilation_zh.md](doc\slow_compilation_zh.md)
