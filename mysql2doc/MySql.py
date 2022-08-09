import sys
import traceback
from urllib.parse import quote

from sqlalchemy import create_engine

from mysql2doc.TableData import *
from mysql2doc.config import dbConfigMap


class MySql:
    def __init__(self):
        super().__init__()
        dburl = "mysql+pymysql://{userName}:%s@{host}:{port}/{databaseName}?charset={charset}".format(
            **dbConfigMap
        ) % quote(dbConfigMap['password'])
        self.engine = create_engine(dburl)

    def showTables(self):
        return [ele[0] for ele in self.engine.execute('show tables')]

    def tableDetail(self, tableName):
        fields = []
        for fieldRow in self.engine.execute('show full columns from ' + tableName):
            field = Field()
            field.name = fieldRow['Field']
            field.type = str(fieldRow['Type']).lower()
            field.nullable = fieldRow['Null']
            field.nullable = 'Y' if fieldRow['Null'] == 'YES' else 'N'
            field.isPK = 'Y' if fieldRow['Key'] == 'PRI' else 'N'
            field.comment = fieldRow['Comment']
            field.default = fieldRow['Default']
            field.extra = fieldRow['Extra']
            fields.append(field)
        tableComment = ''
        for ele in self.engine.execute('show table status where name="' + tableName + '"'):
            tableComment = ele['Comment']
        indices = []
        for idx in self.engine.execute('show index from ' + tableName):
            index = Index()
            index.isUnique = (idx['Non_unique'] == 0)
            index.name = str(idx['Key_name'])
            fieldName = idx['Column_name']
            index.fieldName = str(fieldName).lower()
            index.comment = idx['Comment']
            index.seqNO = str(idx['Seq_in_index'])
            index.type = idx['Index_type']
            indices.append(index)

        table = Table(tableName)
        table.fields = fields
        table.indices = indices
        table.comment = tableComment
        return table

    def generateTableData(self):
        tableNames = self.showTables()
        return [self.tableDetail(tableName) for tableName in tableNames]

    def close(mysql):
        if mysql is None:
            return
        try:
            mysql.engine.dispose()
        except:
            traceback.print_exc(file=sys.stdout)
