import streamlit as st
import json
import time

# Configuración de la página - DEBE SER LO PRIMERO
st.set_page_config(
    page_title="Centro de Análisis Documentario",
    layout="wide",
    page_icon="📑"
)

# Importar componentes y utilidades
from components.header import render_header
from components.document_selector import render_document_selector
from components.analysis_cards import render_analysis_cards
from utils.session import initialize_session_state, update_analysis_state, clear_selection
from utils.rest_api import initialize_api_client, load_available_documents, analyze_selected_documents

# Función de depuración
def debug_api_results():
    """
    Función de ayuda para mostrar información de depuración sobre los resultados de la API.
    """
    if st.session_state.get('debug_mode', False):
        with st.expander("Debug: API Results"):
            if st.session_state.api_results:
                st.json(st.session_state.api_results)
            else:
                st.info("No hay resultados de API disponibles")
            
            st.write("Analysis State:", st.session_state.analysis_state)
            st.write("Selected Documents:", len(st.session_state.selected_documents))

# Inicializar estado de la sesión
initialize_session_state()

# Inicializar cliente de API
initialize_api_client()

# Habilitar modo debug con un parámetro de URL: ?debug=true
if st.query_params.get('debug', 'false').lower() == 'true':
    st.session_state.debug_mode = True

# Cargar documentos disponibles (solo si no están ya cargados o son None)
if 'available_documents' not in st.session_state or st.session_state.available_documents is None or len(st.session_state.available_documents) == 0:
    with st.spinner("Cargando documentos disponibles..."):
        documents = load_available_documents()

# Renderizar encabezado
render_header()

# Renderizar selector de documentos
selected_documents = render_document_selector()

# Botón para generar análisis
col1, col2, col3 = st.columns([2, 1, 2])
with col2:
    generate_clicked = st.button(
        "Generar Análisis",
        disabled=len(selected_documents) == 0,
        help="Generar análisis completo de los documentos seleccionados",
        type="primary"
    )

# Mostrar información de depuración
debug_api_results()

# Procesar análisis cuando se hace clic en el botón
if generate_clicked and selected_documents:
    # Actualizar estado a "procesando"
    update_analysis_state({
        "status": "processing",
        "progress": 0,
        "message": "Generando análisis...",
        "analysis_id": None
    })
    
    # Mostrar un spinner durante el procesamiento
    with st.spinner("Procesando análisis..."):
        # Solicitar análisis
        success, results = analyze_selected_documents(selected_documents)
        
        if success and results:
            # Actualizar estado a "completado"
            update_analysis_state({
                "status": "complete",
                "progress": 100,
                "message": "Análisis completado",
                "analysis_id": None
            })
            
            # Guardar resultados
            st.session_state.api_results = results
            
            # Mostrar mensaje de éxito ANTES de rerun
            success_placeholder = st.empty()
            success_placeholder.success("¡Análisis completado con éxito!")
            
            # Forzar rerun para mostrar los resultados
            st.rerun()
        else:
            # Actualizar estado a "error"
            update_analysis_state({
                "status": "error",
                "progress": 0,
                "message": "Error al generar análisis",
                "analysis_id": None
            })
            
            st.error("No se pudo completar el análisis. Por favor, intente nuevamente.")

# Mostrar resultados si existen
if st.session_state.api_results is not None:
    st.markdown("---")
    
    # Mostrar información para depuración
    if st.session_state.get('debug_mode', False):
        st.write("Resultados disponibles para mostrar. Estado:", st.session_state.analysis_state["status"])
    
    try:
        # Intentar usar la visualización estilizada
        from components.analysis_cards import render_analysis_cards
        render_analysis_cards(st.session_state.api_results)
    except Exception as e:
        # Si falla, usar la visualización alternativa simple
        st.error(f"Error al renderizar tarjetas estilizadas: {str(e)}")
        from components.analysis_cards_alternate import render_analysis_cards_simple
        render_analysis_cards_simple(st.session_state.api_results)
    
    # Botón para reiniciar (limpiar selección)
    st.markdown("---")
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        if st.button("Nuevo Análisis", type="secondary"):
            clear_selection()
            st.session_state.api_results = None
            st.session_state.analysis_state = {
                "status": "idle",
                "progress": 0,
                "message": "",
                "analysis_id": None
            }
            st.rerun()