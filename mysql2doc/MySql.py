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
        tables = []
        for db in dbConfigMap['dbs'].split(","):
            self.engine.execute('use ' + db)
            for line in self.engine.execute('show tables'):
                tables.append(db + '.' + line[0])
        return tables
        # return [ele[0] for ele in self.engine.execute('show tables')]

    def type_en_to_cn(self, en):
        if "CHAR" in en or 'text' in en:
            return '变长字符串'
        if "INT" in en or "DOUBLE" in en:
            return '数字'
        if "DATE" in en:
            return '日期'
        return ''

    def tableDetail(self, table):
        fields = []
        fieldNames = []
        pk_field_name = None
        db = table.split('.')[0]
        tableName = table.split('.')[1]
        self.engine.execute('use ' + db)
        for fieldRow in self.engine.execute('show full columns from ' + tableName):
            field = Field()
            field.name = fieldRow['Field']
            field.type = str(fieldRow['Type']).upper()
            field.nullable = 'Y' if fieldRow['Null'] == 'YES' else 'N'
            field.isPK = '主键ID' if fieldRow['Key'] == 'PRI' else ''
            field.biz_rule = '自动生成' if fieldRow['Key'] == 'PRI' else '填写'
            field.comment = fieldRow['Comment']
            field.default = fieldRow['Default']
            field.extra = fieldRow['Extra']
            field.type_cn = self.type_en_to_cn(field.type)
            field.nullable_cn = '是' if fieldRow['Null'] == 'YES' else '否'
            field.isPK_cn = '是' if fieldRow['Key'] == 'PRI' else '否'
            if fieldRow['Key'] == 'PRI':
                pk_field_name = field.comment
            fields.append(field)
            if field.comment is not None:
                fieldNames.append(field.comment)
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

        table = Table(table)
        table.fields = fields
        table.fieldNames = '、'.join(fieldNames)
        table.indices = indices
        table.comment = tableComment
        table.pk_field_name = pk_field_name
        return table

    def generateTableData(self):
        tables = self.showTables()
        return [self.tableDetail(table) for table in tables]

    def close(mysql):
        if mysql is None:
            return
        try:
            mysql.engine.dispose()
        except:
            traceback.print_exc(file=sys.stdout)
