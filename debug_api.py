import streamlit as st
import json
import requests
import traceback

# Configuración de la página
st.set_page_config(
    page_title="Debug API",
    layout="wide",
    page_icon="🔍"
)

st.title("Depurador de API")

# Cargar secretos
try:
    # Mostrar información sobre los secretos (sin revelar valores sensibles)
    st.subheader("1. Configuración de Secretos")
    secrets_loaded = False
    
    try:
        auth_url = st.secrets["api"]["auth_url"]
        documents_url = st.secrets["api"]["documents_url"]
        generate_url = st.secrets["api"]["generate_url"]
        client_id = st.secrets["cognito"]["client_id"]
        
        # No mostrar el client_secret completo por seguridad
        client_secret = st.secrets["cognito"]["client_secret"]
        masked_secret = client_secret[:5] + "..." + client_secret[-5:] if len(client_secret) > 10 else "***"
        
        scope = st.secrets["cognito"]["scope"]
        timeout = st.secrets["api"].get("timeout_seconds", 30)
        
        secrets_data = {
            "auth_url": auth_url,
            "documents_url": documents_url,
            "generate_url": generate_url,
            "client_id": client_id,
            "client_secret": masked_secret,
            "scope": scope,
            "timeout": timeout
        }
        
        st.json(secrets_data)
        secrets_loaded = True
        st.success("✅ Secretos cargados correctamente")
    except Exception as e:
        st.error(f"❌ Error al cargar secretos: {str(e)}")
        st.code(traceback.format_exc())
        
    # Prueba de autenticación
    st.subheader("2. Prueba de Autenticación")
    
    if secrets_loaded and st.button("Probar Autenticación"):
        try:
            from utils.rest_api import DocumentAnalysisAPI
            api_client = DocumentAnalysisAPI()
            
            with st.spinner("Obteniendo token..."):
                token = api_client.get_token()
                
            if token:
                # Mostrar solo los primeros y últimos caracteres del token por seguridad
                masked_token = token[:10] + "..." + token[-10:] if len(token) > 20 else token
                st.success(f"✅ Token obtenido correctamente: {masked_token}")
                st.session_state.api_client = api_client
            else:
                st.error("❌ No se pudo obtener el token")
        except Exception as e:
            st.error(f"❌ Error en la autenticación: {str(e)}")
            st.code(traceback.format_exc())
    
    # Prueba de obtención de documentos
    st.subheader("3. Prueba de Obtención de Documentos")
    
    if 'api_client' in st.session_state and st.button("Obtener Documentos"):
        try:
            with st.spinner("Obteniendo documentos..."):
                documents = st.session_state.api_client.get_documents()
                
            if documents and len(documents) > 0:
                st.success(f"✅ Se obtuvieron {len(documents)} documentos")
                st.dataframe(documents)
                st.session_state.documents = documents
            else:
                st.warning("⚠️ No se encontraron documentos")
        except Exception as e:
            st.error(f"❌ Error al obtener documentos: {str(e)}")
            st.code(traceback.format_exc())
    
    # Prueba de generación de análisis
    st.subheader("4. Prueba de Generación de Análisis")
    
    if 'documents' in st.session_state and len(st.session_state.documents) > 0:
        # Seleccionar documentos para análisis
        options = [f"{doc['name'][:50]}... ({doc['number']})" for doc in st.session_state.documents]
        selected_indices = st.multiselect("Seleccionar documentos para análisis:", options)
        
        if selected_indices and st.button("Generar Análisis de Prueba"):
            # Obtener los documentos seleccionados
            selected_docs = [st.session_state.documents[options.index(idx)] for idx in selected_indices]
            
            try:
                # Extraer números de documentos
                document_numbers = [doc["number"] for doc in selected_docs if "number" in doc and doc["number"]]
                
                st.write(f"Enviando números de documentos: {document_numbers}")
                
                with st.spinner("Generando análisis..."):
                    # Usar la API para generar análisis
                    results = st.session_state.api_client.generate_analysis(document_numbers)
                
                if results:
                    st.success("✅ Análisis generado correctamente")
                    st.json(results)
                    
                    # Guardar resultados en la sesión
                    st.session_state.api_results = results
                    
                    # Procesar resultados para mostrarlos
                    processed_results = st.session_state.api_client.process_analysis_results(results)
                    st.session_state.processed_results = processed_results
                    
                    st.subheader("Resultados procesados:")
                    st.json(processed_results)
                    
                    # Mostrar resultados con el componente alternativo
                    st.subheader("Visualización de resultados:")
                    try:
                        from components.analysis_cards_alternate import render_analysis_cards_simple
                        render_analysis_cards_simple(processed_results)
                    except Exception as viz_error:
                        st.error(f"❌ Error al visualizar resultados: {str(viz_error)}")
                        st.code(traceback.format_exc())
                else:
                    st.error("❌ No se recibieron resultados del análisis")
            except Exception as e:
                st.error(f"❌ Error al generar análisis: {str(e)}")
                st.code(traceback.format_exc())
    else:
        st.info("Primero obtenga documentos para poder generar un análisis")

    # Prueba manual de la API
    st.subheader("5. Prueba Manual de API")
    
    # Campos para prueba manual
    manual_api_url = st.text_input("URL de API:", value=generate_url if 'generate_url' in locals() else "")
    manual_method = st.selectbox("Método:", ["GET", "POST"])
    manual_payload = st.text_area("Payload (JSON):", value='{"document_numbers": ["123456789"]}')
    
    if st.button("Enviar Solicitud Manual") and manual_api_url:
        try:
            # Obtener token si es necesario
            if 'api_client' not in st.session_state:
                from utils.rest_api import DocumentAnalysisAPI
                st.session_state.api_client = DocumentAnalysisAPI()
            
            token = st.session_state.api_client.get_token()
            
            if not token:
                st.error("❌ No se pudo obtener el token para la solicitud manual")
            else:
                # Configurar headers
                headers = {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {token}"
                }
                
                # Hacer la solicitud
                with st.spinner("Enviando solicitud..."):
                    if manual_method == "GET":
                        response = requests.get(manual_api_url, headers=headers, timeout=30)
                    else:
                        response = requests.post(manual_api_url, data=manual_payload, headers=headers, timeout=30)
                
                # Mostrar resultados
                st.subheader("Respuesta:")
                st.write(f"Status Code: {response.status_code}")
                
                try:
                    # Intentar parsear como JSON
                    response_json = response.json()
                    st.json(response_json)
                    
                    # Guardar en la sesión
                    st.session_state.api_results = response_json
                except:
                    # Si no es JSON, mostrar como texto
                    st.text(response.text)
        except Exception as e:
            st.error(f"❌ Error en la solicitud manual: {str(e)}")
            st.code(traceback.format_exc())

except Exception as global_error:
    st.error(f"❌ Error global: {str(global_error)}")
    st.code(traceback.format_exc())