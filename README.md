# UniversalGameAgent

UniversalGameAgent 是一个面向手游与桌面游戏自动化的插件化框架，统一抽象了 runtime、vision、state、planner 与 workflow 五层能力，目标是支持跨游戏、跨平台以及后续 AI 化扩展。

## 当前实现范围

第一阶段聚焦《剑与远征经典服》手游的日常任务：

- 登录游戏
- 收取邮件
- 领取日常奖励
- 领取挂机奖励

当前版本以骨架搭建优先，重点是把主执行链路先跑通：

- runtime 接口已经稳定
- 已提供 ADB runtime 雏形
- workflow 执行链路可运行
- 已接入 AFK Arena 的插件层定义
- 视觉检测与页面识别层当前仍为可替换占位实现

## 项目结构

```text
src/universal_game_agent/
  core/
  games/
  planner/
  state/
  vision/
  workflow/
```

## 快速开始

本项目当前推荐调试链路：

```text
云端 Linux agent
  -> Tailscale 组网
  -> Windows 电脑
  -> Windows ADB server
  -> 雷电模拟器
```

### 本地 stub 模式

用于验证 workflow 主链路，不需要 Android 设备：

```bash
PYTHONPATH=src python3 -m universal_game_agent.main --game afk_arena --workflow daily
```

### 普通 Android ADB 模式

用于 Linux 能直接看到 Android 设备或模拟器的场景：

```bash
PYTHONPATH=src python3 -m universal_game_agent.main \
  --game afk_arena \
  --workflow daily \
  --platform adb \
  --device-id emulator-5554
```

### Windows 雷电模拟器远程 ADB 模式

用于当前开发环境：项目 agent 在云端 Linux，模拟器运行在 Windows。

Linux 侧已完成：

- 已安装 `adb`
- 已安装并启动 Tailscale
- Linux Tailscale IPv4：`100.113.242.69`
- 项目已支持远程 ADB server 参数：
  - `--adb-host`
  - `--adb-port`
- 已新增 ADB 自检入口：
  - `python3 -m universal_game_agent.adb_doctor`

Windows 侧准备：

1. 安装 Tailscale 并登录同一个账号。
2. 获取 Windows 的 Tailscale IPv4：

```powershell
tailscale ip -4
```

3. 测试 Windows 到 Linux 的组网连通性：

```powershell
tailscale ping 100.113.242.69
```

4. 启动雷电模拟器，建议先固定为横屏 `1280x720`。
5. 找到雷电模拟器目录下的 `adb.exe`，常见路径：

```text
C:\LDPlayer\LDPlayer9\adb.exe
D:\leidian\LDPlayer9\adb.exe
```

6. 在 `adb.exe` 所在目录打开 PowerShell，确认模拟器设备：

```powershell
.\adb.exe devices -l
```

如果没有设备，尝试连接雷电本地 ADB 端口：

```powershell
.\adb.exe connect 127.0.0.1:5555
.\adb.exe devices -l
```

多开实例可继续尝试：

```powershell
.\adb.exe connect 127.0.0.1:5557
.\adb.exe connect 127.0.0.1:5559
.\adb.exe devices -l
```

7. 启动一个对 Tailscale 网络可访问的 Windows ADB server：

```powershell
.\adb.exe kill-server
.\adb.exe -a -P 5037 nodaemon server
```

保持这个 PowerShell 窗口开启。

Linux 侧验证设备列表：

```bash
adb -H <WINDOWS_TAILSCALE_IP> -P 5037 devices -l
```

运行 ADB 自检，确认设备状态、分辨率、DPI，并抓取截图：

```bash
PYTHONPATH=src python3 -m universal_game_agent.adb_doctor \
  --adb-host <WINDOWS_TAILSCALE_IP> \
  --adb-port 5037 \
  --device-id <DEVICE_ID>
```

预期会生成：

```text
artifacts/adb_doctor.png
```

确认自检通过后运行 workflow：

```bash
PYTHONPATH=src python3 -m universal_game_agent.main \
  --game afk_arena \
  --workflow daily \
  --platform adb \
  --adb-host <WINDOWS_TAILSCALE_IP> \
  --adb-port 5037 \
  --device-id <DEVICE_ID>
```

完整操作文档见：

```text
docs/ldplayer_remote_adb_setup.md
```

## 当前已完成内容

- runtime 抽象：截图、点击、滑动、输入文本
- Stub runtime：用于本地 dry-run 验证
- ADB runtime：支持本机 ADB 与远程 ADB server
- ADB doctor：用于验证远程 ADB 连接、设备信息与截图能力
- Tailscale 组网方案：用于云端 Linux 连接 Windows 雷电模拟器
- workflow loader：可加载 AFK Arena 日常流程
- rule planner：按步骤顺序执行任务
- 游戏插件层：将页面与按钮配置从执行器中解耦

## 下一步仍缺少的内容

- Windows 雷电模拟器端的 ADB 连通性确认
- OCR 与模板识别素材
- 《剑与远征经典服》页面与按钮样本集
- 更安全的账号输入与登录策略
- 面向不同分辨率的坐标映射配置
- 未知弹窗与异常页面的兜底处理

## 你需要提供的信息

- 设备类型：安卓真机或模拟器
- 期望的控制方式：ADB、模拟器 API，还是 Windows 投屏控制
- 屏幕分辨率与宽高比
- 日常任务相关页面截图
- 游戏 UI 使用语言
- 登录方式：免登录、账号密码、扫码，或其他方式
- 第一阶段是否需要支持多账号轮换

## 下一阶段开发建议

建议优先完成以下工作：

1. 在 Windows 上启动雷电模拟器和远程 ADB server。
2. 从 Linux 运行 `adb_doctor`，确认截图、分辨率和设备状态。
3. 收集《剑与远征经典服》关键页面截图。
4. 建立页面识别规则与按钮检测素材。
5. 增加未知页面停止、超时退出、手动暂停等安全控制。
6. 在单账号稳定后，再扩展多账号与 dashboard。
