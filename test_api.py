import streamlit as st
import requests
from urllib.parse import urlencode, quote
import json

st.title("🧪 Prueba de Conexión API")

# Mostrar configuración
st.header("1️⃣ Configuración")
st.write("**Client ID:**", st.secrets["cognito"]["client_id"])
st.write("**Scope:**", st.secrets["cognito"]["scope"])
st.write("**Auth URL:**", st.secrets["api"]["auth_url"])
st.write("**Documents URL:**", st.secrets["api"]["documents_url"])

# Probar obtención de token
st.header("2️⃣ Prueba de Autenticación")
if st.button("Obtener Token"):
    try:
        payload = {
            "grant_type": "client_credentials",
            "scope": st.secrets["cognito"]["scope"],
            "client_id": st.secrets["cognito"]["client_id"],
            "client_secret": st.secrets["cognito"]["client_secret"]
        }
        payload_encoded = urlencode(payload, quote_via=quote)
        
        st.code(f"Payload: {payload_encoded[:100]}...")
        
        response = requests.post(
            st.secrets["api"]["auth_url"],
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data=payload_encoded,
            timeout=30
        )
        
        st.write(f"**Código de respuesta:** {response.status_code}")
        
        if response.status_code == 200:
            token_data = response.json()
            st.success("✅ Token obtenido exitosamente!")
            st.json(token_data)
            
            # Guardar token en session state
            st.session_state['test_token'] = token_data.get("access_token")
        else:
            st.error(f"❌ Error: {response.status_code}")
            st.text(response.text)
            
    except Exception as e:
        st.error(f"❌ Excepción: {type(e).__name__}")
        st.text(str(e))

# Probar obtención de documentos
st.header("3️⃣ Prueba de Documentos")
if 'test_token' in st.session_state:
    st.success(f"Token disponible: {st.session_state['test_token'][:20]}...")
    
    if st.button("Obtener Documentos"):
        try:
            headers = {
                "Authorization": f"Bearer {st.session_state['test_token']}"
            }
            
            response = requests.get(
                st.secrets["api"]["documents_url"],
                headers=headers,
                timeout=30
            )
            
            st.write(f"**Código de respuesta:** {response.status_code}")
            
            if response.status_code == 200:
                documents = response.json()
                st.success(f"✅ {len(documents)} documentos obtenidos!")
                
                # Mostrar primeros 3 documentos
                for i, doc in enumerate(documents[:3]):
                    st.write(f"**Documento {i+1}:**")
                    st.json(doc)
            else:
                st.error(f"❌ Error: {response.status_code}")
                st.text(response.text)
                
        except Exception as e:
            st.error(f"❌ Excepción: {type(e).__name__}")
            st.text(str(e))
else:
    st.warning("⚠️ Primero obtén un token")

# Información adicional
st.header("4️⃣ Información de Debug")
st.write("**Session State:**")
st.json({k: str(v)[:100] + "..." if len(str(v)) > 100 else v for k, v in st.session_state.items()})