from typing import Annotated

from mcp.server import MCPServer
from mcp.server.mcpserver import Context
from mcp.types import ToolAnnotations
from pydantic import Field

from app.discount import DiscountResult, calculate_discount_value

mcp = MCPServer(
    name="python-discount-stdio",
    title="Python 折扣计算 MCP Server（stdio）",
    version="1.0.0",
    instructions="使用 calculate_discount 计算商品折扣、优惠金额与最终应付金额。",
)


@mcp.tool(
    name="calculate_discount",
    title="折扣计算器",
    description="根据商品原价、折扣百分比和数量，计算优惠金额与应付金额。",
    annotations=ToolAnnotations(read_only_hint=True, open_world_hint=False),
    structured_output=True,
)
async def calculate_discount(
    original_price: Annotated[
        float,
        Field(ge=0, allow_inf_nan=False, description="商品原始单价，必须大于或等于 0。"),
    ],
    discount_percent: Annotated[
        float,
        Field(ge=0, le=100, allow_inf_nan=False, description="优惠百分比，例如 20 表示减免 20%。"),
    ],
    ctx: Context,
    quantity: Annotated[int, Field(ge=1, description="购买数量。")] = 1,
    currency: Annotated[
        str,
        Field(pattern=r"^[A-Z]{3}$", description="ISO 4217 三位大写货币代码。"),
    ] = "CNY",
    precision: Annotated[int, Field(ge=0, le=4, description="金额保留的小数位数。")] = 2,
) -> DiscountResult:
    await ctx.report_progress(progress=1, total=1, message="折扣计算完成")
    return calculate_discount_value(original_price, discount_percent, quantity, currency, precision)


def main() -> None:
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()

