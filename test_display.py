import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="Test de Visualización",
    layout="wide",
    page_icon="🧪"
)

st.title("Prueba de Visualización de Resultados")

# Datos de prueba estáticos
test_results = {
    "introduction": "Esta es una introducción de prueba para verificar que la visualización funciona correctamente.",
    "contexto": "Este es un contexto de prueba para verificar la visualización de esta sección.",
    "resumenes_ejecutivos": "Estos son resúmenes ejecutivos de prueba para verificar la visualización de esta sección.",
    "analisis_detallado": "Este es un análisis detallado de prueba para verificar la visualización de esta sección.",
    "comparacion_documentos": "Esta es una comparación de documentos de prueba para verificar la visualización de esta sección.",
    "conclusion": "Esta es una conclusión de prueba para verificar la visualización de esta sección."
}

# Mostrar datos usando componentes básicos de Streamlit
st.header("Visualización con componentes básicos")

# Dividir en dos columnas
col1, col2 = st.columns(2)

with col1:
    # Introducción
    st.subheader("Introducción")
    st.write(test_results["introduction"])
    
    # Resúmenes ejecutivos
    st.subheader("Resúmenes Ejecutivos")
    st.write(test_results["resumenes_ejecutivos"])
    
    # Comparación de documentos
    st.subheader("Comparación de Documentos")
    st.write(test_results["comparacion_documentos"])

with col2:
    # Contexto
    st.subheader("Contexto")
    st.write(test_results["contexto"])
    
    # Análisis detallado
    st.subheader("Análisis Detallado")
    st.write(test_results["analisis_detallado"])
    
    # Conclusión
    st.subheader("Conclusión")
    st.write(test_results["conclusion"])

# Intenta importar y usar el componente personalizado
st.header("Visualización con componente personalizado")

if st.button("Probar Visualización con Componente Personalizado"):
    try:
        # Importar el componente
        import sys
        import os
        st.write("Directorios en sys.path:", sys.path)
        st.write("Directorio actual:", os.getcwd())
        st.write("Archivos en el directorio components:", os.listdir("components") if os.path.exists("components") else "No existe")
        
        from components.analysis_cards_alternate import render_analysis_cards_simple
        render_analysis_cards_simple(test_results)
        st.success("Visualización con componente alternativo funciona correctamente")
    except Exception as e:
        st.error(f"Error al usar el componente alternativo: {str(e)}")
        import traceback
        st.code(traceback.format_exc())

# Sección para depurar la respuesta de la API
st.header("Depurar respuesta de API")

# Mostrar el último resultado de API si existe
if 'api_results' in st.session_state and st.session_state.api_results:
    st.subheader("Contenido de st.session_state.api_results:")
    st.json(st.session_state.api_results)
else:
    st.info("No hay resultados de API en la sesión actual")

# Botón para simular resultados de API
if st.button("Simular respuesta de API y guardar en session_state"):
    st.session_state.api_results = test_results
    st.success("Datos de prueba guardados en session_state.api_results")
    st.rerun()