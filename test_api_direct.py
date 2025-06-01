import streamlit as st
import requests
import json
from urllib.parse import urlencode, quote

st.set_page_config(page_title="Test API Directo", layout="wide")

st.title("🔧 Test Directo de API")

# Mostrar configuración
st.markdown("### 📋 Configuración Actual")
col1, col2 = st.columns(2)

with col1:
    st.markdown("**URLs:**")
    st.code(f"""
auth_url: {st.secrets['api']['auth_url']}
documents_url: {st.secrets['api']['documents_url']}
generate_url: {st.secrets['api']['generate_url']}
    """)

with col2:
    st.markdown("**Credenciales:**")
    st.code(f"""
client_id: {st.secrets['cognito']['client_id']}
scope: {st.secrets['cognito']['scope']}
timeout: {st.secrets['api'].get('timeout_seconds', 30)}s
    """)

st.markdown("---")

# Test 1: Obtener Token
if st.button("🔑 Test 1: Obtener Token"):
    with st.spinner("Obteniendo token..."):
        try:
            # Preparar payload
            payload = {
                "grant_type": "client_credentials",
                "scope": st.secrets['cognito']['scope'],
                "client_id": st.secrets['cognito']['client_id'],
                "client_secret": st.secrets['cognito']['client_secret']
            }
            payload_encoded = urlencode(payload, quote_via=quote)
            
            st.info(f"Payload enviado: {payload}")
            
            # Hacer solicitud
            response = requests.post(
                st.secrets['api']['auth_url'],
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                data=payload_encoded,
                timeout=30
            )
            
            st.success(f"Código de respuesta: {response.status_code}")
            
            if response.status_code == 200:
                token_data = response.json()
                token = token_data.get("access_token", "NO TOKEN FOUND")
                st.success(f"✅ Token obtenido: {token[:50]}...")
                st.session_state.test_token = token
                
                # Mostrar respuesta completa
                with st.expander("Ver respuesta completa"):
                    st.json(token_data)
            else:
                st.error(f"Error: {response.text}")
                
        except Exception as e:
            st.error(f"Excepción: {type(e).__name__}")
            st.error(f"Detalle: {str(e)}")
            import traceback
            st.code(traceback.format_exc())

st.markdown("---")

# Test 2: Obtener Documentos
if 'test_token' in st.session_state:
    if st.button("📄 Test 2: Obtener Documentos (requiere token)"):
        with st.spinner("Obteniendo documentos..."):
            try:
                headers = {
                    "Authorization": f"Bearer {st.session_state.test_token}"
                }
                
                st.info(f"URL: {st.secrets['api']['documents_url']}")
                st.info(f"Headers: Authorization: Bearer {st.session_state.test_token[:20]}...")
                
                response = requests.get(
                    st.secrets['api']['documents_url'],
                    headers=headers,
                    timeout=30
                )
                
                st.success(f"Código de respuesta: {response.status_code}")
                
                if response.status_code == 200:
                    documents = response.json()
                    st.success(f"✅ Documentos obtenidos: {len(documents)}")
                    
                    # Mostrar primeros 5 documentos
                    st.markdown("**Primeros 5 documentos:**")
                    for i, doc in enumerate(documents[:5]):
                        st.write(f"{i+1}. {doc}")
                    
                    # Mostrar respuesta completa
                    with st.expander("Ver todos los documentos"):
                        st.json(documents)
                else:
                    st.error(f"Error: {response.text}")
                    
            except Exception as e:
                st.error(f"Excepción: {type(e).__name__}")
                st.error(f"Detalle: {str(e)}")
                import traceback
                st.code(traceback.format_exc())
else:
    st.info("👆 Primero obtén un token con el Test 1")

st.markdown("---")

# Test 3: Verificar imports
if st.button("🔍 Test 3: Verificar Imports"):
    try:
        st.info("Intentando importar módulos...")
        
        # Test import de rest_api
        try:
            from utils.rest_api import DocumentAnalysisAPI, initialize_api_client, load_available_documents
            st.success("✅ utils.rest_api importado correctamente")
            st.write("Funciones disponibles:", [DocumentAnalysisAPI, initialize_api_client, load_available_documents])
        except Exception as e:
            st.error(f"❌ Error importando utils.rest_api: {e}")
        
        # Test import de session
        try:
            from utils.session import initialize_session_state
            st.success("✅ utils.session importado correctamente")
        except Exception as e:
            st.error(f"❌ Error importando utils.session: {e}")
        
        # Test import de components
        try:
            from components.header import render_header
            from components.document_selector import render_document_selector
            from components.analysis_cards import render_analysis_cards
            st.success("✅ Todos los componentes importados correctamente")
        except Exception as e:
            st.error(f"❌ Error importando componentes: {e}")
            
    except Exception as e:
        st.error(f"Error general: {e}")
        import traceback
        st.code(traceback.format_exc())