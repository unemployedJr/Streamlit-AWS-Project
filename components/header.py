import streamlit as st

def render_header():
    """Renderiza el encabezado de la aplicación."""
    # Título y descripción
    st.title("Centro de Análisis Documentario")
    st.markdown("""
    Esta herramienta le permite analizar documentos regulatorios utilizando inteligencia artificial.
    Seleccione los documentos relevantes y genere un análisis completo.
    """)
    
    # Línea divisoria
    st.markdown("---")