import streamlit as st
from typing import List, Dict, Any
from utils.session import add_document, clear_selection

def render_document_selector():
    """
    Renderiza el selector de documentos y la lista de documentos seleccionados.
    
    Returns:
        List[Dict]: Lista de documentos seleccionados
    """
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown('<div class="section-title">Biblioteca de Documentos</div>', unsafe_allow_html=True)
        
        # Sección de selección de documentos
        st.markdown("---")
        st.markdown("**Selección de Documentos**")
        
        # Obtener documentos disponibles del estado de la sesión
        documents = st.session_state.available_documents or []
        
        if not documents:
            st.warning("No se pudieron cargar los documentos. Por favor, refresque la página.")
        else:
            # Selectbox con todos los documentos
            document_options = [f"{doc['name'][:70]}..." for doc in documents]
             #document_options = [f"{doc['name'][:70]}... ({doc.get('relevance', '100%')})" for doc in documents]
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
                
                # Intentar agregar el documento
                if add_document(selected_doc):
                    st.success(f"✅ Documento agregado: {selected_doc['name'][:50]}...")
                    st.rerun()  # Forzar actualización de la UI
                else:
                    # Documento ya está seleccionado
                    if st.session_state.last_attempted_document == selected_doc['id']:
                        st.warning("⚠️ Este documento ya está seleccionado")

    with col2:
        st.markdown('<div class="section-title">Documentos Seleccionados</div>', unsafe_allow_html=True)
        
        # Área de documentos seleccionados
        if st.session_state.selected_documents:
            st.markdown('<div class="selected-docs-container">', unsafe_allow_html=True)
            selected_names = ""
            for i, doc in enumerate(st.session_state.selected_documents, 1):
                selected_names += f'<span class="selected-doc-tag">{i}. {doc["name"][:50]}...</span> '
            st.markdown(selected_names, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Botón para limpiar selección
            if st.button("Limpiar Selección"):
                clear_selection()
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
    
    # Información de documentos seleccionados (debajo de ambas columnas)
    if st.session_state.selected_documents:
        st.success(f"Total: {len(st.session_state.selected_documents)} documento(s) seleccionado(s)")
    else:
        st.info("Seleccione al menos un documento para generar el análisis")
    
    return st.session_state.selected_documents