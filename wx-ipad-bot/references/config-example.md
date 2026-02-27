# 配置文件示例

## 登录状态配置

### login_state.json (自动生成)
登录成功后自动生成，用于保存登录状态，下次可快速重连。

```json
{
  "itchat_login_state": {
    "username": "wxid_xxxxxxxxxxxxx",
    "key": "xxxxxxxxxxxx",
    "device_id": "xxxxxxxxxxxx"
  }
}
```

**说明:**
- 此文件由程序自动生成和管理
- 包含登录凭据和设备信息
- 位置: 项目根目录或指定路径
- 建议定期更新以保持登录状态

## 自定义配置模板

### bot_config.json (可选)
用户可以创建自定义配置文件来管理机器人行为。

```json
{
  "login": {
    "state_file": "login_state.json",
    "auto_login": true
  },
  "message": {
    "auto_reply": true,
    "reply_delay": 2,
    "max_retries": 3
  },
  "filters": {
    "blacklist": ["user1", "user2"],
    "whitelist": [],
    "keywords": ["广告", "推广"]
  },
  "group_management": {
    "enabled": true,
    "auto_welcome": true,
    "welcome_message": "欢迎加入群组！"
  },
  "logging": {
    "enabled": true,
    "log_file": "bot.log",
    "log_level": "INFO"
  }
}
```

**配置项说明:**

### login (登录配置)
- `state_file`: 登录状态文件路径
- `auto_login`: 是否自动登录

### message (消息配置)
- `auto_reply`: 是否启用自动回复
- `reply_delay`: 回复延迟（秒）
- `max_retries`: 发送失败重试次数

### filters (过滤配置)
- `blacklist`: 黑名单（不处理这些用户的消息）
- `whitelist`: 白名单（仅处理这些用户的消息）
- `keywords`: 关键词过滤

### group_management (群组管理配置)
- `enabled`: 是否启用群组管理
- `auto_welcome`: 是否自动欢迎新成员
- `welcome_message`: 欢迎消息内容

### logging (日志配置)
- `enabled`: 是否启用日志
- `log_file`: 日志文件路径
- `log_level`: 日志级别 (DEBUG/INFO/WARNING/ERROR)

## 使用示例

### 示例1: 基本配置
```python
import json

# 加载配置
with open('bot_config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

# 根据配置初始化机器人
bot = WeChatBot(login_state_file=config['login']['state_file'])

# 登录
if config['login']['auto_login']:
    bot.login()
```

### 示例2: 消息过滤
```python
config = load_config('bot_config.json')

def handle_message(msg):
    # 检查黑名单
    if msg['FromUserName'] in config['filters']['blacklist']:
        return
    
    # 检查关键词过滤
    for keyword in config['filters']['keywords']:
        if keyword in msg['Content']:
            print(f"检测到敏感词: {keyword}")
            return
    
    # 处理正常消息
    process_message(msg)
```

### 示例3: 群组欢迎
```python
config = load_config('bot_config.json')

def handle_group_message(msg):
    if not config['group_management']['enabled']:
        return
    
    # 检测新成员加入
    if '加入了群聊' in msg['Content']:
        if config['group_management']['auto_welcome']:
            welcome_msg = config['group_management']['welcome_message']
            send_message(msg['FromUserName'], welcome_msg)
```

## 环境变量配置

### 使用环境变量配置敏感信息
```bash
# Linux/Mac
export WECHAT_BOT_CONFIG="/path/to/bot_config.json"
export WECHAT_BOT_LOG_LEVEL="INFO"

# Windows
set WECHAT_BOT_CONFIG=C:\path\to\bot_config.json
set WECHAT_BOT_LOG_LEVEL=INFO
```

**在代码中读取环境变量:**
```python
import os

config_path = os.getenv('WECHAT_BOT_CONFIG', 'bot_config.json')
log_level = os.getenv('WECHAT_BOT_LOG_LEVEL', 'INFO')
```

## 注意事项

1. **安全性**: 配置文件可能包含敏感信息，请妥善保管
2. **备份**: 定期备份配置文件和登录状态文件
3. **权限**: 确保程序对配置文件有读写权限
4. **编码**: 配置文件建议使用 UTF-8 编码
5. **格式**: JSON 格式必须正确，注意逗号和引号

## 配置验证

### 验证配置文件的正确性
```python
import json

def validate_config(config_path):
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # 检查必需字段
        required_fields = ['login', 'message', 'filters']
        for field in required_fields:
            if field not in config:
                print(f"缺少必需字段: {field}")
                return False
        
        print("配置文件验证通过")
        return True
        
    except json.JSONDecodeError as e:
        print(f"JSON 格式错误: {e}")
        return False
    except FileNotFoundError:
        print("配置文件不存在")
        return False
```
