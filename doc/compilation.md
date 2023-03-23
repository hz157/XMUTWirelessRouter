# openwrt compilation
<p align="left">🇬🇧 English  |  <a title="English" href="compilation_zh.md">🇨🇳 中文简体</a></p>

## Steps
1. Clone openwrt to local
```bash
git clone https://github.com/openwrt/openwrt.git
```
2. Edit configuration
```bash
Make menuconfig
```
Here you need to modify the chip model, device model and generate the configuration file (.config) only need to modify the following three places. <br>
- Target system (chip vendor)
- subtarget (chip model)
- Target data (device model)
3. Compilation
```shell
./scripts/feeds update -a
./scripts/feeds install -a
Make V=99
```

## common problem
1. The compilation speed is extremely slow
> Solution reference [doc\slow_compilation_zh.md](slow_compilation_zh.md)
