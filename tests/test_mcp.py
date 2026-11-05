import pytest
from mcp import Client

from app.server import mcp


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture
async def client():
    async with Client(mcp, raise_exceptions=True) as connected_client:
        yield connected_client


@pytest.mark.anyio
async def test_tool_schema(client: Client) -> None:
    listed = await client.list_tools()

    assert len(listed.tools) == 1
    tool = listed.tools[0]
    assert tool.name == "calculate_discount"
    assert tool.input_schema["properties"]["discount_percent"]["maximum"] == 100
    assert tool.output_schema is not None
    assert "total_payable" in tool.output_schema["properties"]


@pytest.mark.anyio
async def test_call_discount_tool(client: Client) -> None:
    result = await client.call_tool(
        "calculate_discount",
        {"original_price": 100, "discount_percent": 20, "quantity": 3},
    )

    assert result.is_error is False
    assert result.structured_content is not None
    assert result.structured_content["total_discount_amount"] == 60.0
    assert result.structured_content["total_payable"] == 240.0


@pytest.mark.anyio
async def test_invalid_discount_is_tool_error(client: Client) -> None:
    result = await client.call_tool(
        "calculate_discount",
        {"original_price": 100, "discount_percent": 101},
    )

    assert result.is_error is True
    assert result.structured_content is None

