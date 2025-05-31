import streamlit as st
import json
import time

# Importar componentes y utilidades
from components.header import render_header
from components.document_selector import render_document_selector
from components.analysis_cards import render_analysis_cards
from utils.session import initialize_session_state, update_analysis_state, clear_selection
from utils.rest_api import initialize_api_client, load_available_documents, analyze_selected_documents

# Configuración de la página
st.set_page_config(
    page_title="Centro de análisis documentario",
    layout="wide",
    page_icon="📑"
)

# Inicializar estado de la sesión
initialize_session_state()

# Inicializar cliente de API
initialize_api_client()

# Cargar documentos disponibles (solo si no están ya cargados)
if 'available_documents' not in st.session_state:
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
        help="Generar análisis completo de los documentos seleccionados"
    )

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
    with st.spinner("Procesando análisis de documentos..."):
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
            st.success("¡Análisis completado con éxito!")
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
if st.session_state.api_results and st.session_state.analysis_state["status"] == "complete":
    render_analysis_cards(st.session_state.api_results)

# Botón para reiniciar (limpiar selección)
if st.session_state.api_results:
    st.markdown("---")
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        if st.button("Nuevo Análisis"):
            clear_selection()
            st.session_state.api_results = None
            st.session_state.analysis_state = {
                "status": "idle",
                "progress": 0,
                "message": "",
                "analysis_id": None
            }
            st.rerun()