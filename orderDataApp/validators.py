from django.core.exceptions import ValidationError
import magic

def validate_file_type(csv_file):
    initial_pos = csv_file.tell()
    csv_file.seek(0)   

    valid_mime_types = ['text/plain']
    file_mime_type = magic.from_buffer(csv_file.read(2048), mime=True)
    csv_file.seek(initial_pos)
    if file_mime_type not in valid_mime_types:
        raise ValidationError('Unsupported file type.')
    

def validate_content_type(csv_file):
    file_type = csv_file.content_type
    if not file_type == 'application/vnd.ms-excel':
        raise ValidationError('Unsupported content type.')
    

def validate_file_extension(csv_file):

    file_name = csv_file.name
    ext = file_name.split(".")[-1]  # [0] returns the extension
    valid_extensions = ['csv']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')

