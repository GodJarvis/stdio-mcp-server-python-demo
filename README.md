# Python stdio MCP Server Demo

使用 Python 3.11+ 和官方 `mcp` Python SDK 实现的标准 stdio MCP Server，以 `calculate_discount` 折扣计算工具为例。

stdio 是子进程标准流传输，不存在 HTTP 请求生命周期，因此它不由 FastAPI 承载；对应的 Streamable HTTP 项目使用 FastAPI 挂载同一类 MCP 工具。stdio 项目与 HTTP 项目都使用 Pydantic 生成并校验输入、输出 JSON Schema。

## 安装与启动

```bash
uv sync --dev
uv run python -m app.server
```

启动后没有普通控制台输出，服务端正在等待客户端通过 stdin 发送 MCP 消息。stdout 只用于协议数据，日志写入 stderr。

## MCP 客户端配置

```json
{
  "mcpServers": {
    "discount-stdio-python": {
      "command": "uv",
      "args": [
        "--directory",
        "/home/zw/vibe-demo/stdio-mcp-server-python-demo",
        "run",
        "python",
        "-m",
        "app.server"
      ]
    }
  }
}
```

## 工具参数

| 参数 | 类型 | 必填 | 约束 |
|---|---:|---:|---|
| `original_price` | number | 是 | 大于或等于 0 |
| `discount_percent` | number | 是 | 0～100 |
| `quantity` | integer | 否 | 大于或等于 1，默认 1 |
| `currency` | string | 否 | 三位大写货币代码，默认 `CNY` |
| `precision` | integer | 否 | 0～4，默认 2 |

金额使用 `ROUND_HALF_UP`，并按“先舍入单件折后价，再乘数量”的规则计算。

## 验证

```bash
uv run ruff check .
uv run pytest
uv run python scripts/e2e_client.py
```

