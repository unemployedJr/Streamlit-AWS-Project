import streamlit as st
from typing import Dict, Any

def render_analysis_cards(results: Dict[str, Any]):
    """
    Renderiza los resultados del análisis en tarjetas.
    
    Args:
        results: Resultados procesados del análisis
    """
    st.markdown("## Resultados del Análisis")
    st.markdown("---")
    
    # Dividir la pantalla en dos columnas
    col1, col2 = st.columns(2)
    
    # Introducción (columna 1)
    with col1:
        st.markdown("### Introducción")
        if results.get("introduction"):
            st.markdown(results["introduction"])
        else:
            st.info("No hay información de introducción disponible.")
    
    # Contexto (columna 2)
    with col2:
        st.markdown("### Contexto")
        if results.get("context"):
            st.markdown(results["context"])
        else:
            st.info("No hay información de contexto disponible.")
    
    st.markdown("---")
    
    # Contenido Principal (ancho completo)
    st.markdown("### Contenido Principal")
    if results.get("main_content"):
        st.markdown(results["main_content"])
    else:
        st.info("No hay contenido principal disponible.")
    
    st.markdown("---")
    
    # Conclusión (ancho completo)
    st.markdown("### Conclusión")
    if results.get("conclusion"):
        st.markdown(results["conclusion"])
    else:
        st.info("No hay conclusión disponible.")