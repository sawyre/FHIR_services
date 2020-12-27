def sql_query_by_id(resource_type, id):
    query = 'select * from {} where txid={}'.format(resource_type, id)
    return query

def sql_query_by_dict(resource_type, fhir_resource_dict):
    pass