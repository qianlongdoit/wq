def gen_template(fields):
    group_compare_op = ['group_rank', 'group_zscore', 'group_neutralize']  # 分组比较操作符列表
    # 定义时间序列比较操作符
    ts_compare_op = ['ts_rank', 'ts_zscore', 'ts_av_diff']  # 时间序列比较操作符列表
    # 定义公司基本面数据的字段列表
    company_fundamentals = fields
    # 定义时间周期列表
    days = [60, 200]
    # 定义分组依据列表
    group = ['market', 'industry', 'subindustry', 'sector', 'densify(pv13_h_f1_sector)']
    # 初始化alpha表达式列表
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

    print(f"there are total {len(alpha_expressions)} alpha expressions")

    alpha_list = []

    for index, alpha in enumerate(alpha_expressions, start=1):
        simulation_data = {
            "type": "REGULAR",
            "settings": {
                "instrumentType": "EQUITY",
                "region": "USA",
                "universe": "TOP3000",
                "delay": 1,
                "decay": 0,
                "neutralization": "SUBINDUSTRY",
                "truncation": 0.01,
                "pasteurization": "ON",
                "unitHandling": "VERIFY",
                "nanHandling": "OFF",
                "language": "FASTEXPR",
                "visualization": False,
            },
            "regular": alpha
        }

        alpha_list.append(alpha)

    return alpha_list