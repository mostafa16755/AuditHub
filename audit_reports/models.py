from django.db import models

class AuditReport(models.Model):
    company = models.CharField(max_length=100, null=True)
    content = models.TextField(null=True)
    addressee = models.CharField(max_length=100, null=True)
    introductory_paragraph = models.TextField(blank=True, null=True)  
    managements_responsibility = models.TextField(blank=True, null=True)  
    auditors_responsibility = models.TextField(blank=True, null=True)  
    scope_paragraph = models.TextField(blank=True, null=True)  
    opinion_paragraph = models.TextField(blank=True, null=True)  
    basis_of_opinion = models.TextField(blank=True, null=True)  
    date = models.DateField(auto_now_add=True)  # Automatically set to current date
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.company} - {self.date}"