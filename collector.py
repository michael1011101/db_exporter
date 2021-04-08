from prometheus_client import core

class BaseController(object):

    def __init__(self, queryConfig, client):
        self.queryConfig = queryConfig
        self.mysql_client = client
    
    def _scrape(self, query_cmd, db_conn, metrics, queryItem=None):
        with db_conn.cursor() as cursor:
            cursor.execute(query_cmd)
            columns = [column[0] for column in cursor.description]
            # fetch all solution
            raw_response = cursor.fetchall()

            for item in queryItem.load_metrics(raw_response, columns):
                yield item

    def collect(self):
        if self.queryConfig.enable:
            with self.mysql_client.connection() as db_conn:
                for queryConfigItem in self.queryConfig.queryConfigItems:
                    query_cmd = queryConfigItem.query
                    metrics = queryConfigItem.metrics
                    for obj in self._scrape(query_cmd, db_conn, metrics, queryConfigItem):
                        yield obj