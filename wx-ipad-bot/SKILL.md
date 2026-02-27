---
name: wx-ipad-bot
description: 基于iPad协议的微信机器人，支持自动消息收发、联系人管理、群组操作和智能对话
dependency:
  python:
    - itchat-uos>=1.5.0.dev0
    - requests>=2.28.0
---

# 微信 iPad 协议机器人

## 任务目标
- 本 Skill 用于: 自动化微信消息处理、联系人管理、群组交互
- 能力包含: 消息收发、智能回复、好友管理、群组操作
- 触发条件: 用户需要进行微信自动化操作或构建聊天机器人

## 前置准备
- 依赖说明: 需要安装 itchat-uos 库（itchat 的增强版，专门修复 iPad 协议兼容性）和 requests 库
  ```bash
  pip install itchat-uos>=1.5.0.dev0 requests>=2.28.0
  ```
  **说明**: itchat-uos 是 itchat 的社区维护版本，修复了 iPad 协议的兼容性问题，支持最新的微信版本
- 非标准文件/文件夹准备: 无需额外准备

## 操作步骤
- 标准流程:
  1. 登录微信
     - 执行 `python scripts/wechat_bot.py login`
     - 扫描二维码登录微信账号
     - 登录成功后会保存登录状态
  2. 接收和处理消息
     - 智能体持续监控消息队列
     - 根据消息内容分析用户意图
     - 调用脚本或直接生成回复
  3. 发送消息
     - 调用 `scripts/wechat_bot.py send --to <好友ID> --message <内容>`
     - 支持文本、图片等多种格式
  4. 管理联系人和群组
     - 调用脚本获取好友列表、群组信息
     - 智能体根据管理策略执行操作

- 可选分支:
  - 当 启用自动回复模式: 智能体根据关键词或语义自动回复
  - 当 启用群组管理: 执行群消息推送、群成员管理等操作

## 资源索引
- 必要脚本: 见 [scripts/wechat_bot.py](scripts/wechat_bot.py)(用途与参数: 实现微信登录、消息收发、联系人管理)
- 领域参考: 见 [references/api-guide.md](references/api-guide.md)(何时读取: 查看API接口和参数说明)
- 输出资产: 见 [references/config-example.md](references/config-example.md)(直接用于生成/修饰输出: 配置文件模板)

## 注意事项
- 仅在需要时读取参考，保持上下文简洁。
- **使用 itchat-uos**: 本 Skill 使用 itchat-uos 库，这是 itchat 的增强版本，专门修复了 iPad 协议的兼容性问题
- iPad协议登录可能触发微信安全检测，建议小频率使用。
- 智能体负责消息理解和内容生成，脚本负责技术实现。
- 避免高频发送消息，防止账号被封禁。

## 使用示例

### 示例1: 登录并发送消息
```bash
# 登录
python scripts/wechat_bot.py login

# 使用昵称/备注名发送消息
python scripts/wechat_bot.py send --to "好友备注名" --message "你好，这是一条测试消息"

# 使用微信ID发送消息（直接定位，不查找昵称）
python scripts/wechat_bot.py send --to "wxid_xxxxxxxxxxxxx" --use-id --message "通过ID发送的消息"
```

### 示例2: 获取好友列表
```bash
python scripts/wechat_bot.py get_friends
```

### 示例3: 智能对话模式
```python
# 在SKILL内部由智能体调用脚本
messages = get_messages()  # 获取未读消息
for msg in messages:
    reply = generate_response(msg.content)  # 智能体生成回复
    send_message(msg.sender, reply)
```

### 示例4: 群组操作
```bash
# 发送群消息
python scripts/wechat_bot.py send_group --group "群名称" --message "群公告"

# 获取群成员
python scripts/wechat_bot.py get_group_members --group "群名称"
```
