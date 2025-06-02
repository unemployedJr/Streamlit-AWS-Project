import streamlit as st
from typing import Dict, Any
import html

def render_analysis_cards(results: Dict[str, Any]):
    """
    Renderiza los resultados del análisis en tarjetas con el nuevo diseño.
    
    Args:
        results: Resultados procesados del análisis
    """
    st.markdown('<div class="section-title">Resultados del Análisis</div>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Información de depuración
    st.write("Renderizando resultados:", list(results.keys()))
    
    # Función de ayuda para escapar HTML y manejar None
    def safe_html(text):
        if text is None:
            return "No hay información disponible."
        return html.escape(str(text)).replace("\n", "<br>")
    
    # Dividir la pantalla en dos columnas
    col1, col2 = st.columns(2)
    
    with col1:
        # Introducción
        intro_content = safe_html(results.get("introduction", "No hay información de introducción disponible."))
        st.markdown(f"""
        <div class="section-card">
            <div class="section-header">Introducción</div>
            <div class="content-text">{intro_content}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Resumenes ejecutivos
        resumenes_ejecutivos = safe_html(results.get("resumenes_ejecutivos", "No hay resúmenes ejecutivos disponibles."))
        st.markdown(f"""
        <div class="section-card">
            <div class="section-header">Resúmenes Ejecutivos</div>
            <div class="content-text">{resumenes_ejecutivos}</div>
        </div>
        """, unsafe_allow_html=True)

        # Comparacion_documentos
        comparacion_documentos = safe_html(results.get("comparacion_documentos", "No hay comparación de documentos disponible."))
        st.markdown(f"""
        <div class="section-card">
            <div class="section-header">Comparación de Documentos</div>
            <div class="content-text">{comparacion_documentos}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Contexto
        context_content = safe_html(results.get("contexto", "No hay información de contexto disponible."))
        st.markdown(f"""
        <div class="section-card">
            <div class="section-header">Contexto</div>
            <div class="content-text">{context_content}</div>
        </div>
        """, unsafe_allow_html=True)

        # Análisis detallado
        analisis_detallado = safe_html(results.get("analisis_detallado", "No hay análisis detallado disponible."))
        st.markdown(f"""
        <div class="section-card">
            <div class="section-header">Análisis Detallado</div>
            <div class="content-text">{analisis_detallado}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Conclusión
        conclusion_content = safe_html(results.get("conclusion", "No hay conclusión disponible."))
        st.markdown(f"""
        <div class="section-card">
            <div class="section-header">Conclusión</div>
            <div class="content-text">{conclusion_content}</div>
        </div>
        """, unsafe_allow_html=True)