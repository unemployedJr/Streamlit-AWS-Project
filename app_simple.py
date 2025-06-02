import streamlit as st
import time
import json

# Configuración de la página
st.set_page_config(
    page_title="Centro de Análisis Documentario (Simplificado)",
    layout="wide",
    page_icon="📑"
)

# Inicializar el estado de la sesión si es necesario
if 'selected_documents' not in st.session_state:
    st.session_state.selected_documents = []

if 'available_documents' not in st.session_state:
    st.session_state.available_documents = []

if 'api_results' not in st.session_state:
    st.session_state.api_results = None

# Cargar utilidades
from utils.rest_api import initialize_api_client, load_available_documents, analyze_selected_documents
from utils.session import initialize_session_state, update_analysis_state, clear_selection, add_document

# Inicializar estado y cliente API
initialize_session_state()
initialize_api_client()

# Funciones simplificadas
def process_results(results):
    """
    Procesa los resultados de la API a un formato simple.
    """
    processed = {}
    sections = ["introduction", "contexto", "resumenes_ejecutivos", "analisis_detallado", "comparacion_documentos", "conclusion"]
    
    if isinstance(results, dict) and "sections" in results:
        for section in sections:
            if section in results["sections"]:
                section_data = results["sections"][section]
                if isinstance(section_data, list):
                    texts = []
                    for item in section_data:
                        if isinstance(item, dict) and "text" in item:
                            texts.append(item["text"])
                        elif isinstance(item, str):
                            texts.append(item)
                    processed[section] = "\n\n".join(texts)
                elif isinstance(section_data, str):
                    processed[section] = section_data
                else:
                    processed[section] = f"Error en formato de {section}"
            else:
                processed[section] = f"No hay datos para {section}"
    elif isinstance(results, dict):
        for section in sections:
            if section in results:
                if isinstance(results[section], list):
                    texts = []
                    for item in results[section]:
                        if isinstance(item, dict) and "text" in item:
                            texts.append(item["text"])
                        elif isinstance(item, str):
                            texts.append(item)
                    processed[section] = "\n\n".join(texts)
                elif isinstance(results[section], str):
                    processed[section] = results[section]
                else:
                    processed[section] = f"Error en formato de {section}"
            else:
                processed[section] = f"No hay datos para {section}"
    else:
        for section in sections:
            processed[section] = "Formato de resultados inválido"
    
    return processed

def show_results(results):
    """
    Muestra los resultados procesados.
    """
    st.header("Resultados del Análisis")
    
    # Dividir en dos columnas
    col1, col2 = st.columns(2)
    
    with col1:
        # Introducción
        st.subheader("Introducción")
        st.write(results.get("introduction", "No hay información disponible"))
        
        # Resúmenes ejecutivos
        st.subheader("Resúmenes Ejecutivos")
        st.write(results.get("resumenes_ejecutivos", "No hay información disponible"))
        
        # Comparación de documentos
        st.subheader("Comparación de Documentos")
        st.write(results.get("comparacion_documentos", "No hay información disponible"))
    
    with col2:
        # Contexto
        st.subheader("Contexto")
        st.write(results.get("contexto", "No hay información disponible"))
        
        # Análisis detallado
        st.subheader("Análisis Detallado")
        st.write(results.get("analisis_detallado", "No hay información disponible"))
        
        # Conclusión
        st.subheader("Conclusión")
        st.write(results.get("conclusion", "No hay información disponible"))

# Interfaz principal
st.title("Centro de Análisis Documentario (Simplificado)")
st.markdown("---")

# Cargar documentos disponibles
with st.spinner("Cargando documentos..."):
    documents = load_available_documents()

# Selector de documentos simplificado
st.subheader("Selección de Documentos")

# Mostrar documentos disponibles
if documents:
    # Crear opciones para el selectbox
    document_options = [f"{doc['name'][:50]}..." for doc in documents]
    selected_option = st.selectbox(
        "Seleccione un documento:",
        ["Seleccione un documento..."] + document_options
    )
    
    # Procesar selección
    if selected_option != "Seleccione un documento...":
        selected_index = document_options.index(selected_option)
        selected_doc = documents[selected_index]
        
        if st.button("Agregar Documento"):
            add_document(selected_doc)
            st.success(f"Documento agregado: {selected_doc['name'][:50]}...")
            st.rerun()
else:
    st.warning("No se pudieron cargar los documentos")

# Mostrar documentos seleccionados
st.subheader("Documentos Seleccionados")
if st.session_state.selected_documents:
    for i, doc in enumerate(st.session_state.selected_documents, 1):
        st.write(f"{i}. {doc['name']}")
    
    if st.button("Limpiar Selección"):
        clear_selection()
        st.rerun()
else:
    st.info("No hay documentos seleccionados")

# Botón para generar análisis
if st.session_state.selected_documents:
    if st.button("Generar Análisis", type="primary"):
        with st.spinner("Procesando análisis..."):
            success, results = analyze_selected_documents(st.session_state.selected_documents)
            
            if success and results:
                # Guardar resultados
                st.session_state.api_results = results
                st.success("¡Análisis completado con éxito!")
                
                # Mostrar información sobre los resultados
                st.write("Tipo de resultados:", type(results))
                if isinstance(results, dict):
                    st.write("Claves en los resultados:", list(results.keys()))
                
                # Procesar resultados
                processed_results = process_results(results)
                
                # Mostrar resultados
                show_results(processed_results)
            else:
                st.error("No se pudo completar el análisis")

# Mostrar resultados si existen y no se acaban de generar
elif 'api_results' in st.session_state and st.session_state.api_results:
    st.subheader("Resultados del último análisis")
    processed_results = process_results(st.session_state.api_results)
    show_results(processed_results)

# Botón para simular resultados (para pruebas)
with st.expander("Opciones de prueba"):
    if st.button("Simular Resultados"):
        # Crear datos de prueba
        test_results = {
            "sections": {
                "introduction": [{"text": "Esta es una introducción de prueba."}],
                "contexto": [{"text": "Este es un contexto de prueba."}],
                "resumenes_ejecutivos": [{"text": "Estos son resúmenes ejecutivos de prueba."}],
                "analisis_detallado": [{"text": "Este es un análisis detallado de prueba."}],
                "comparacion_documentos": [{"text": "Esta es una comparación de documentos de prueba."}],
                "conclusion": [{"text": "Esta es una conclusión de prueba."}]
            }
        }
        
        # Guardar en la sesión
        st.session_state.api_results = test_results
        
        # Procesar y mostrar
        processed_results = process_results(test_results)
        show_results(processed_results)
        
        st.success("Resultados simulados mostrados correctamente")