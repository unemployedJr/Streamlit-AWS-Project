import streamlit as st
import requests
import json
import time
import re
from typing import Dict, Any, List, Optional, Tuple
from urllib.parse import urlencode, quote

class DocumentAnalysisAPI:
    """
    Cliente para comunicarse con el API REST para análisis de documentos.
    Maneja la autenticación con Cognito y las solicitudes al API Gateway.
    """
    
    def __init__(self):
        """Inicializa el cliente API."""
        # URLs de los endpoints (desde secrets)
        self.auth_url = st.secrets["api"]["auth_url"]  # URL completa para obtener token
        self.documents_url = st.secrets["api"]["documents_url"]  # URL para obtener documentos
        self.generate_url = st.secrets["api"]["generate_url"]  # URL para generar análisis
        
        # Credenciales de autenticación
        self.client_id = st.secrets["cognito"]["client_id"]
        self.client_secret = st.secrets["cognito"]["client_secret"]
        self.scope = st.secrets["cognito"]["scope"]  # "poc-smv-genai-api/write poc-smv-genai-api/read"
        
        # Estado de la autenticación
        self.token = None
        self.token_expiry = 0  # Timestamp de expiración
        
        # Configuración de timeout
        self.timeout = st.secrets["api"].get("timeout_seconds", 30)
    
    def get_token(self) -> Optional[str]:
        """
        Obtiene un token de acceso de Cognito. Si ya existe un token válido,
        lo devuelve directamente, de lo contrario solicita uno nuevo.
        
        Returns:
            str: Token de acceso o None si falla la obtención
        """
        # Verificar si ya tenemos un token válido (con margen de 5 minutos)
        current_time = time.time()
        if self.token and current_time < (self.token_expiry - 300):
            return self.token
        
        # Si no hay token o está a punto de expirar, obtener uno nuevo
        try:
            # Preparar payload para la solicitud de token
            payload = {
                "grant_type": "client_credentials",
                "scope": self.scope,
                "client_id": self.client_id,
                "client_secret": self.client_secret
            }
            payload=urlencode(payload, quote_via = quote)
            
            # Hacer la solicitud para obtener el token
            response = requests.request('POST',
                self.auth_url,
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                data=payload,
                timeout=self.timeout
            )
            
            # Verificar si la solicitud fue exitosa
            if response.status_code == 200:
                token_data = response.json()
                self.token = token_data.get("access_token")
                
                # Calcular la expiración (restar 5 minutos para ser conservadores)
                expires_in = token_data.get("expires_in", 3600)  # Default 1 hora
                self.token_expiry = current_time + expires_in
                
                return self.token
            else:
                st.error(f"Error al obtener token: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            st.error(f"Error en la autenticación: {str(e)}")
            return None
    
    def get_documents(self) -> List[Dict[str, str]]:
        """
        Obtiene la lista de documentos disponibles desde el API.
        
        Returns:
            List[Dict]: Lista de documentos con id y nombre
        """
        # Obtener token de acceso
        token = self.get_token()
        if not token:
            st.error("No se pudo obtener el token de autenticación.")
            return []
        
        try:
            # Configurar headers con el token Bearer
            headers = {
                "Authorization": f"Bearer {token}"
            }
            
            # Realizar la solicitud GET al API
            response = requests.request('GET',
                self.documents_url,
                headers=headers,
                timeout=self.timeout
            )
            
            # Verificar si la solicitud fue exitosa
            if response.status_code == 200:
                documents_data = response.json()
                
                # Procesar los documentos recibidos
                processed_documents = []
                for doc in documents_data:
                    # Usar NUM_INTERNO_DOC como ID principal
                    #doc_id = doc.get("NUM_INTERNO_DOC", "")
                    doc_name = doc.get("NOMBRE_DOCUMENTO", "")
                    doc_id = self._extract_document_number(doc_name)
                    # Extraer el número del documento del nombre para el campo "number"
                    doc_number = self._extract_document_number(doc_name)
                    
                    # Si por alguna razón no hay NUM_INTERNO_DOC, usar el número extraído
                    if not doc_id:
                        doc_id = doc_number if doc_number else f"doc_{len(processed_documents)}"
                    
                    processed_documents.append({
                        "id": doc_id,
                        "name": doc_name,
                        "number": doc_number,
                    })
                
                return processed_documents
            else:
                st.error(f"Error al obtener documentos: {response.status_code} - {response.text}")
                return []
                
        except Exception as e:
            st.error(f"Error al obtener documentos: {str(e)}")
            return []
    
    def _extract_document_number(self, doc_name: str) -> str:
        """
        Extrae el número del documento del nombre.
        
        Args:
            doc_name: Nombre completo del documento
            
        Returns:
            str: Número del documento extraído
        """
        # Extraer el número al inicio del nombre del documento
        # Ejemplo: "2020029582 - RSASCM 074 ICCGSA.docx" -> "2020029582"
        match = re.match(r"^(\d+)", doc_name)
        if match:
            return match.group(1)
        return ""
    
    def generate_analysis(self, document_numbers: List[str]) -> Optional[Dict[str, Any]]:
        """
        Solicita el análisis de los documentos seleccionados.
        
        Args:
            document_numbers: Lista de números de documentos seleccionados
            
        Returns:
            Dict: Resultados del análisis o None si hay error
        """
        # Obtener token de acceso
        token = self.get_token()
        if not token:
            st.error("No se pudo obtener el token de autenticación.")
            return None
        
        try:
            # Preparar payload para la solicitud
            payload = json.dumps({
                "document_numbers": document_numbers
            })
            
            # Configurar headers con el token Bearer
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            }
            
            # Realizar la solicitud POST al API
            response = requests.request('POST',
                self.generate_url,
                data=payload,
                headers=headers,
                timeout=self.timeout
            )
            
            # Verificar si la solicitud fue exitosa
            if response.status_code == 200:
                return response.json()
            else:
                error_msg = f"Error al solicitar análisis: {response.status_code}"
                try:
                    error_detail = response.json()
                    error_msg += f" - {json.dumps(error_detail)}"
                except:
                    error_msg += f" - {response.text}"
                
                st.error(error_msg)
                return None
                
        except requests.exceptions.Timeout:
            st.error(f"Tiempo de espera agotado al solicitar análisis.")
            return None
        except requests.RequestException as e:
            st.error(f"Error de conexión: {str(e)}")
            return None
        except Exception as e:
            st.error(f"Error inesperado: {str(e)}")
            return None
    
    def process_analysis_results(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Procesa los resultados del análisis para mostrarlos en la UI.
        
        Args:
            results: Resultados del análisis
            
        Returns:
            Dict: Resultados procesados con las secciones para mostrar
        """
        # Inicializar estructura de resultados procesados
        processed_results = {
            "introduction": "",
            "contexto": "",
            "resumenes_ejecutivos":"",
            "analisis_detallado":"",
            "comparacion_documentos":"",
            "conclusion": ""
        }
        
        # Procesar las secciones según la estructura de la Fig4
        if "sections" in results:
            sections = results["sections"]
            
            # Procesar introducción
            if "introduction" in sections and len(sections["introduction"]) > 0:
                intro_texts = []
                for intro_item in sections["introduction"]:
                    if "text" in intro_item:
                        intro_texts.append(intro_item["text"])
                processed_results["introduction"] = "\n\n".join(intro_texts)
            
            # Procesar contexto (si existe)
            if "contexto" in sections and len(sections["contexto"]) > 0:
                context_texts = []
                for context_item in sections["contexto"]:
                    if "text" in context_item:
                        context_texts.append(context_item["text"])
                processed_results["contexto"] = "\n\n".join(context_texts)
            
            # Procesar contenido principal (si existe)
            if "resumenes_ejecutivos" in sections and len(sections["resumenes_ejecutivos"]) > 0:
                main_texts = []
                for main_item in sections["resumenes_ejecutivos"]:
                    if "text" in main_item:
                        main_texts.append(main_item["text"])
                processed_results["resumenes_ejecutivos"] = "\n\n".join(main_texts)

                     # Procesar contenido principal (si existe)
            if "analisis_detallado" in sections and len(sections["analisis_detallado"]) > 0:
                main_texts = []
                for main_item in sections["analisis_detallado"]:
                    if "text" in main_item:
                        main_texts.append(main_item["text"])
                processed_results["analisis_detallado"] = "\n\n".join(main_texts)

                     # Procesar contenido principal (si existe)
            if "comparacion_documentos" in sections and len(sections["comparacion_documentos"]) > 0:
                main_texts = []
                for main_item in sections["comparacion_documentos"]:
                    if "text" in main_item:
                        main_texts.append(main_item["text"])
                processed_results["comparacion_documentos"] = "\n\n".join(main_texts)
            
            # Procesar conclusión (si existe)
            if "conclusion" in sections and len(sections["conclusion"]) > 0:
                conclusion_texts = []
                for conclusion_item in sections["conclusion"]:
                    if "text" in conclusion_item:
                        conclusion_texts.append(conclusion_item["text"])
                processed_results["conclusion"] = "\n\n".join(conclusion_texts)
        
        return processed_results

# Funciones para inicializar y utilizar en la aplicación

def initialize_api_client():
    """
    Inicializa el cliente de API y lo almacena en el estado de la sesión.
    Debe llamarse al inicio de la aplicación.
    """
    if 'api_client' not in st.session_state:
        st.session_state.api_client = DocumentAnalysisAPI()

def load_available_documents():
    """
    Carga la lista de documentos disponibles y la almacena en el estado de la sesión.
    
    Returns:
        List[Dict]: Lista de documentos disponibles
    """
    # Verificar si ya tenemos documentos cargados y válidos
    if 'available_documents' in st.session_state and st.session_state.available_documents is not None and len(st.session_state.available_documents) > 0:
        return st.session_state.available_documents
    
    # Obtener documentos del API
    api_client = st.session_state.get('api_client')
    if not api_client:
        api_client = DocumentAnalysisAPI()
        st.session_state.api_client = api_client
    
    documents = api_client.get_documents()
    
    if documents:
        st.session_state.available_documents = documents
        return documents
    else:
        st.session_state.available_documents = []
        return []

def analyze_selected_documents(selected_docs: List[Dict[str, Any]]) -> Tuple[bool, Optional[Dict[str, Any]]]:
    """
    Envía los documentos seleccionados para análisis y procesa los resultados.
    
    Args:
        selected_docs: Lista de documentos seleccionados
        
    Returns:
        Tuple[bool, Dict]: (éxito, resultados procesados)
    """
    if not selected_docs:
        st.warning("Seleccione al menos un documento para analizar.")
        return False, None
    
    # Extraer números de documentos
    document_numbers = [doc["number"] for doc in selected_docs if "number" in doc]
    
    if not document_numbers:
        st.warning("Los documentos seleccionados no tienen números válidos.")
        return False, None
    
    # Enviar solicitud de análisis
    api_client = st.session_state.api_client
    results = api_client.generate_analysis(document_numbers)
    
    if results:
        # Procesar resultados para mostrarlos en la UI
        processed_results = api_client.process_analysis_results(results)
        return True, processed_results
    else:
        return False, None