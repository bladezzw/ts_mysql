import pandas as pd

#data_preparation数据预处理

def none2str(df,table_type):
    """
    change none to 'replace_str'
    :param data: DataFrame
    :replace_str: str char that you wanna to replace none
    This will be involved into a class ('data_preparation') in the future
    """
    bool_value = pd.isnull(df)
    df[bool_value]=table_type
    return df

if __name__ == '__main__':
    print("data_preparation_module".center(20,'-'))