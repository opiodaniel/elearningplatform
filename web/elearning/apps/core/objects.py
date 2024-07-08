from .sql import SQL
import sys
from django.apps import apps
# from ..corporatevaluation.models import XBRLCompanyInfo, ETFWatchLists, XBRLSPStatistics


class SystemMaintenance(object):
    def __init__(self):
        pass

    def get_database_info(self, dic):
        # print("9055 \n")
        # print(dic)
        # print("90551")
        try:
            db_name = dic["db_name"]
            sql = SQL()
            s_query = "SELECT pg_size_pretty( pg_database_size('"+db_name+"'))"
            # print(s_query)
            results = sql.exc_sql(s_query, [], verb='select')
            results = {"status": "ok", "s_query": s_query, "db_size": results[0][0]}
        except Exception as ex:
            results = {"status": "error: "+str(ex), "s_query": s_query, "db_size": -1}
        return results

    def get_table_info(self, dic):
        # print("9060")
        # print(dic)
        # print("90601")
        try:
            app_name = dic["app_name"]
            table_name = dic["table_name"]
            model = apps.get_model(app_label=app_name, model_name=table_name)
            m = model()
            table_size = sys.getsizeof(m) * model.objects.count()
            table_size = str(round(table_size/1000000, 2))+" MB"
            results = {"status": "ok", "table_size": table_size}
        except Exception as ex:
            results = {"status": "error: "+str(ex), "table_size": table_size}
        return results

    def create_sp500_group(self, dic):
        # print("9075")
        spc, c = ETFWatchLists.objects.get_or_create(symbol="SP500")
        if c:
            spc.description = "SP500"
            spc.save()
        sps = XBRLSPStatistics.objects.all()
        for s in sps:
            try:
                c = XBRLCompanyInfo.objects.get(ticker=s.company.ticker)
                c.etfwatchlist = spc
                c.save()
                # print("--done--", s.company.ticker, s.company.company_name)
                results = {"status": "ok"}
            except Exception as ex:
                # print(str(ex))
                results = {"status": "error: " + str(ex)}
        return results

