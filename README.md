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

以本地 stub 模式运行：

```bash
$env:PYTHONPATH='src'; python -m universal_game_agent.main --game afk_arena --workflow daily
```

以 Android ADB 模式运行：

```bash
$env:PYTHONPATH='src'; python -m universal_game_agent.main --game afk_arena --workflow daily --platform adb --device-id emulator-5554
```

## 当前已完成内容

- runtime 抽象：截图、点击、滑动、输入文本
- Stub runtime：用于本地 dry-run 验证
- ADB runtime 雏形：用于后续真机或模拟器接入
- workflow loader：可加载 AFK Arena 日常流程
- rule planner：按步骤顺序执行任务
- 游戏插件层：将页面与按钮配置从执行器中解耦

## 接入真机前仍缺少的内容

- 完整的 Android ADB 联调
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

1. 接入真实 ADB 截图与点击能力
2. 收集《剑与远征经典服》关键页面截图
3. 建立页面识别规则与按钮检测素材
4. 增加未知页面停止、超时退出、手动暂停等安全控制
5. 在单账号稳定后，再扩展多账号与 dashboard
