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
        
        # Contenido Principal
        main_content = results.get("main_content", "No hay contenido principal disponible.")
        st.markdown(f"""
        <div class="section-card">
            <div class="section-header">Contenido Principal</div>
            <div class="content-text">{main_content}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Contexto
        context_content = results.get("context", "No hay información de contexto disponible.")
        st.markdown(f"""
        <div class="section-card">
            <div class="section-header">Contexto</div>
            <div class="content-text">{context_content}</div>
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