import streamlit as st
from datetime import datetime
import io
from typing import Dict, Any, List

def create_download_button(results: Dict[str, Any], selected_documents: List[Dict[str, Any]]):
    """
    Crea un botón de descarga para el PDF del análisis.
    
    Args:
        results: Resultados procesados del análisis
        selected_documents: Lista de documentos seleccionados
    """
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.colors import HexColor
    except ImportError as e:
        st.error(f"❌ Error importando ReportLab: {e}")
        return
    
    try:
        # Generar el PDF
        pdf_data = generate_analysis_pdf_fixed(results, selected_documents)
        
        if pdf_data:
            # Crear nombre del archivo con timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"analisis_documentario_{timestamp}.pdf"
            
            # Botón de descarga
            st.download_button(
                label="📄 Descargar Análisis (PDF)",
                data=pdf_data,
                file_name=filename,
                mime="application/pdf",
                help="Descargar el análisis completo en formato PDF"
            )
        else:
            st.error("No se pudo generar el PDF")
        
    except Exception as e:
        st.error(f"Error al generar el PDF: {str(e)}")

def generate_analysis_pdf_fixed(results: Dict[str, Any], selected_documents: List[Dict[str, Any]]) -> bytes:
    """
    Genera un PDF con todos los resultados del análisis.
    Versión corregida que evita el problema de conversión a dict.
    """
    # Importaciones locales
    from reportlab.lib.pagesizes import A4
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.colors import HexColor
    
    # Crear buffer
    buffer = io.BytesIO()
    
    # Función interna para crear y construir el PDF
    def build_pdf():
        # Crear el documento PDF dentro de la función para evitar interferencias
        pdf_doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18
        )
        
        # Verificar inmediatamente que es el tipo correcto
        if not hasattr(pdf_doc, 'build'):
            raise ValueError(f"PDF document object is invalid: {type(pdf_doc)}")
        
        # Obtener estilos
        styles = getSampleStyleSheet()
        
        # Crear estilos personalizados
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=20,
            spaceAfter=30,
            alignment=1,  # Centrado
            textColor=HexColor('#2C3E50'),
            fontName='Helvetica-Bold'
        )
        
        section_title_style = ParagraphStyle(
            'SectionTitle',
            parent=styles['Heading2'],
            fontSize=14,
            spaceAfter=15,
            spaceBefore=20,
            textColor=HexColor('#3498DB'),
            fontName='Helvetica-Bold'
        )
        
        content_style = ParagraphStyle(
            'Content',
            parent=styles['Normal'],
            fontSize=11,
            spaceAfter=12,
            alignment=4,  # Justificado
            fontName='Helvetica',
            leading=16
        )
        
        doc_list_style = ParagraphStyle(
            'DocList',
            parent=styles['Normal'],
            fontSize=10,
            spaceAfter=8,
            leftIndent=20,
            fontName='Helvetica'
        )
        
        # Crear story
        story = []
        
        # Título principal
        story.append(Paragraph("CENTRO DE ANÁLISIS DOCUMENTARIO", title_style))
        story.append(Paragraph("Reporte de Análisis", styles['Heading2']))
        story.append(Spacer(1, 20))
        
        # Información del reporte
        current_date = datetime.now().strftime("%d/%m/%Y %H:%M")
        story.append(Paragraph(f"<b>Fecha de generación:</b> {current_date}", content_style))
        story.append(Paragraph(f"<b>Total de documentos analizados:</b> {len(selected_documents)}", content_style))
        story.append(Spacer(1, 20))
        
        # Lista de documentos analizados
        story.append(Paragraph("Documentos Analizados", section_title_style))
        for i, document in enumerate(selected_documents, 1):
            doc_name = document.get('name', 'Sin nombre')
            # Escapar caracteres especiales
            doc_name = escape_xml_chars(doc_name)
            doc_text = f"{i}. {doc_name}"
            story.append(Paragraph(doc_text, doc_list_style))
        
        story.append(Spacer(1, 30))
        story.append(PageBreak())
        
        # Secciones del análisis
        sections_data = [
            ("Introducción", results.get("introduction", "")),
            ("Contexto", results.get("contexto", "")),
            ("Resúmenes Ejecutivos", results.get("resumenes_ejecutivos", "")),
            ("Análisis Detallado", results.get("analisis_detallado", "")),
            ("Comparación de Documentos", results.get("comparacion_documentos", "")),
            ("Conclusión", results.get("conclusion", ""))
        ]
        
        for section_name, section_content in sections_data:
            if section_content and section_content.strip():
                # Título de la sección
                story.append(Paragraph(section_name, section_title_style))
                
                # Procesar contenido en párrafos
                paragraphs = section_content.split('\n\n')
                for paragraph in paragraphs:
                    if paragraph.strip():
                        # Limpiar y escapar el texto
                        clean_text = paragraph.strip().replace('\n', ' ')
                        clean_text = escape_xml_chars(clean_text)
                        
                        # Limitar longitud del párrafo para evitar problemas
                        if len(clean_text) > 2000:
                            clean_text = clean_text[:2000] + "..."
                        
                        story.append(Paragraph(clean_text, content_style))
                
                story.append(Spacer(1, 20))
        
        # Verificar nuevamente antes de build
        if not hasattr(pdf_doc, 'build'):
            raise ValueError(f"PDF document lost build method: {type(pdf_doc)}")
        
        # Construir el PDF
        pdf_doc.build(story)
        
        return True
    
    try:
        # Ejecutar la construcción del PDF
        success = build_pdf()
        
        if success:
            # Obtener datos del buffer
            pdf_data = buffer.getvalue()
            buffer.close()
            return pdf_data
        else:
            buffer.close()
            return b""
            
    except Exception as e:
        buffer.close()
        st.error(f"Error en build_pdf: {str(e)}")
        return b""

def escape_xml_chars(text: str) -> str:
    """
    Escapa caracteres especiales para XML/HTML.
    
    Args:
        text: Texto a escapar
        
    Returns:
        str: Texto escapado
    """
    if not isinstance(text, str):
        text = str(text)
    
    # Escapar caracteres básicos
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    text = text.replace('"', '&quot;')
    text = text.replace("'", '&#x27;')
    
    return text