class CassandraOrgData():
    def __init__(self, elasticOrgData):
        data = elasticOrgData['hits']['hits'][0]['_source']
        self.data = data