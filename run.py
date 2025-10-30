"""
Archivo de ejecución principal para la aplicación Streamlit.
Uso: streamlit run run.py
"""

import sys
import os

# Agregar directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui.app import main

if __name__ == "__main__":
    main()

