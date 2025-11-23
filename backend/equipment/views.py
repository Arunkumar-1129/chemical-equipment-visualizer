from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.db.models import Q
import pandas as pd
import json
import os
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from .models import EquipmentDataset
from .serializers import EquipmentDatasetSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """Register a new user"""
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email', '')
    
    if not username or not password:
        return Response({'error': 'Username and password required'}, 
                       status=status.HTTP_400_BAD_REQUEST)
    
    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists'}, 
                       status=status.HTTP_400_BAD_REQUEST)
    
    user = User.objects.create_user(username=username, password=password, email=email)
    token, _ = Token.objects.get_or_create(user=user)
    
    return Response({
        'token': token.key,
        'user_id': user.id,
        'username': user.username
    }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    """Login user and return token"""
    from django.contrib.auth import authenticate
    
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response({'error': 'Username and password required'}, 
                       status=status.HTTP_400_BAD_REQUEST)
    
    user = authenticate(username=username, password=password)
    
    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.id,
            'username': user.username
        })
    else:
        return Response({'error': 'Invalid credentials'}, 
                       status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_csv(request):
    """Upload and process CSV file"""
    if 'file' not in request.FILES:
        return Response({'error': 'No file provided'}, 
                       status=status.HTTP_400_BAD_REQUEST)
    
    file = request.FILES['file']
    
    try:
        # Read CSV file
        df = pd.read_csv(file)
        
        # Validate required columns
        required_columns = ['Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            return Response({
                'error': f'Missing required columns: {", ".join(missing_columns)}'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Calculate summary statistics
        total_count = len(df)
        avg_flowrate = df['Flowrate'].mean() if 'Flowrate' in df.columns else None
        avg_pressure = df['Pressure'].mean() if 'Pressure' in df.columns else None
        avg_temperature = df['Temperature'].mean() if 'Temperature' in df.columns else None
        
        # Equipment type distribution
        equipment_type_dist = df['Type'].value_counts().to_dict()
        
        # Convert DataFrame to list of dictionaries
        raw_data = df.to_dict('records')
        
        # Store in database
        dataset = EquipmentDataset.objects.create(
            user=request.user,
            filename=file.name,
            total_count=total_count,
            avg_flowrate=avg_flowrate,
            avg_pressure=avg_pressure,
            avg_temperature=avg_temperature,
            equipment_type_distribution=json.dumps(equipment_type_dist),
            raw_data=json.dumps(raw_data)
        )
        
        # Keep only last 5 datasets per user
        datasets = EquipmentDataset.objects.filter(user=request.user).order_by('-uploaded_at')
        if datasets.count() > 5:
            for old_dataset in datasets[5:]:
                old_dataset.delete()
        
        # Return summary
        return Response({
            'id': dataset.id,
            'filename': dataset.filename,
            'uploaded_at': dataset.uploaded_at,
            'summary': {
                'total_count': total_count,
                'avg_flowrate': avg_flowrate,
                'avg_pressure': avg_pressure,
                'avg_temperature': avg_temperature,
                'equipment_type_distribution': equipment_type_dist
            },
            'data': raw_data
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({'error': str(e)}, 
                       status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_summary(request, dataset_id=None):
    """Get summary statistics for a specific dataset or latest"""
    if dataset_id:
        try:
            dataset = EquipmentDataset.objects.get(id=dataset_id, user=request.user)
        except EquipmentDataset.DoesNotExist:
            return Response({'error': 'Dataset not found'}, 
                           status=status.HTTP_404_NOT_FOUND)
    else:
        # Get latest dataset
        dataset = EquipmentDataset.objects.filter(user=request.user).first()
        if not dataset:
            return Response({'error': 'No datasets found'}, 
                           status=status.HTTP_404_NOT_FOUND)
    
    return Response({
        'id': dataset.id,
        'filename': dataset.filename,
        'uploaded_at': dataset.uploaded_at,
        'summary': {
            'total_count': dataset.total_count,
            'avg_flowrate': dataset.avg_flowrate,
            'avg_pressure': dataset.avg_pressure,
            'avg_temperature': dataset.avg_temperature,
            'equipment_type_distribution': dataset.get_equipment_type_distribution()
        }
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_history(request):
    """Get last 5 uploaded datasets"""
    datasets = EquipmentDataset.objects.filter(user=request.user).order_by('-uploaded_at')[:5]
    serializer = EquipmentDatasetSerializer(datasets, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_dataset_data(request, dataset_id):
    """Get full data for a specific dataset"""
    try:
        dataset = EquipmentDataset.objects.get(id=dataset_id, user=request.user)
        serializer = EquipmentDatasetSerializer(dataset)
        return Response(serializer.data)
    except EquipmentDataset.DoesNotExist:
        return Response({'error': 'Dataset not found'}, 
                       status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def generate_pdf_report(request, dataset_id):
    """Generate PDF report for a dataset"""
    try:
        dataset = EquipmentDataset.objects.get(id=dataset_id, user=request.user)
    except EquipmentDataset.DoesNotExist:
        return Response({'error': 'Dataset not found'}, 
                       status=status.HTTP_404_NOT_FOUND)
    
    # Create PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="report_{dataset.id}.pdf"'
    
    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()
    
    # Title
    title = Paragraph(f"Equipment Data Report: {dataset.filename}", styles['Title'])
    elements.append(title)
    elements.append(Spacer(1, 0.2*inch))
    
    # Summary
    summary_title = Paragraph("Summary Statistics", styles['Heading2'])
    elements.append(summary_title)
    
    summary_data = [
        ['Metric', 'Value'],
        ['Total Equipment Count', str(dataset.total_count)],
        ['Average Flowrate', f"{dataset.avg_flowrate:.2f}" if dataset.avg_flowrate else "N/A"],
        ['Average Pressure', f"{dataset.avg_pressure:.2f}" if dataset.avg_pressure else "N/A"],
        ['Average Temperature', f"{dataset.avg_temperature:.2f}" if dataset.avg_temperature else "N/A"],
    ]
    
    summary_table = Table(summary_data)
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(summary_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Equipment Type Distribution
    dist_title = Paragraph("Equipment Type Distribution", styles['Heading2'])
    elements.append(dist_title)
    
    dist = dataset.get_equipment_type_distribution()
    dist_data = [['Equipment Type', 'Count']]
    for eq_type, count in dist.items():
        dist_data.append([eq_type, str(count)])
    
    dist_table = Table(dist_data)
    dist_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(dist_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Footer
    footer = Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 
                      styles['Normal'])
    elements.append(footer)
    
    doc.build(elements)
    return response



