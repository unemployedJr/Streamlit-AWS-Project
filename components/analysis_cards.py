import streamlit as st
from typing import Dict, Any

def render_analysis_cards(results: Dict[str, Any]):
    """
    Renderiza los resultados del análisis en tarjetas con el nuevo diseño.
    
    Args:
        results: Resultados procesados del análisis
    """
    st.markdown('<div class="section-title">Resultados del Análisis</div>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Dividir la pantalla en dos columnas
    col1, col2 = st.columns(2)
    
    with col1:
        # Introducción
        intro_content = results.get("introduction", "No hay información de introducción disponible.")
        st.markdown(f"""
        <div class="section-card">
            <div class="section-header">Introducción</div>
            <div class="content-text">{intro_content}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Resumenes ejecutivos
        resumenes_ejecutivos = results.get("resumenes_ejecutivos", "No hay resúmenes ejecutivos disponibles.")
        st.markdown(f"""
        <div class="section-card">
            <div class="section-header">Resúmenes Ejecutivos</div>
            <div class="content-text">{resumenes_ejecutivos}</div>
        </div>
        """, unsafe_allow_html=True)

         # Comparacion_documentos
        comparacion_documentos = results.get("comparacion_documentos", "No hay contenido principal disponible.")
        st.markdown(f"""
        <div class="section-card">
            <div class="section-header">Comparación de Documentos</div>
            <div class="content-text">{comparacion_documentos}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Contexto
        context_content = results.get("contexto", "No hay información de contexto disponible.")
        st.markdown(f"""
        <div class="section-card">
            <div class="section-header">Contexto</div>
            <div class="content-text">{context_content}</div>
        </div>
        """, unsafe_allow_html=True)

        # Análisis detallado
        analisis_detallado = results.get("analisis_detallado", "No hay información de contexto disponible.")
        st.markdown(f"""
        <div class="section-card">
            <div class="section-header">Análisis detallado</div>
            <div class="content-text">{analisis_detallado}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Conclusión
        conclusion_content = results.get("conclusion", "No hay conclusión disponible.")
        st.markdown(f"""
        <div class="section-card">
            <div class="section-header">Conclusión</div>
            <div class="content-text">{conclusion_content}</div>
        </div>
        """, unsafe_allow_html=True)

    # ======= SECCIÓN DE REFERENCIAS CON STREAMLIT NATIVO =======
    st.markdown("---")
    
    # Contenedor principal de referencias
    st.markdown("""
    <div style="background-color: #FFFFFF; border: 1px solid #BDC3C7; border-radius: 8px; padding: 0; margin: 1rem 0; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
        <div style="background-color: #2C3E50; color: white; padding: 0.85rem 1.5rem; margin: 0; border-radius: 7px 7px 0 0; font-weight: 600; text-align: center; font-family: 'Inter', sans-serif; font-size: 1.2rem;">
            📚 Referencias
        </div>
    """, unsafe_allow_html=True)
    
    # Obtener datos de referencias
    referencias_data = results.get("referencias_data", [])
    
    if referencias_data and isinstance(referencias_data, list) and len(referencias_data) > 0:
        # Container para el contenido
        with st.container():
            #st.markdown(f"""
            #<div style="padding: 1rem; background-color: #2C3E50; color: white; text-align: center; font-weight: 600; margin: 0 1.5rem 1.5rem 1.5rem; border-radius: 8px;">
             #   📚 Total de Referencias Encontradas: {len(referencias_data)}
            #</div>
            #""", unsafe_allow_html=True)
            
            # Mostrar cada referencia usando componentes nativos
            for i, ref in enumerate(referencias_data, 1):
                tipo_doc = ref.get('tipo_doc', 'Documento')
                num_interno = ref.get('num_interno_doc', 'N/A')
                area = ref.get('area', 'N/A')
                fecha = ref.get('fecha_emision', 'N/A')
                expediente = ref.get('num_expediente', 'N/A')
                viddoc = ref.get('viddoc', 'N/A')
                
                # Usar un expander para cada referencia
                with st.expander(f"📄 Referencia {i}: {tipo_doc} - N° {num_interno}", expanded=True):
                    
                    # Crear columnas para mostrar la información
                    ref_col1, ref_col2 = st.columns(2)
                    
                    with ref_col1:
                        st.markdown(f"**🏢 Área Emisora:**")
                        st.write(area)
                        
                        st.markdown(f"**📅 Fecha de Emisión:**")
                        st.write(fecha)
                    
                    with ref_col2:
                        st.markdown(f"**📋 N° de Expediente:**")
                        st.write(expediente)
                        
                        st.markdown(f"**🔗 ID del Documento:**")
                        st.code(viddoc)
    else:
        # Mensaje cuando no hay referencias
        with st.container():
            st.markdown("""
            <div style="padding: 3rem; text-align: center; color: #7F8C8D; font-style: italic;">
                📚 No se encontraron referencias en la respuesta del análisis.<br><br>
                <small>Las referencias aparecerán aquí cuando estén disponibles en los resultados del API.</small>
            </div>
            """, unsafe_allow_html=True)
    
    # Cerrar el contenedor principal
    st.markdown("</div>", unsafe_allow_html=True)
