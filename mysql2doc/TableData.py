class Field:
    def __init__(self, name=None, type=None, comment=None, nullable=None, isPK=None,
                 type_cn=None, nullable_cn=None, isPK_cn=None, biz_rule=None):
        super().__init__()
        self.name = name
        self.type = type
        self.comment = comment
        self.nullable = nullable
        self.isPK = isPK
        self.type_cn = type_cn
        self.nullable_cn = nullable_cn
        self.isPK_cn = isPK_cn
        # 逻辑实体清单中的业务规则
        self.biz_rule = biz_rule


class Index:
    def __init__(self, isUnique=None, name=None, seqNO=None, fieldName=None, comment=None):
        super().__init__()
        self.comment = comment
        self.fieldName = fieldName
        self.seqNO = seqNO
        self.name = name
        self.isUnique = isUnique


class Table:
    def __init__(self, name=None, comment=None):
        self.name = name
        self.fieldNames = []
        self.fields = []
        self.indices = []
        self.comment = comment
        self.pk_field_name = None

    def addField(self, field):
        self.fields.append(field)

    def addIndex(self, index):
        self.indices.append(index)
