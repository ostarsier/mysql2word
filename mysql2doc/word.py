import jinja2
from docxtpl import DocxTemplate

from mysql2doc.MySql import MySql

tpl = DocxTemplate('db_min.docx')

mysql = None
try:
    mysql = MySql()
    table_list = mysql.generateTableData()
    context = {
        'table_list': table_list
    }
    jinja_env = jinja2.Environment(autoescape=True)
    tpl.render(context, jinja_env)
    tpl.save('db.docx')
finally:
    MySql.close(mysql)
