import streamlit as st
from typing import Dict, List, Any

def initialize_session_state():
    """
    Inicializa todas las variables de estado de la sesión necesarias.
    Debe llamarse al inicio de la aplicación.
    """
    # Lista de documentos seleccionados
    if 'selected_documents' not in st.session_state:
        st.session_state.selected_documents = []
    
    # Último documento intentado agregar
    if 'last_attempted_document' not in st.session_state:
        st.session_state.last_attempted_document = None
    
    # Contador para forzar recreación del selectbox
    if 'selector_key' not in st.session_state:
        st.session_state.selector_key = 0
    
    # Resultados del análisis
    if 'api_results' not in st.session_state:
        st.session_state.api_results = None
    
    # Estado del análisis
    if 'analysis_state' not in st.session_state:
        st.session_state.analysis_state = {
            "status": "idle",  # idle, processing, complete, error
            "progress": 0,
            "message": "",
            "analysis_id": None
        }
    
    # Documentos disponibles (se cargarán desde la API)
    if 'available_documents' not in st.session_state:
        st.session_state.available_documents = None

def update_analysis_state(state: Dict[str, Any]):
    """
    Actualiza el estado del análisis SIN causar rerun automático.
    
    Args:
        state: Diccionario con el nuevo estado
    """
    # Actualizar los campos proporcionados
    for key, value in state.items():
        if key in st.session_state.analysis_state:
            st.session_state.analysis_state[key] = value
    
    # NO hacer rerun automático - esto estaba causando el problema

def add_document(document: Dict[str, Any]) -> bool:
    """
    Añade un documento a la lista de seleccionados.
    
    Args:
        document: Documento a añadir
        
    Returns:
        bool: True si se añadió correctamente, False si ya existía
    """
    # Verificar si ya está seleccionado
    is_already_selected = document['id'] in [d['id'] for d in st.session_state.selected_documents]
    
    if not is_already_selected:
        # Documento no está seleccionado, agregarlo
        st.session_state.selected_documents.append(document)
        st.session_state.last_attempted_document = document['id']
        
        # Resetear los resultados de la API cuando se cambia la selección
        st.session_state.api_results = None
        st.session_state.analysis_state["status"] = "idle"
        
        # Incrementar la clave para forzar el reseteo del selectbox
        st.session_state.selector_key += 1
        return True
    else:
        # Documento ya está seleccionado
        st.session_state.last_attempted_document = document['id']
        return False

def clear_selection():
    """Limpia todos los documentos seleccionados y el estado del análisis."""
    st.session_state.selected_documents = []
    st.session_state.last_attempted_document = None
    st.session_state.api_results = None
    st.session_state.analysis_state = {
        "status": "idle",
        "progress": 0,
        "message": "",
        "analysis_id": None
    }
    st.session_state.selector_key += 1