import pandas as pd
from .sign_in import sign_in


SEARCH_SCOPE = {
    'region': 'USA',
    'delay': '1',
    'universe': 'TOP3000',
    'instrumentType': 'EQUITY'
}


def get_data_fields(
        dataset_id: str = '',
        session=None,
        search_scope=None,
        search: str = ''
):
    """
    获取所有满足条件的数据字段及其ID

    参数:
        session: 会话对象session
        search_scope: 搜索范围
        dataset_id: 数据集ID
        search: 搜索关键字
    """
    if session is None:
        session = sign_in()

    if search_scope is None:
        search_scope = SEARCH_SCOPE

    instrument_type = search_scope['instrumentType']
    region = search_scope['region']
    delay = search_scope['delay']
    universe = search_scope['universe']

    if len(search) == 0:
        url_template = "https://api.worldquantbrain.com/data-fields?" + \
                       f"&instrumentType={instrument_type}" + \
                       f"&region={region}&delay={str(delay)}&universe={universe}&dataset.id={dataset_id}&limit=50" + \
                       "&offset={x}"
        count = session.get(url_template.format(x=0)).json()['count']
    else:
        url_template = "https://api.worldquantbrain.com/data-fields?" + \
                       f"&instrumentType={instrument_type}" + \
                       f"&region={region}&delay={str(delay)}&universe={universe}&limit=50" + \
                       f"&search={search}" + \
                       "&offset={x}"
        count = 100

    datafields_list = []
    for x in range(0, count, 50):
        datafields = session.get(url_template.format(x=x))
        datafields_list.append(datafields.json()['results'])

    datafields_list_flat = [item for sublist in datafields_list for item in sublist]

    datafields_df = pd.DataFrame(datafields_list_flat)
    return datafields_df
