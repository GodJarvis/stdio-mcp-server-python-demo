import anyio
from mcp import Client, StdioServerParameters


async def main() -> None:
    server = StdioServerParameters(command="uv", args=["run", "python", "-m", "app.server"])
    async with Client(server) as client:
        tools = await client.list_tools()
        assert [tool.name for tool in tools.tools] == ["calculate_discount"]

        result = await client.call_tool(
            "calculate_discount",
            {"original_price": 199.9, "discount_percent": 15, "quantity": 2},
        )
        assert result.is_error is False
        assert result.structured_content is not None
        assert result.structured_content["total_payable"] == 339.84
        print(result.structured_content)


if __name__ == "__main__":
    anyio.run(main)

