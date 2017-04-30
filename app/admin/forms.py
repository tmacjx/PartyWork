import os.path as op
from flask_admin.form import FileUploadField, BaseForm, secure_filename
from config import Config


def prefix_name(obj, file_data):
    parts = op.splitext(file_data.filename)
    return secure_filename('file-%s%s' % parts)


class MyForm(BaseForm):
    upload = FileUploadField('File', base_path=Config.PROJECT_PATH, relative_path=Config.MEDIA_PATH,
                             abnamegen=prefix_name)
