import json
import pandas as pd
from io import StringIO
import string, random

def random_str(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def get_columns_and_types_for_dataset(dataset):
    
    datas = json.loads(dataset.get_science_data())
    ret = []
    for name, val in datas['variables'].items():
        ret.append({"name": name, "type": val['type']['__Variable__']})

    return ret;

def get_db_engine():
    import sqlalchemy
    return sqlalchemy.create_engine('postgresql://postgres:dVre445Vsd@analytics-platform.ml/public')

def exec_in_pg(sql):
    #return ""
    con = get_db_engine()
    return con.execute(sql)

def build_sql_for_dataset(table_name, dataset):
    eng = get_db_engine()
    
    string_handle = StringIO(dataset.get_content().decode())
    df = pd.read_csv(string_handle)
    ddl = pd.io.sql.get_schema(df.reset_index(), table_name, con=eng)

    inserts = []
    # inserts
    for index, row in df.iterrows():
        columns = '"' + '", "'.join(df.columns) + '"'
        values = str(tuple(row.values))
        #values = values.replace("nan", '"nan"')
        values = values.replace("nan", 'null')
        
        inserts.append('INSERT INTO '+ table_name+' ('+ columns + ') VALUES '+ values)        

    return ddl+";" + ";\n".join(inserts)
