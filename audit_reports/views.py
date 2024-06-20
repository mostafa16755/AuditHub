from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from .forms import AuditReportForm
from .models import AuditReport

def create_audit_report(request):
    if request.method == 'POST':
        form = AuditReportForm(request.POST)
        if form.is_valid():
            audit_report = form.save()

            # Generate PDF using ReportLab
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'filename="audit_report.pdf"'

            # Define styles
            styles = getSampleStyleSheet()
            title_style = styles['Title']
            normal_style = styles['Normal']

            doc = SimpleDocTemplate(response, pagesize=letter)
            elements = []

            # Add elements to the PDF
            elements.append(Paragraph('Audit Report', title_style))
            elements.append(Paragraph(f'Company Name: {audit_report.company}', normal_style))
            elements.append(Paragraph(f'Content: {audit_report.content}', normal_style))
            elements.append(Paragraph(f'Addressee: {audit_report.addressee}', normal_style))
            elements.append(Paragraph(f'Introductory Paragraph: {audit_report.introductory_paragraph}', normal_style))
            elements.append(Paragraph(f"Management's Responsibility: {audit_report.managements_responsibility}", normal_style))
            elements.append(Paragraph(f"Auditor's Responsibility: {audit_report.auditors_responsibility}", normal_style))
            elements.append(Paragraph(f'Scope Paragraph: {audit_report.scope_paragraph}', normal_style))
            elements.append(Paragraph(f'Opinion Paragraph: {audit_report.opinion_paragraph}', normal_style))
            elements.append(Paragraph(f'Basis of Opinion: {audit_report.basis_of_opinion}', normal_style))
            elements.append(Paragraph(f'Date: {audit_report.date}', normal_style))

            doc.build(elements)
            return response
    else:
        form = AuditReportForm()
    return render(request, 'create_audit_report.html', {'form': form})

def audit_report_list(request):
    audit_reports = AuditReport.objects.all().order_by('-date')  # Order by date descending
    return render(request, 'audit_report_list.html', {'audit_reports': audit_reports})

def audit_report_detail(request, report_id):
    audit_report = get_object_or_404(AuditReport, pk=report_id)
    return render(request, 'audit_report_detail.html', {'audit_report': audit_report})
