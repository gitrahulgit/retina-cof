import pandas as pd
from django.db import models
from django.core.management import settings

# Set your Django settings module
settings.configure()

# Import your Django models
from retina.models import Annotation

# Define a function to export a specific table to Excel
def export_table_to_excel():
    # Query all objects from the specific model (YourModel in this example)
    queryset = Annotation.objects.all()

    # Convert the queryset to a Pandas DataFrame
    df = pd.DataFrame.from_records(queryset.values())

    # Specify the Excel file path
    excel_file_path = '/home/rahul/Downloads/annotations.xlsx'

    # Write the DataFrame to an Excel file
    df.to_excel(excel_file_path, index=False)

    print(f'Table exported to {excel_file_path}')

if __name__ == "__main__":
    export_table_to_excel()