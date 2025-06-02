import streamlit as st
import json
import time

# Configuración de la página - DEBE SER LO PRIMERO
st.set_page_config(
    page_title="Centro de Análisis Documentario",
    layout="wide",
    page_icon="📑"
)

# Mostrar información de depuración para ver la estructura de los resultados
def inspect_api_results():
    """Inspecciona los resultados de la API y muestra información detallada"""
    if 'api_results' in st.session_state and st.session_state.api_results:
        with st.expander("Inspección de Resultados"):
            st.write("Tipo de api_results:", type(st.session_state.api_results))
            st.write("Claves en api_results:", list(st.session_state.api_results.keys()) if isinstance(st.session_state.api_results, dict) else "No es un diccionario")
            
            # Verificar si hay secciones
            if isinstance(st.session_state.api_results, dict) and "sections" in st.session_state.api_results:
                st.write("Claves en sections:", list(st.session_state.api_results["sections"].keys()))
            
            # Mostrar los resultados completos
            st.json(st.session_state.api_results)

# Función para visualizar resultados utilizando componentes básicos de Streamlit
def show_results_basic(results):
    """
    Muestra los resultados utilizando componentes básicos de Streamlit
    sin depender de HTML personalizado.
    """
    st.header("Resultados del Análisis")
    
    # Dividir en dos columnas
    col1, col2 = st.columns(2)
    
    with col1:
        # Introducción
        st.subheader("Introducción")
        intro = results.get("introduction", "No hay información disponible")
        st.write(intro)
        
        # Resúmenes ejecutivos
        st.subheader("Resúmenes Ejecutivos")
        resumenes = results.get("resumenes_ejecutivos", "No hay información disponible")
        st.write(resumenes)
        
        # Comparación de documentos
        st.subheader("Comparación de Documentos")
        comparacion = results.get("comparacion_documentos", "No hay información disponible")
        st.write(comparacion)
    
    with col2:
        # Contexto
        st.subheader("Contexto")
        contexto = results.get("contexto", "No hay información disponible")
        st.write(contexto)
        
        # Análisis detallado
        st.subheader("Análisis Detallado")
        analisis = results.get("analisis_detallado", "No hay información disponible")
        st.write(analisis)
        
        # Conclusión
        st.subheader("Conclusión")
        conclusion = results.get("conclusion", "No hay información disponible")
        st.write(conclusion)

# Procesar la respuesta de la API para extraer las secciones relevantes
def process_api_response(api_response):
    """
    Procesa la respuesta de la API para extraer y formatear las secciones.
    
    Args:
        api_response: Respuesta original de la API
        
    Returns:
        dict: Diccionario con las secciones procesadas
    """
    # Inicializar el diccionario de resultados
    processed_results = {
        "introduction": "No hay información disponible",
        "contexto": "No hay información disponible",
        "resumenes_ejecutivos": "No hay información disponible",
        "analisis_detallado": "No hay información disponible",
        "comparacion_documentos": "No hay información disponible",
        "conclusion": "No hay información disponible"
    }
    
    # Verificar si la respuesta es un diccionario
    if not isinstance(api_response, dict):
        st.error(f"Error: La respuesta de la API no es un diccionario: {type(api_response)}")
        return processed_results
    
    # Verificar si hay una clave 'sections'
    if "sections" in api_response:
        sections = api_response["sections"]
        
        # Procesar cada sección si existe
        for key in processed_results.keys():
            if key in sections:
                # Obtener los textos de la sección
                section_data = sections[key]
                
                if isinstance(section_data, list):
                    # Extraer el texto de cada elemento
                    texts = []
                    for item in section_data:
                        if isinstance(item, dict) and "text" in item:
                            texts.append(item["text"])
                        elif isinstance(item, str):
                            texts.append(item)
                    
                    if texts:
                        processed_results[key] = "\n\n".join(texts)
                
                elif isinstance(section_data, str):
                    processed_results[key] = section_data
    
    # Si no hay 'sections', buscar las claves directamente
    else:
        for key in processed_results.keys():
            if key in api_response:
                section_data = api_response[key]
                
                if isinstance(section_data, list):
                    texts = []
                    for item in section_data:
                        if isinstance(item, dict) and "text" in item:
                            texts.append(item["text"])
                        elif isinstance(item, str):
                            texts.append(item)
                    
                    if texts:
                        processed_results[key] = "\n\n".join(texts)
                
                elif isinstance(section_data, str):
                    processed_results[key] = section_data
    
    return processed_results

# SECCIÓN PRINCIPAL DEL PROGRAMA
st.title("Centro de Análisis Documentario - Solución Directa")
st.markdown("---")

# Botón para simular resultados
if st.button("Simular Resultados de Análisis"):
    # Crear datos de prueba
    sample_results = {
        "sections": {
            "introduction": [{"text": "Esta es una introducción de prueba"}],
            "contexto": [{"text": "Este es un contexto de prueba"}],
            "resumenes_ejecutivos": [{"text": "Estos son resúmenes ejecutivos de prueba"}],
            "analisis_detallado": [{"text": "Este es un análisis detallado de prueba"}],
            "comparacion_documentos": [{"text": "Esta es una comparación de documentos de prueba"}],
            "conclusion": [{"text": "Esta es una conclusión de prueba"}]
        }
    }
    
    # Guardar en la sesión
    st.session_state.api_results = sample_results
    
    # Mostrar mensaje de éxito
    st.success("Datos de prueba generados correctamente")
    
    # Procesar los resultados
    processed_results = process_api_response(sample_results)
    
    # Guardar los resultados procesados
    st.session_state.processed_results = processed_results

# Mostrar la inspección de resultados
inspect_api_results()

# Mostrar los resultados si existen
if 'api_results' in st.session_state and st.session_state.api_results:
    st.markdown("---")
    st.header("Visualización de Resultados")
    
    # Procesar los resultados si no están procesados
    if 'processed_results' not in st.session_state:
        st.session_state.processed_results = process_api_response(st.session_state.api_results)
    
    # Mostrar los resultados procesados
    show_results_basic(st.session_state.processed_results)

# Botón para limpiar la sesión
if st.button("Limpiar Sesión"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.success("Sesión limpiada correctamente")
    st.rerun()