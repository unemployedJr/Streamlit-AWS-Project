import streamlit as st

def render_header():
    """Renderiza el encabezado de la aplicación con estilos personalizados."""
    
    # CSS personalizado con la nueva paleta de colores y estilos
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        :root {
            --primary-dark: #2C3E50;
            --secondary-blue: #3498DB;
            --accent-teal: #1ABC9C;
            --text-dark: #34495E;
            --text-light: #7F8C8D;
            --bg-light: #ECF0F1;
            --bg-card: #FFFFFF;
            --border-color: #BDC3C7;
            --success-color: #2ECC71;
            --warning-color: #F39C12;
            --error-color: #E74C3C;
        }

        body {
            font-family: 'Inter', sans-serif;
            color: var(--text-dark);
            background-color: var(--bg-light);
        }

        .main-header {  
            background: linear-gradient(to right, var(--primary-dark), #34495E);
            color: white;
            padding: 1.8rem;
            border-radius: 12px;
            margin-bottom: 2.5rem;
            text-align: center;
            font-size: 2.5rem;
            font-weight: 700;
            font-family: 'Inter', sans-serif;
            letter-spacing: -0.035em;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }
        
        .document-list-container {
            background-color: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            margin: 1rem 0;
            max-height: 350px;
            overflow-y: auto;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        
        .section-card {
            background-color: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 1.5rem;
            margin: 1rem 0;
            min-height: 250px;
            max-height: 450px;
            overflow-y: auto;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        
        .selected-docs-container {
            background-color: #EBF5FB;
            border: 2px solid var(--secondary-blue);
            border-radius: 8px;
            padding: 1.2rem;
            margin: 1rem 0;
            min-height: 120px;
            max-height: 200px;
            overflow-y: auto;
        }
        
        .selected-doc-tag {
            background-color: var(--secondary-blue);
            color: white;
            padding: 0.6rem 1.1rem;
            margin: 0.3rem;
            border-radius: 25px;
            display: inline-block;
            font-size: 0.88rem;
            font-family: 'Inter', sans-serif;
            font-weight: 500;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }
        
        .section-header {
            background-color: var(--primary-dark);
            color: white;
            padding: 0.85rem 1.5rem;
            margin: -1.5rem -1.5rem 1.2rem -1.5rem;
            border-radius: 7px 7px 0 0;
            font-weight: 600;
            text-align: center;
            font-family: 'Inter', sans-serif;
            font-size: 1.2rem;
            letter-spacing: -0.025em;
        }
        
        .content-text {
            font-family: 'Inter', sans-serif;
            font-size: 1.05rem;
            line-height: 1.8;
            color: var(--text-dark);
            text-align: justify;
        }
        
        .section-title {
            font-family: 'Inter', sans-serif;
            font-weight: 700;
            color: var(--primary-dark);
            font-size: 1.35rem;
            margin-bottom: 1.2rem;
            letter-spacing: -0.02em;
        }

        /* Estilos mejorados para botones */
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
            background-color: #288FCA;
            transform: translateY(-1px);
        }

        .stButton > button:active:enabled {
            transform: translateY(0);
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }

        .stButton > button:disabled {
            background-color: #BDC3C7;
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

        /* Estilos para expander */
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

        /* Estilos para mensajes de Streamlit */
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

        /* Estilos para el hr (línea divisoria) */
        hr {
            margin: 2rem 0;
            border: none;
            border-top: 1px solid var(--border-color);
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Encabezado principal con el nuevo estilo
    st.markdown('<div class="main-header">CENTRO DE ANÁLISIS DOCUMENTARIO</div>', unsafe_allow_html=True)
    
    # Descripción
    #st.markdown("""
    #<p style="text-align: center; color: var(--text-light); font-family: 'Inter', sans-serif; font-size: 1.1rem; margin-top: -1.5rem;">
    #Esta herramienta le permite analizar documentos regulatorios utilizando inteligencia artificial.
    #Seleccione los documentos relevantes y genere un análisis completo.
    #</p>
    #""", unsafe_allow_html=True)