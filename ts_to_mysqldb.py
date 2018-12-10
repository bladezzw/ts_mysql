import time
from ts_mysql import * #获取包的全局参数
from ts_mysql import tushare_api as ts_api
from ts_mysql import mysql_api as ms_api
import threading
from  multiprocessing import Process,Pool


"""
该模块用来将tushare的数据插入mysql
"""
# from sqlalchemy import create_engine
# import tushare as ts
#
# df = ts.get_tick_data('600848', date='2014-12-22')
# engine = create_engine('mysql://user:passwd@127.0.0.1/db_name?charset=utf8')
#
# #存入数据库
# df.to_sql('tick_data',engine)
#
# #追加数据到现有表
# #df.to_sql('tick_data',engine,if_exists='append')



def mysql_sql(table_name = '',keys='',value=[]):
    """
    :param table_name: str
    :param keys: list
    :param value: list  在tushare中是df.iloc[i],df的某一列
    :return:
    """
    sql = "insert into {tab_name}{keys} values {values};" \
        .format(tab_name=table_name, keys=keys, values=tuple(value))
    return sql

#%% insert data into mysql
def insert_df2mysql(df,table=''): 
    """
    :param df:DataFrame with columns'name
    :param table: str,table_name of your databases(default:'stock_market')
    This will be collected into a class (mysql_insert) in the future
    """
    conn = pymysql.connect(host=host,port=port,user=user,passwd=passwd,db=db)
    cursor = conn.cursor()
    col_name = list(df.columns)#column titles of data
    col_name.extend(['create_date'])#add keys: 'create_date' ,'last_update_date'
    #table_name's formation like '(ts_code, symbol, name, area, industry, market, list_date)'
    date = time.strftime('%Y-%m-%d')
    keys = str(tuple(col_name)).replace("'",'')
    for i in range(len(df)):
        #will be updated to a efficient way!
        temp = list(df.iloc[i])
        temp.extend([date])
        sql = mysql_sql(table ,keys, value = temp)
        #value may be None,
        #print(sql)
        cursor.execute(sql)
        conn.commit()
        #print(int(i*100/len(symbol)),'%')
#    print('finish!')
    cursor.close()
    conn.close()

def insert_alldaily2mysql1(symbols=[]):
    """
    This could use the threading method,will be modifed in the future.
    but,may cause discontinuous daily
    """
    print('Start all !')
    for i in range(len(symbols)):
        try:
            insert_df2mysql(ts_api.get_1stock_daily_dataInTushare(ts_code=symbols[i]),'daily')
        except Exception as ee:
            print(ee)
            print('something wrong with stock: {}'.format(symbols[i]))
#        if i%200 == 199:
#            time.sleep(60)
        print(i,'%d %'%(int(i*100/len(symbols))))
    print('Finish all!')

def get_and_insert1data2mysql(symbol='',start_date='20180101',end_date = now_,table = ''):
    try:
        df = ts_api.get_1stock_daily_dataInTushare(symbol,start_date=start_date,end_date=now_)
        insert_df2mysql(df, table=table)
    except Exception as ee:
        print(ee)

def insert_alldaily2mysql(symbols=[],start_date='20180101',end_date = now_,table = ''):
    """
    插入symbol对应的股票进入
    """
    if table:
        thre = []
        semaphore = threading.Semaphore(4)
        for i in range(len(symbols)):
            thre.append(threading.Thread(target=get_and_insert1data2mysql,args=(symbols.iloc[i],start_date,end_date,table,)))
        for t in thre:
            t.start()
            print('thread %s start!'%t)

if __name__ == '__main__':
    print("ts_mysql_module".center(20,'-'))
    ##
    #
    # ddf = ts_api.get_symbolIntushare()
    # # print(ddf.iloc[:,1].iloc[0:16])
    # symbols = ddf.iloc[:, 1].iloc[0:16]
    # print(symbols)
    # print('start threading ')
    # insert_alldaily2mysql(symbols = symbols,table='daily')

    # #insert symbols into mysqldb's table
    # #1.get all symbols
    # df = ts_api.get_symbolIntushare()
    # #2.insert into mysql
    # insert_df2mysql(df,'symbol')

    ##the line below is to insert a daily data of a certain stock
    # get_and_insert1data2mysql(symbol='000001.SZ',table='daily')


    ##多线程实现insert all daily of all stocks recorded in mysql
    # ddf = ms_api.get_allSymbolInMysql()
    # symbols = ddf[:10]
    #
    # thre = []
    #
    # semaphore = threading.Semaphore(16)
    # for i in range(len(symbols)):
    #     thre.append(
    #         threading.Thread(target=get_and_insert1data2mysql, args=(symbols[i],'19900101', now_, 'daily',)))
    # for t in thre:
    #     t.start()
    #     print('thread %s start!' % t)

    ##多进程实现insert all daily of all stocks recorded in mysql
    ddf = ms_api.get_allSymbolInMysql()
    symbols = ddf[:10]
    thre = []
    pool = Pool()
    for i in range(len(symbols)):
        pool.apply_async(func=get_and_insert1data2mysql, args=(symbols[i],'19900101', now_, 'daily',))

    pool.close()
    pool.join()         # join与close调用顺序是固定的

    print('end')


    ##串行实现insert all daily of all stocks recorded in mysql
    # ddf = ms_api.get_allSymbolInMysql()
    # symbols = ddf[0:4]
    # insert_alldaily2mysql1(symbols)




    

    
    


