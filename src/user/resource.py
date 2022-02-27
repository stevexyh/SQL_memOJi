from import_export import fields, resources
from import_export.widgets import ForeignKeyWidget
from import_export.fields import Field
from .models import *
class StudentListResource(resources.ModelResource):
    # fieldname = Field(attribute='record_id', column_name='记录ID')
    # 还可继续写其他字段
    classroom = fields.Field(
        column_name='classroom',
        attribute='classroom',
        widget=ForeignKeyWidget(Classroom, 'join_code'))
    class Meta:
        model = StudentList
        list_display = ['record_id','full_name','internal_id','classroom','join_status']
        fields = ('full_name','internal_id','classroom')
        export_order = ('full_name', 'internal_id', 'classroom')
        import_id_fields = ['internal_id','full_name']
