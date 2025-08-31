from src.config.simulation_setting_config import gen_simulation_config

# 分组比较操作符列表
GROUP_COMPARE_OP = ['group_rank', 'group_zscore', 'group_neutralize']

# 时间序列比较操作符列表
TS_COMPARE_OP = ['ts_rank', 'ts_zscore', 'ts_av_diff']

# 时间枚举
TIME_ENUM = ['60', '200']

# 分组依据枚举
GROUP_BY = ['industry', 'subindustry', 'market', 'sector', 'densify(pv13_h_f1_sector)']


def gen_template(
        company_fundamentals,
        group_compare_op=None,
        ts_compare_op=None,
        days=None,
        group=None
):
    """
    生成alpha表达式模板

    参数:
        :param company_fundamentals: 公司基本面数据的字段列表
        :param group_compare_op: 分组比较操作符列表
        :param ts_compare_op: 时间序列比较操作符列表
        :param days: 时间周期列表
        :param group: 分组依据列表
    """

    group_compare_op = group_compare_op if group_compare_op else GROUP_COMPARE_OP
    ts_compare_op = ts_compare_op if ts_compare_op else TS_COMPARE_OP
    days = days if days else TIME_ENUM
    group = group if group else GROUP_BY

    alpha_expressions = []
    # 遍历分组比较操作符
    for gco in group_compare_op:
        # 遍历时间序列比较操作符
        for tco in ts_compare_op:
            # 遍历公司基本面数据的字段
            for cf in company_fundamentals:
                # 遍历时间周期
                for d in days:
                    # 遍历分组依据
                    for grp in group:
                        # 生成alpha表达式并添加到列表中
                        alpha_expressions.append(f"{gco}({tco}({cf}, {d}), {grp})")

    print(f"there are total {len(alpha_expressions)} alpha expressions, the first 5 are:{alpha_expressions[:5]}")

    alpha_list = []

    for index, alpha in enumerate(alpha_expressions, start=1):
        alpha_list.append(gen_simulation_config(alpha))

    return alpha_list
