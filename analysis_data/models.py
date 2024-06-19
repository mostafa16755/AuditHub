from django.db import models

class CSV(models.Model):
    csv_file = models.FileField(upload_to='uploads/' ,default="CinemasCsv.csv")  # Assuming you want to store the uploaded CSV files

    # Optionally, you can add more fields to the model if needed

    
    def __str__(self):
        return self.csv_file.name
