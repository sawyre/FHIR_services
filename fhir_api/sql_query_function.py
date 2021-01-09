import requests
import json

from utility.constants import SEARCH_RESOURCE_SERVER

RECOURCE_ID_NUM_DB = 0
RECOURCE_COLUMN_NUM_DB = 5


def _get_resource_by_id(resource_type, id):
    """
    resource_type - маленькими буквами
    id - число
    """
    sql_search_query = 'select * from {} where id=\'{}\';'.format(resource_type, id)
    query_dict = {'query': sql_search_query}
    print(query_dict)
    ans = requests.post(SEARCH_RESOURCE_SERVER, headers={'Content-type': 'application/json'}, json=query_dict)
    return json.loads(ans.json()['success'][0][RECOURCE_COLUMN_NUM_DB])

def _get_resources_by_dict(resource_type, fhir_resource_dict):
    """
    resource_type - маленькими буквами
    fhir_resource_dict - параметры, по которым нужно искать
    """
    json_text = str(fhir_resource_dict).replace("\'", "\"")
    query  = 'SELECT * FROM {} WHERE (resource @> \'{}\'::jsonb);'.format(resource_type, json_text)
    query_dict = {'query': query}
    print(query_dict)
    ans = requests.post(SEARCH_RESOURCE_SERVER, headers={'Content-type': 'application/json'}, json=query_dict)
    data = ans.json()['success']
    if type(data[0]) == str:
        resources_dict = {data[RECOURCE_ID_NUM_DB]: data[RECOURCE_COLUMN_NUM_DB]}
    else:
        resources_dict = dict(zip([item[RECOURCE_ID_NUM_DB] for item in ans.json()['success']], [json.loads(item[RECOURCE_COLUMN_NUM_DB]) for item in ans.json()['success']]))
    return resources_dict