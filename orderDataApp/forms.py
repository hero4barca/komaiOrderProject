from django import forms
from django.core.exceptions import ValidationError

# import validatord for csv file type
from .validators import validate_file_extension, validate_content_type, validate_file_type
from orderDataApp.classes.csv_file_reader import * 

class CsvUploadForm(forms.Form):
    csv_file = forms.FileField(validators=[validate_file_extension,
                                             validate_file_type,
                                              validate_content_type])

    def clean(self):
        cleaned_data = super().clean()
        cc_csv_file = cleaned_data.get("csv_file")
        
        if cc_csv_file:
            new_csv_data = CsvFileReader() # instance var
            
            
            try:
                csv_order_data, summary = new_csv_data.process_file(cc_csv_file)
                cleaned_data["order_data"] = csv_order_data
                cleaned_data["summary"] = summary
                               
                            
            except KeyError as err :                
                msg = "missing column key. {}".format( err.args)
                raise ValidationError(msg)

            except Exception as err:
                msg = "Cannot process csv file. {}".format(  err.args)
                raise ValidationError (msg)
        
        return cleaned_data # return cleaned data





