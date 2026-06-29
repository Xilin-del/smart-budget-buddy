import os
from typing import Dict, List


def call_llm(text):
    """调用大模型接口，优先读取环境变量中的 API Key。"""
    try:
        from openai import OpenAI
    except ImportError as error:
        raise ImportError(
            "未安装 openai 依赖，请先执行 `pip install openai --break-system-packages`"
        ) from error

    api_key = os.getenv(
        "BUDGET_AGENT_API_KEY",
        "sk-46764d377c524e6c9d7072da25043f01"
    )
    client = OpenAI(
        api_key=api_key,
        base_url="https://llm-obplvr9av8e9nmwz.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
    )
    completion = client.chat.completions.create(
        model="qwen-plus",
        messages=[
            {"role": "user", "content": text}
        ]
    )
    return completion.choices[0].message.content


def _format_category_lines(items: List[Dict], value_key: str, empty_text: str) -> str:
    if not items:
        return empty_text

    lines = []
    for item in items:
        value = item.get(value_key, 0)
        if isinstance(value, float):
            value = round(value, 2)
        lines.append(
            f"- {item.get('label', '未知')}: {value}"
        )
    return "\n".join(lines)


def build_financial_prompt(username: str, analysis_type: str, snapshot: Dict) -> str:
    """将账单摘要整理成适合 LLM 分析的提示词。"""
    top_expense_categories = _format_category_lines(
        snapshot.get("top_expense_categories", []),
        "amount",
        "暂无分类支出数据"
    )
    monthly_expense_trend = _format_category_lines(
        snapshot.get("monthly_expense_trend", []),
        "amount",
        "暂无月度趋势数据"
    )
    recent_records = _format_category_lines(
        snapshot.get("recent_records", []),
        "display",
        "暂无近期记录"
    )
    largest_expenses = _format_category_lines(
        snapshot.get("largest_expenses", []),
        "display",
        "暂无大额支出记录"
    )

    base_info = f"""
你是一个中文财务分析 AI 助手，请基于用户的个人记账数据进行分析。

用户：{username}
账单总数：{snapshot.get("record_count", 0)}
时间范围：{snapshot.get("date_range", "暂无数据")}
总收入：{snapshot.get("total_income", 0)}
总支出：{snapshot.get("total_expense", 0)}
当前结余：{snapshot.get("current_balance", 0)}
平均单笔支出：{snapshot.get("avg_expense", 0)}
平均单笔收入：{snapshot.get("avg_income", 0)}
最大单笔支出：{snapshot.get("max_expense", 0)}
最近 30 天支出：{snapshot.get("recent_30d_expense", 0)}
最近 30 天收入：{snapshot.get("recent_30d_income", 0)}

支出分类 Top5：
{top_expense_categories}

月度支出趋势：
{monthly_expense_trend}

最近 8 条流水：
{recent_records}

最大 5 笔支出：
{largest_expenses}
""".strip()

    if analysis_type == "summary":
        instruction = """
请输出：
1. 总体消费概览
2. 消费结构总结
3. 最近消费行为观察
4. 一句简短结论

要求：
- 使用中文
- 语言清晰、像给普通用户解释
- 不要编造没有提供的数据
- 控制在 250 字以内
""".strip()
    elif analysis_type == "advice":
        instruction = """
请输出：
1. 当前资金使用状态判断
2. 2 到 4 条具体可执行的资金建议
3. 需要重点关注的消费类别

要求：
- 使用中文
- 建议要结合结余、近期支出和分类支出
- 优先给出节流、预算和风险提醒
- 控制在 300 字以内
""".strip()
    else:
        instruction = """
请输出：
1. 消费历史中的主要模式
2. 月度趋势或阶段性变化
3. 大额支出与消费偏好分析
4. 后续记账与复盘建议

要求：
- 使用中文
- 结合时间趋势和近期记录
- 不要编造不存在的月份或类别
- 控制在 320 字以内
""".strip()

    return f"{base_info}\n\n{instruction}"


def generate_financial_analysis(username: str, analysis_type: str, snapshot: Dict) -> str:
    """生成财务 AI 分析结果。"""
    if snapshot.get("record_count", 0) == 0:
        return "当前还没有账单记录，先添加几笔收入或支出后，我再帮你做消费总结和资金建议。"

    prompt = build_financial_prompt(username, analysis_type, snapshot)
    return call_llm(prompt)
