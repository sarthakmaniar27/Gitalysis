from CassandraHelper import Utils as utils
from CassandraHelper import config
from multiprocessing import Pool
from ElasticSearchHelper import ElasticSearchHelper as esh

class CassandraUserData():
    def __init__(self, elasticUserData):
        dataList = elasticUserData['hits']['hits']
        self.data = list()
        threadPool = Pool(config.THREAD_COUNT)
        self.data = threadPool.map(self.processDataList, dataList)
        print("Done CassandraRepoData")
        # for i in range(len(dataList)):
        #     self.data.append(self.processDataList(dataList[i]))

    def processDataList(self, userDataItem):
        return userDataItem['_source']