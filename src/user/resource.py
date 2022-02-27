from import_export import fields, resources
from import_export.widgets import ForeignKeyWidget
from import_export.fields import Field
from .models import *
class StudentListResource(resources.ModelResource):
    # fieldname = Field(attribute='record_id', column_name='记录ID')
    # 还可继续写其他字段
    class Meta:
        model = StudentList

