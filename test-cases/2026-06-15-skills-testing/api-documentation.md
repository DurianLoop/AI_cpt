# API 使用指南：天气查询服务

## 快速开始

### 认证

所有 API 请求需要在 header 中包含 API Key：

```bash
Authorization: Bearer YOUR_API_KEY
```

获取 API Key：登录控制台 → 设置 → API 密钥

---

## 端点

### 1. 获取当前天气

**请求**：
```http
GET /api/v1/weather/current?city={city}&lang={lang}
```

**参数**：
| 参数 | 类型 | 必填 | 说明 | 示例 |
|------|------|------|------|------|
| city | string | 是 | 城市名称 | Beijing |
| lang | string | 否 | 语言代码（默认：en） | zh, en, ja |
| units | string | 否 | 单位（默认：metric） | metric, imperial |

**响应**：
```json
{
  "status": "success",
  "data": {
    "city": "Beijing",
    "country": "CN",
    "timestamp": "2024-06-15T10:30:00Z",
    "temperature": 28.5,
    "feels_like": 30.2,
    "humidity": 65,
    "wind_speed": 12.5,
    "conditions": "partly_cloudy",
    "description": "多云"
  }
}
```

**示例代码**：

Python:
```python
import requests

url = "https://api.weather-service.com/api/v1/weather/current"
headers = {"Authorization": "Bearer YOUR_API_KEY"}
params = {"city": "Beijing", "lang": "zh"}

response = requests.get(url, headers=headers, params=params)
data = response.json()

print(f"当前温度: {data['data']['temperature']}°C")
```

JavaScript:
```javascript
const response = await fetch(
  'https://api.weather-service.com/api/v1/weather/current?city=Beijing&lang=zh',
  {
    headers: {
      'Authorization': 'Bearer YOUR_API_KEY'
    }
  }
);

const data = await response.json();
console.log(`当前温度: ${data.data.temperature}°C`);
```

---

### 2. 获取未来天气预报

**请求**：
```http
GET /api/v1/weather/forecast?city={city}&days={days}
```

**参数**：
| 参数 | 类型 | 必填 | 说明 | 范围 |
|------|------|------|------|------|
| city | string | 是 | 城市名称 | - |
| days | integer | 否 | 预报天数（默认：7） | 1-14 |

**响应**：
```json
{
  "status": "success",
  "data": {
    "city": "Beijing",
    "forecasts": [
      {
        "date": "2024-06-16",
        "temp_high": 32,
        "temp_low": 22,
        "conditions": "sunny",
        "precipitation_chance": 10
      },
      {
        "date": "2024-06-17",
        "temp_high": 30,
        "temp_low": 21,
        "conditions": "rainy",
        "precipitation_chance": 80
      }
    ]
  }
}
```

---

### 3. 批量查询

**请求**：
```http
POST /api/v1/weather/batch
Content-Type: application/json
```

**请求体**：
```json
{
  "cities": ["Beijing", "Shanghai", "Guangzhou"],
  "lang": "zh"
}
```

**响应**：
```json
{
  "status": "success",
  "data": [
    {
      "city": "Beijing",
      "temperature": 28.5,
      "conditions": "partly_cloudy"
    },
    {
      "city": "Shanghai",
      "temperature": 26.0,
      "conditions": "rainy"
    },
    {
      "city": "Guangzhou",
      "temperature": 32.0,
      "conditions": "sunny"
    }
  ]
}
```

---

## 错误处理

所有错误响应遵循以下格式：

```json
{
  "status": "error",
  "error": {
    "code": "INVALID_CITY",
    "message": "城市名称无效",
    "details": "City 'Beijng' not found. Did you mean 'Beijing'?"
  }
}
```

**常见错误代码**：

| 代码 | 说明 | 解决方案 |
|------|------|----------|
| INVALID_API_KEY | API Key 无效 | 检查 API Key 是否正确 |
| RATE_LIMIT_EXCEEDED | 超过速率限制 | 降低请求频率或升级套餐 |
| INVALID_CITY | 城市不存在 | 检查城市名称拼写 |
| MISSING_PARAMETER | 缺少必填参数 | 查看参数要求 |

---

## 速率限制

| 套餐 | 每分钟请求数 | 每日请求数 |
|------|-------------|-----------|
| 免费 | 10 | 1,000 |
| 基础 | 60 | 10,000 |
| 专业 | 300 | 100,000 |

超出限制后会返回 `429 Too Many Requests`。

响应头包含限制信息：
```
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 42
X-RateLimit-Reset: 1623456789
```

---

## SDK

### Python SDK

安装：
```bash
pip install weather-service-sdk
```

使用：
```python
from weather_service import WeatherClient

client = WeatherClient(api_key="YOUR_API_KEY")

# 获取当前天气
weather = client.current("Beijing", lang="zh")
print(f"温度: {weather.temperature}°C")

# 获取预报
forecast = client.forecast("Shanghai", days=5)
for day in forecast:
    print(f"{day.date}: {day.temp_high}°C")
```

### JavaScript SDK

安装：
```bash
npm install @weather-service/sdk
```

使用：
```javascript
import { WeatherClient } from '@weather-service/sdk';

const client = new WeatherClient({ apiKey: 'YOUR_API_KEY' });

// 获取当前天气
const weather = await client.current('Beijing', { lang: 'zh' });
console.log(`温度: ${weather.temperature}°C`);

// 获取预报
const forecast = await client.forecast('Shanghai', { days: 5 });
forecast.forEach(day => {
  console.log(`${day.date}: ${day.tempHigh}°C`);
});
```

---

## 最佳实践

### 1. 缓存响应
天气数据通常每小时更新一次，建议缓存结果：

```python
import time

cache = {}
CACHE_TTL = 3600  # 1 小时

def get_weather_cached(city):
    now = time.time()
    if city in cache and now - cache[city]['time'] < CACHE_TTL:
        return cache[city]['data']
    
    data = client.current(city)
    cache[city] = {'data': data, 'time': now}
    return data
```

### 2. 错误重试
网络问题时自动重试：

```python
import time
from requests.exceptions import RequestException

def get_weather_with_retry(city, max_retries=3):
    for attempt in range(max_retries):
        try:
            return client.current(city)
        except RequestException as e:
            if attempt == max_retries - 1:
                raise
            time.sleep(2 ** attempt)  # 指数退避
```

### 3. 批量优化
需要多个城市数据时使用批量接口：

```python
# ❌ 不推荐：多次单独请求
cities = ["Beijing", "Shanghai", "Guangzhou"]
for city in cities:
    weather = client.current(city)

# ✅ 推荐：批量请求
weather_data = client.batch(cities)
```

---

## 更新日志

### v1.2.0 (2024-06-01)
- ✨ 新增批量查询接口
- 🐛 修复时区处理问题
- 📈 性能提升 30%

### v1.1.0 (2024-05-01)
- ✨ 支持 14 天预报
- 🌍 新增多语言支持
- 📖 完善文档

---

## 支持

- 📧 Email: support@weather-service.com
- 💬 Discord: discord.gg/weather-service
- 📚 文档: docs.weather-service.com
- 🐛 问题反馈: github.com/weather-service/issues
