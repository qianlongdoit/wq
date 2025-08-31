# 简单模板
# "group_rank(roe, industry)"
SIMPLE_TEMPLATE = "{group_op}{factor}, group"

# 时间序列模板
# "ts_zscore(revenue, 60)"
TIME_SERIES_TEMPLATE = "{ts_op}{factor}, window"

# 复合策略
# "group_neutralize(ts_zscore(ebitda, 25), subindustry)"
COMPOSITE_TEMPLATE = "{group_op}{ts_op}{factor}, {widow}, {group}"

# 比率策略
# "group_rank(ebitda/enterprise_value, industry)"
RATIO_TEMPLATE = "{group_op}{factor1}/{factor2}, {group}"

# 多因子策略
# "group_neutralize(rank(roe) + rank(roa), subindustry)"
MULTI_FACTOR_TEMPLATE = "{group_op}(rank(factor1) + rank(factor2), {group})"

# 时间序列比率策略
# "group_neutralize(ts_zscore(rank(ebitda)/rank(enterprise_value), 10), industry)"
TIME_SERIES_RATIO_TEMPLATE = "{group_op}{ts_op}(rank({factor1})/rank({factor2}), {window}), {group}"
