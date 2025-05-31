import streamlit as st
import boto3
import requests
import json

# Configuración de la página
st.set_page_config(
    page_title="Centro de análisis documentario",
    layout="wide",
    page_icon="📑"
)

# CSS personalizado para mejorar la apariencia con nueva paleta de colores y fuente
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    :root {
        --primary-dark: #2C3E50; /* Azul oscuro casi negro */
        --secondary-blue: #3498DB; /* Azul corporativo */
        --accent-teal: #1ABC9C; /* Verde azulado para acentos sutiles */
        --text-dark: #34495E; /* Gris oscuro para texto principal */
        --text-light: #7F8C8D; /* Gris claro para texto secundario */
        --bg-light: #ECF0F1; /* Fondo muy claro */
        --bg-card: #FFFFFF; /* Fondo de tarjetas */
        --border-color: #BDC3C7; /* Color de borde gris */
        --success-color: #2ECC71; /* Verde éxito */
        --warning-color: #F39C12; /* Naranja advertencia */
        --error-color: #E74C3C; /* Rojo error */
    }

    body {
        font-family: 'Inter', sans-serif;
        color: var(--text-dark);
        background-color: var(--bg-light);
    }

    .main-header {  
        background: linear-gradient(to right, var(--primary-dark), #34495E); /* Degradado de azules/grises oscuros */
        color: white;
        padding: 1.8rem; /* Un poco más de padding */
        border-radius: 12px;
        margin-bottom: 2.5rem; /* Más margen inferior */
        text-align: center;
        font-size: 2.5rem; /* Un poco más grande */
        font-weight: 700; /* Más audaz */
        font-family:'Inter',sans-serif;
        letter-spacing: -0.035em; /* Un poco más apretado */
        box-shadow: 0 4px 15px rgba(0,0,0,0.2); /* Sombra más pronunciada */
    }
    
    .document-list-container {
        background-color: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: 8px;
        margin: 1rem 0;
        max-height: 350px; /* Altura máxima para la lista de documentos */
        overflow-y: auto;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1); /* Sombra más suave */
    }
    
    /* Aumento de la altura mínima y máxima de las cards de análisis */
    .section-card {
        background-color: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1rem 0;
        min-height: 250px; /* Aumentado para asegurar espacio para el texto */
        max-height: 450px; /* Aumentado para permitir más contenido antes del scroll */
        overflow-y: auto; /* Permite scroll si el contenido excede la altura máxima */
        box-shadow: 0 2px 8px rgba(0,0,0,0.1); /* Sombra más suave */
    }
    
    .document-item-clickable {
        background-color: var(--bg-card);
        border-bottom: 1px solid #EAECEE; /* Un gris muy suave */
        padding: 1rem 1.2rem; /* Más padding */
        cursor: pointer;
        transition: background-color 0.2s ease;
        font-family: 'Inter', sans-serif;
        font-size: 0.95rem; /* Ligeramente más grande */
        color: var(--text-dark);
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin: 0;
    }
    
    .document-item-clickable:hover {
        background-color: #F8F9F9; /* Gris muy claro al pasar el ratón */
    }
    
    .document-item-clickable:last-child {
        border-bottom: none;
    }
    
    .document-item-clickable:first-child {
        border-radius: 7px 7px 0 0;
    }
    
    .document-item-clickable:last-child {
        border-radius: 0 0 7px 7px;
    }
    
    .selected-docs-container {
        background-color: #EBF5FB; /* Azul muy claro para documentos seleccionados */
        border: 2px solid var(--secondary-blue);
        border-radius: 8px;
        padding: 1.2rem; /* Más padding */
        margin: 1rem 0;
        min-height: 120px;
        max-height: 200px;
        overflow-y: auto;
    }
    
    .selected-doc-tag {
        background-color: var(--secondary-blue);
        color: white;
        padding: 0.6rem 1.1rem; /* Más padding */
        margin: 0.3rem; /* Más margen */
        border-radius: 25px; /* Más redondeado */
        display: inline-block;
        font-size: 0.88rem; /* Ligeramente más grande */
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    
    .section-header {
        background-color: var(--primary-dark); /* Azul oscuro corporativo */
        color: white;
        padding: 0.85rem 1.5rem; /* Más padding */
        margin: -1.5rem -1.5rem 1.2rem -1.5rem;
        border-radius: 7px 7px 0 0;
        font-weight: 600;
        text-align: center;
        font-family: 'Inter', sans-serif;
        font-size: 1.2rem; /* Ligeramente más grande */
        letter-spacing: -0.025em;
    }
    
    .percentage-badge {
        background-color: var(--error-color); /* Rojo para relevancia */
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-weight: 600;
        font-size: 0.85rem;
        font-family: 'Inter', sans-serif;
    }
    
    .content-text {
        font-family: 'Inter', sans-serif;
        font-size: 1.05rem; /* Ligeramente más grande para mejor legibilidad dentro de las cards */
        line-height: 1.8; /* Mayor interlineado para facilitar la lectura de bloques de texto */
        color: var(--text-dark);
        text-align: justify;
    }
    
    .section-title {
        font-family: 'Inter', sans-serif;
        font-weight: 700; /* Más audaz */
        color: var(--primary-dark); /* Color principal */
        font-size: 1.35rem; /* Más grande */
        margin-bottom: 1.2rem;
        letter-spacing: -0.02em;
    }
    
    .info-text {
        font-family: 'Inter', sans-serif;
        color: var(--text-light); /* Gris más claro para info */
        font-size: 0.95rem;
    }

    /* Estilos para los mensajes de Streamlit (info, success, warning) */
    .stAlert {
        font-family: 'Inter', sans-serif !important;
        font-size: 0.95rem !important;
        line-height: 1.5 !important;
        border-radius: 8px !important;
        margin-top: 1rem !important;
        margin-bottom: 1rem !important;
        padding: 1rem !important;
    }

    .stAlert.info {
        background-color: #EBF5FB !important;
        color: var(--secondary-blue) !important;
        border-left: 5px solid var(--secondary-blue) !important;
    }

    .stAlert.success {
        background-color: #EAF7ED !important;
        color: var(--success-color) !important;
        border-left: 5px solid var(--success-color) !important;
    }

    .stAlert.warning {
        background-color: #FCF8EA !important;
        color: var(--warning-color) !important;
        border-left: 5px solid var(--warning-color) !important;
    }

    /* Estilos para botones */
    .stButton > button {
        background-color: var(--secondary-blue);
        color: white;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        border: none;
        transition: background-color 0.2s ease, transform 0.1s ease;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }

    .stButton > button:hover:enabled {
        background-color: #288FCA; /* Un azul ligeramente más oscuro al pasar el ratón */
        transform: translateY(-1px);
    }

    .stButton > button:active:enabled {
        transform: translateY(0);
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }

    .stButton > button:disabled {
        background-color: #BDC3C7; /* Gris para botones deshabilitados */
        color: #ECF0F1;
        cursor: not-allowed;
        box-shadow: none;
    }

    /* Estilos para selectbox */
    .stSelectbox > div > div {
        border-radius: 8px;
        border: 1px solid var(--border-color);
        font-family: 'Inter', sans-serif;
        color: var(--text-dark);
        padding: 0.2rem 0.5rem;
        box-shadow: inset 0 1px 3px rgba(0,0,0,0.05);
    }
    .stSelectbox > label {
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        color: var(--primary-dark);
        margin-bottom: 0.5rem;
    }

    .css-1n74gkb { /* Clase específica del contenedor del selectbox en Streamlit */
        border-radius: 8px;
    }

    .css-1n74gkb > div > div > div {
        font-family: 'Inter', sans-serif;
    }

    /* Estilo para expander */
    .streamlit-expanderHeader {
        background-color: var(--bg-light);
        color: var(--primary-dark);
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        border-radius: 8px;
        border: 1px solid var(--border-color);
        padding: 0.8rem 1.2rem;
        margin-top: 1rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .streamlit-expanderContent {
        background-color: var(--bg-card);
        border: 1px solid var(--border-color);
        border-top: none;
        border-radius: 0 0 8px 8px;
        padding: 1rem 1.2rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        color: var(--text-dark);
        font-family: 'Inter', sans-serif;
        line-height: 1.6;
    }

</style>
""", unsafe_allow_html=True)

# Función para obtener lista de documentos
def get_documents():
    return [
        {"id": "1", "name": "Resolución N° 038-2018 de Superintendencia de Mercados y Valores - Proyecto de Disposiciones para la aplicación del literal c) del artículo 51 de la Ley del Mercado de Valores", "relevance": "100%"},
        {"id": "2", "name": "Resolución N° 042-2019 de Superintendencia de Mercados y Valores - Modificaciones al Reglamento de Ofertas Públicas de Adquisición", "relevance": "85%"},
        {"id": "3", "name": "Directiva N° 001-2020-SMV - Lineamientos para la implementación de sistemas de gestión de riesgos", "relevance": "92%"},
        {"id": "4", "name": "Circular N° 015-2021-SMV - Procedimientos para la autorización de sociedades titulizadoras", "relevance": "78%"},
        {"id": "5", "name": "Resolución N° 025-2022 - Marco normativo para fondos de inversión alternativos", "relevance": "88%"},
        {"id": "6", "name": "Instructivo N° 003-2023-SMV - Requisitos de información para emisores de valores", "relevance": "94%"},
        {"id": "7", "name": "Directiva N° 004-2023 - Estándares de gobierno corporativo para sociedades anónimas abiertas", "relevance": "81%"},
        {"id": "8", "name": "Resolución N° 017-2024 - Disposiciones sobre transparencia en operaciones del mercado secundario", "relevance": "89%"}
    ]

# Función para obtener análisis completo
def get_complete_analysis(doc_ids):
    if not doc_ids:
        return None
    
    return {
        "introduction": "Este análisis comprende un conjunto integral de resoluciones y documentos normativos emitidos por la Superintendencia de Mercados y Valores entre 2018 y 2024. El marco regulatorio analizado abarca desde disposiciones específicas sobre ofertas públicas hasta lineamientos comprehensivos sobre gestión de riesgos y gobierno corporativo. Los documentos seleccionados representan una evolución sistemática del marco normativo peruano, diseñado para fortalecer la integridad, transparencia y eficiencia del mercado de capitales nacional en línea con estándares internacionales.",
        
        "context": "La emisión de estos instrumentos normativos se enmarca en el proceso de modernización y fortalecimiento del sistema financiero peruano iniciado en 2018. La Superintendencia de Mercados y Valores ha implementado una estrategia regulatoria progresiva, respondiendo tanto a las dinámicas del mercado local como a las mejores prácticas internacionales. Este conjunto de disposiciones refleja un enfoque sistémico hacia la supervisión del mercado de valores, incorporando elementos de supervisión basada en riesgos, fortalecimiento del gobierno corporativo y mejora de los mecanismos de protección al inversionista.",
        
        "main_content": "El análisis de los documentos revela cuatro ejes principales de la política regulatoria: Primero, el fortalecimiento de los marcos de gestión de riesgos a través de la implementación de sistemas comprehensivos de identificación, medición y control de riesgos operacionales, de mercado y de crédito. Segundo, la mejora sustancial de los estándares de divulgación de información y transparencia, estableciendo requisitos específicos para emisores y participantes del mercado. Tercero, la modernización de los procedimientos de autorización y supervisión, incorporando criterios de proporcionalidad y eficiencia regulatoria. Cuarto, el fortalecimiento de los estándares de gobierno corporativo, particularmente para sociedades anónimas abiertas, con énfasis en la independencia de directorios y la protección de derechos de accionistas minoritarios.",
        
        "conclusion": "La implementación coordinada de este marco normativo representa un avance significativo en la sofisticación y efectividad de la regulación del mercado de valores peruano. Las disposiciones analizadas demuestran un enfoque balanceado entre el fomento del desarrollo del mercado y la protección de los inversionistas. Se recomienda una implementación gradual con períodos de adaptación apropiados para los participantes del mercado, acompañada de programas de capacitación y asistencia técnica. La supervisión continua de la efectividad de estas medidas será crucial para asegurar el cumplimiento de los objetivos regulatorios sin generar cargas desproporcionadas para los agentes del mercado."
    }

# Función para mostrar el análisis en cards con scroll
def display_analysis_cards(analysis):
    col1, col2 = st.columns(2)
    
    with col1:
        # Introducción
        st.markdown(f"""
        <div class="section-card">
            <div class="section-header">Introducción</div>
            <div class="content-text">{analysis['introduction']}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Contenido Principal
        st.markdown(f"""
        <div class="section-card">
            <div class="section-header">Contenido Principal</div>
            <div class="content-text">{analysis['main_content']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Contexto
        st.markdown(f"""
        <div class="section-card">
            <div class="section-header">Contexto</div>
            <div class="content-text">{analysis['context']}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Conclusión
        st.markdown(f"""
        <div class="section-card">
            <div class="section-header">Conclusión</div>
            <div class="content-text">{analysis['conclusion']}</div>
        </div>
        """, unsafe_allow_html=True)

# Inicializar estado de la sesión
if 'selected_documents' not in st.session_state:
    st.session_state.selected_documents = []

# Nuevo: Agregar seguimiento del último documento intentado
if 'last_attempted_document' not in st.session_state:
    st.session_state.last_attempted_document = None

# Contador para forzar recreación del selectbox
# Este contador se incrementa para cambiar la key del selectbox y resetear su valor
if 'selector_key' not in st.session_state:
    st.session_state.selector_key = 0

# Encabezado principal
st.markdown('<div class="main-header">CENTRO DE ANÁLISIS DOCUMENTARIO</div>', unsafe_allow_html=True)

# Obtener la lista de documentos
documents = get_documents()

# Layout principal
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown('<div class="section-title">Biblioteca de Documentos</div>', unsafe_allow_html=True)
    
    # Sección de selección de documentos
    st.markdown("---")
    st.markdown("**Selección de Documentos**")
    
    # Selectbox con todos los documentos
    document_options = [f"{doc['name'][:70]}... ({doc['relevance']})" for doc in documents]
    
    # La clave del selectbox ahora usa st.session_state.selector_key
    selected_option = st.selectbox(
        "Seleccione un documento para agregar:",
        ["Seleccione un documento..."] + document_options,
        key=f"doc_selector_{st.session_state.selector_key}" # Clave dinámica
    )
    
    # Lógica para procesar la selección
    if selected_option != "Seleccione un documento...":
        # Encontrar el documento seleccionado
        selected_index = document_options.index(selected_option)
        selected_doc = documents[selected_index]
        
        # Verificar si el documento ya está en la lista seleccionada
        is_already_selected = selected_doc['id'] in [d['id'] for d in st.session_state.selected_documents]
        
        if not is_already_selected:
            # Documento no está seleccionado, agregarlo
            st.session_state.selected_documents.append(selected_doc)
            st.session_state.last_attempted_document = selected_doc['id']
            st.success(f"✅ Documento agregado: {selected_doc['name'][:50]}...")
            
            # Incrementar la clave para forzar el reseteo del selectbox en la siguiente ejecución
            st.session_state.selector_key += 1
            st.rerun() # Dispara una re-ejecución para que el selectbox se resetee
        else:
            # Documento ya está seleccionado, mostrar advertencia solo si no es la re-ejecución
            if st.session_state.last_attempted_document != selected_doc['id']:
                 st.warning("⚠️ Este documento ya está seleccionado")
            
            # Actualizar el último documento intentado, incluso si ya estaba seleccionado,
            # para que la próxima selección del MISMO documento dispare la advertencia.
            st.session_state.last_attempted_document = selected_doc['id']


with col2:
    st.markdown('<div class="section-title">Documentos Seleccionados</div>', unsafe_allow_html=True)
    
    # Área de documentos seleccionados con contenido por defecto
    if st.session_state.selected_documents:
        st.markdown('<div class="selected-docs-container">', unsafe_allow_html=True)
        selected_names = ""
        for i, doc in enumerate(st.session_state.selected_documents, 1):
            selected_names += f'<span class="selected-doc-tag">{i}. {doc["name"][:50]}...</span> '
        st.markdown(selected_names, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Botón para limpiar selección
        if st.button("Limpiar Selección"):
            st.session_state.selected_documents = []
            st.session_state.last_attempted_document = None  # Reset del seguimiento
            st.session_state.selector_key += 1  # Cambiar la clave para forzar recreación del selectbox
            st.rerun()
    else:
        # Contenido por defecto cuando no hay documentos seleccionados
        st.info("**Instrucciones:**\n\n1. Revise la lista de documentos disponibles\n2. Use el selector para elegir documentos\n3. Los documentos seleccionados aparecerán aquí\n4. Haga clic en 'Generar Análisis' cuando esté listo")
        
        # Mostrar una preview de qué tipos de análisis se pueden hacer
        with st.expander("ℹ️ Tipos de análisis disponibles"):
            st.write("""
            **Introducción**: Contexto general de los documentos seleccionados
            
            **Contenido Principal**: Análisis detallado de las disposiciones normativas
            
            **Contexto**: Marco temporal y regulatorio de los documentos
            
            **Conclusión**: Recomendaciones y síntesis del análisis
            """)
    

# Información de documentos seleccionados
if st.session_state.selected_documents:
    st.success(f"Total: {len(st.session_state.selected_documents)} documento(s) seleccionado(s)")
else:
    st.info("Seleccione al menos un documento para generar el análisis")

# Botón Generar centrado
col1, col2, col3 = st.columns([2, 1, 2])
with col2:
    generate_clicked = st.button(
        "Generar Análisis",
        disabled=len(st.session_state.selected_documents) == 0,
        help="Generar análisis completo de los documentos seleccionados"
    )

# Mostrar resultados si se hace clic en generar
if generate_clicked and st.session_state.selected_documents:
    with st.spinner("Procesando análisis..."):
        # Simular tiempo de procesamiento
        import time
        time.sleep(2)
        
        selected_ids = [doc['id'] for doc in st.session_state.selected_documents]
        analysis = get_complete_analysis(selected_ids)
        
        if analysis:
            st.markdown("---")
            st.markdown('<div class="section-title">Resultados del Análisis</div>', unsafe_allow_html=True)
            display_analysis_cards(analysis)
            
            # Botón para exportar resultados
            st.markdown("---")
            col1, col2, col3 = st.columns([2, 1, 2])
            with col2:
                if st.button("Exportar Resultados"):
                    st.success("Resultados exportados exitosamente")