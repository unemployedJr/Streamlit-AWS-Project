import streamlit as st
import json
import time

# Configuración de la página
st.set_page_config(
    page_title="Solución de problemas",
    layout="wide",
    page_icon="🔧"
)

# Agregar un título
st.title("Herramienta de Solución de Problemas")

st.markdown("""
Esta herramienta te ayudará a identificar y solucionar problemas con tu aplicación Centro de Análisis Documentario.
""")

# Verificar estado de la sesión
st.header("1. Estado de la Sesión")

if 'selected_documents' in st.session_state:
    st.success(f"✅ selected_documents: {len(st.session_state.selected_documents)} documentos")
else:
    st.error("❌ selected_documents no está inicializado")

if 'api_results' in st.session_state:
    if st.session_state.api_results:
        st.success("✅ api_results contiene datos")
        st.write("Estructura de api_results:")
        st.json(st.session_state.api_results)
    else:
        st.warning("⚠️ api_results está vacío o es None")
else:
    st.error("❌ api_results no está inicializado")

if 'analysis_state' in st.session_state:
    st.success("✅ analysis_state está inicializado")
    st.write("Estado actual:", st.session_state.analysis_state)
else:
    st.error("❌ analysis_state no está inicializado")

# Probar la API
st.header("2. Prueba de API")

from utils.rest_api import initialize_api_client, load_available_documents, analyze_selected_documents
from utils.session import initialize_session_state

# Inicializar estado si no existe
if 'api_client' not in st.session_state:
    initialize_session_state()
    initialize_api_client()

# Mostrar documentos disponibles
if st.button("Cargar Documentos"):
    with st.spinner("Cargando documentos..."):
        docs = load_available_documents()
        st.write(f"Se cargaron {len(docs)} documentos")
        st.dataframe(docs)

# Simular análisis con datos de prueba
st.subheader("Simular Análisis")

if st.button("Simular Análisis con Datos de Prueba"):
    # Crear datos de prueba
    test_results = {
        "introduction": "Esta es una introducción de prueba.",
        "contexto": "Este es un contexto de prueba.",
        "resumenes_ejecutivos": "Estos son resúmenes ejecutivos de prueba.",
        "analisis_detallado": "Este es un análisis detallado de prueba.",
        "comparacion_documentos": "Esta es una comparación de documentos de prueba.",
        "conclusion": "Esta es una conclusión de prueba."
    }
    
    # Guardar en estado de sesión
    st.session_state.api_results = test_results
    st.session_state.analysis_state = {
        "status": "complete",
        "progress": 100,
        "message": "Análisis completado (simulación)",
        "analysis_id": None
    }
    
    st.success("Datos de prueba guardados en el estado de la sesión")
    
    # Mostrar datos
    from components.analysis_cards import render_analysis_cards
    render_analysis_cards(test_results)

# Mostrar información técnica
st.header("3. Información Técnica")

# Versiones
import streamlit as st_version
st.write(f"Versión de Streamlit: {st_version.__version__}")

# Estructura de directorios
st.subheader("Estructura de Directorios")
import os
current_dir = os.getcwd()
st.write(f"Directorio actual: {current_dir}")

# Listar archivos en el directorio actual
files = os.listdir(current_dir)
st.write("Archivos en el directorio raíz:")
st.write(files)

# Listar archivos en components y utils
if os.path.exists("components"):
    st.write("Archivos en components:")
    st.write(os.listdir("components"))

if os.path.exists("utils"):
    st.write("Archivos en utils:")
    st.write(os.listdir("utils"))

# Botón para limpiar el estado de la sesión
st.header("4. Herramientas de Mantenimiento")

if st.button("Limpiar Estado de Sesión"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.success("Estado de sesión limpiado")
    st.rerun()