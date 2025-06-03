import streamlit as st
from typing import Dict, Any

def render_analysis_cards(results: Dict[str, Any]):
    """
    Renderiza los resultados del análisis en tarjetas con el nuevo diseño.
    
    Args:
        results: Resultados procesados del análisis
    """
    st.markdown('<div class="section-title">Resultados del Análisis</div>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Dividir la pantalla en dos columnas
    col1, col2 = st.columns(2)
    
    with col1:
        # Introducción
        intro_content = results.get("introduction", "No hay información de introducción disponible.")
        st.markdown(f"""
        <div class="section-card">
            <div class="section-header">Introducción</div>
            <div class="content-text">{intro_content}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Resumenes ejecutivos
        resumenes_ejecutivos = results.get("resumenes_ejecutivos", "No hay resúmenes ejecutivos disponibles.")
        st.markdown(f"""
        <div class="section-card">
            <div class="section-header">Resúmenes Ejecutivos</div>
            <div class="content-text">{resumenes_ejecutivos}</div>
        </div>
        """, unsafe_allow_html=True)

         # Comparacion_documentos
        comparacion_documentos = results.get("comparacion_documentos", "No hay contenido principal disponible.")
        st.markdown(f"""
        <div class="section-card">
            <div class="section-header">Comparación de Documentos</div>
            <div class="content-text">{comparacion_documentos}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Contexto
        context_content = results.get("contexto", "No hay información de contexto disponible.")
        st.markdown(f"""
        <div class="section-card">
            <div class="section-header">Contexto</div>
            <div class="content-text">{context_content}</div>
        </div>
        """, unsafe_allow_html=True)

        # Análisis detallado
        analisis_detallado = results.get("analisis_detallado", "No hay información de contexto disponible.")
        st.markdown(f"""
        <div class="section-card">
            <div class="section-header">Análisis detallado</div>
            <div class="content-text">{analisis_detallado}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Conclusión
        conclusion_content = results.get("conclusion", "No hay conclusión disponible.")
        st.markdown(f"""
        <div class="section-card">
            <div class="section-header">Conclusión</div>
            <div class="content-text">{conclusion_content}</div>
        </div>
        """, unsafe_allow_html=True)

    # ======= SECCIÓN DE REFERENCIAS SIMPLE =======
    st.markdown("---")
    
    # Obtener datos de referencias
    referencias_data = results.get("referencias_data", [])
    
    if referencias_data and isinstance(referencias_data, list) and len(referencias_data) > 0:
        # Crear contenido de referencias como texto simple
        referencias_content = ""
        
        for i, ref in enumerate(referencias_data, 1):
            tipo_doc = ref.get('tipo_doc', 'Documento')
            num_interno = ref.get('num_interno_doc', 'N/A')
            area = ref.get('area', 'N/A')
            fecha = ref.get('fecha_emision', 'N/A')
            expediente = ref.get('num_expediente', 'N/A')
            viddoc = ref.get('viddoc', 'N/A')
            
            # Agregar cada referencia como texto simple
            referencias_content += f"""
Referencia {i}: {tipo_doc} - N° {num_interno}

Área Emisora: {area}
Fecha de Emisión: {fecha}
N° de Expediente: {expediente}
ID del Documento: {viddoc}

"""
            if i < len(referencias_data):
                referencias_content += "---\n\n"
        
        # Mostrar usando el mismo formato que las otras secciones
        st.markdown(f"""
        <div class="section-card">
            <div class="section-header">Referencias</div>
            <div class="content-text">{referencias_content}</div>
        </div>
        """, unsafe_allow_html=True)
        
    else:
        # Mensaje cuando no hay referencias
        st.markdown("""
        <div class="section-card">
            <div class="section-header">Referencias</div>
            <div class="content-text">No se encontraron referencias en la respuesta del análisis.</div>
        </div>
        """, unsafe_allow_html=True)