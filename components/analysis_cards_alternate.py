import streamlit as st
from typing import Dict, Any

def render_analysis_cards_simple(results: Dict[str, Any]):
    """
    Renderiza los resultados del análisis utilizando componentes básicos de Streamlit
    en lugar de HTML personalizado. Útil para depuración y como alternativa.
    
    Args:
        results: Resultados procesados del análisis
    """
    st.header("Resultados del Análisis")
    st.markdown("---")
    
    # Dividir la pantalla en dos columnas
    col1, col2 = st.columns(2)
    
    with col1:
        # Introducción
        with st.container():
            st.subheader("Introducción")
            intro_content = results.get("introduction", "No hay información de introducción disponible.")
            st.write(intro_content)
        
        # Resúmenes ejecutivos
        with st.container():
            st.subheader("Resúmenes Ejecutivos")
            resumenes_ejecutivos = results.get("resumenes_ejecutivos", "No hay resúmenes ejecutivos disponibles.")
            st.write(resumenes_ejecutivos)
        
        # Comparación de documentos
        with st.container():
            st.subheader("Comparación de Documentos")
            comparacion_documentos = results.get("comparacion_documentos", "No hay comparación de documentos disponible.")
            st.write(comparacion_documentos)
    
    with col2:
        # Contexto
        with st.container():
            st.subheader("Contexto")
            context_content = results.get("contexto", "No hay información de contexto disponible.")
            st.write(context_content)
        
        # Análisis detallado
        with st.container():
            st.subheader("Análisis Detallado")
            analisis_detallado = results.get("analisis_detallado", "No hay análisis detallado disponible.")
            st.write(analisis_detallado)
        
        # Conclusión
        with st.container():
            st.subheader("Conclusión")
            conclusion_content = results.get("conclusion", "No hay conclusión disponible.")
            st.write(conclusion_content)