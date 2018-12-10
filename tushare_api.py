from ts_mysql import *
from ts_mysql import data_preparation as dp #数据预处理
#tushare上下载的数据为pandas.DataFrame格式

pro = ts.pro_api()

#该模块用来获取tushare的数据

def initial_token():
    """set your token"""
    ts.set_token('22db94abb1e9f6b56883665e737d1600d064260591a351c98809c8ae')

#%% get data from tushare
def get_symbolIntushare():
    """从tushare上得到基本股票列表及信息"""
    code = pro.stock_basic()
    return dp.none2str(code,'Null')

def get_index(market=''):
    """
    obtain the Index of certain market
    市场代码 	说明
    MSCI 	MSCI指数
    CSI 	中证指数
    SSE 	上交所指数
    SZSE 	深交所指数
    CICC 	中金所指数
    SW 	申万指数
    CNI 	国证指数
    OTH 	其他指数
    """
    df = pro.index_basic(market = market)
    return dp.none2str(df,'Null')

def get_1stock_daily_data(ts_code='',start_date='19900101',end_date=now_):
    """
    :param ts_code:str
    :param trade_date\end_date:str yyyymmdd
    """
#    if not end_date:
#        end_date = time.strftime('%Y%m%d')
#    if not start_date:
#        start_date='19990101'
    df = pro.daily(ts_code=ts_code,start_date=start_date,end_date=end_date)
    d = df.drop(['change'],axis=1)#change is mysql key word,cant use
    return d

def get_1stock_daily_dataInTushare(ts_code='',start_date='19900101',end_date=now_):
    """
    :param ts_code:str
    :param trade_date\end_date:str yyyymmdd
    """
#    if not end_date:
#        end_date = time.strftime('%Y%m%d')
#    if not start_date:
#        start_date='19990101'
    df = pro.daily(ts_code=ts_code,start_date=start_date,end_date=end_date)
    d = df.drop(['change'],axis=1)
    return d

if __name__ == '__main__':
    print("tushare_api module".center(20,'-'))
    #initial_token()  # inidal token to get access

    #get daily data of '000001.SZ' from '20180101' to '20181126'
    df = get_1stock_daily_data(ts_code='000001.SZ',start_date='20180101',end_date='20181126')
    print(df)

