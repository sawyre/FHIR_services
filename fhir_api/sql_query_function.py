import requests


RECOURCE_ID_NUM_DB = 1
RECOURCE_COLUMN_NUM_DB = 5
SEARCH_RESOURCE_SERVER = "https://hisgateway.herokuapp.com/panel/his_requests/"

def _get_resource_by_id(resource_type, id):
    """
    resource_type - маленькими буквами
    id - число
    """
    sql_search_query = 'select * from {} where txid={}'.format(resource_type, id)
    query_dict = {'query': sql_search_query}
    print(query_dict)
    ans = requests.post(SEARCH_RESOURCE_SERVER, headers={'Content-type': 'application/json'}, json=query_dict)
    return ans.json()[0][RECOURCE_COLUMN_NUM_DB]

def _get_resources_by_dict(resource_type, fhir_resource_dict):
    """
    resource_type - маленькими буквами
    fhir_resource_dict - параметры, по которым нужно искать
    """
    json_text = str(fhir_resource_dict).replace("\'", "\"")
    query  = 'SELECT * FROM {} WHERE (resource @> \'{}\'::jsonb)'.format(resource_type, json_text)
    query_dict = {'query': query}
    print(query_dict)
    ans = requests.post(SEARCH_RESOURCE_SERVER, headers={'Content-type': 'application/json'}, json=query_dict)
    
    resources_dict = dict(zip([item[RECOURCE_ID_NUM_DB] for item in ans.json()], [item[RECOURCE_COLUMN_NUM_DB] for item in ans.json()]))
    return resources_dict