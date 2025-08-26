# Chatbot con Streamlit y Ollama

Este proyecto es un chatbot desarrollado en Python utilizando **Streamlit** para la interfaz web y **Ollama** para el modelo de lenguaje.

---

## 🛠 Requisitos

- Python 3.9 o superior
- Entorno virtual recomendado (`venv`)
- Ollama instalado y funcionando

---

## Instalación

1. **Clonar el repositorio** (si aplica):
```bash
git clone <URL-del-repositorio>
cd <nombre-del-proyecto>
```
2. **Crear un entorno virtual** (opcional pero recomendado):
```bash
python -m venv .venv
```
3. **Activar el entorno virtual**:

PowerShell:
```bash
.venv\Scripts\Activate.ps1
```
CMD:
```bash
.venv\Scripts\activate.bat
```
Git Bash / Unix:
```bash
source .venv/Scripts/activate
```
4. **Instalar las librerías necesarias**:
```bash
pip install streamlit ollama
```
---
## Uso

1. **Levantar el servidor de Ollama** (debe estar corriendo antes de usar el chatbot):
```bash
ollama serve
```
2. **Ejecutar la aplicación de Streamlit**:
```bash
streamlit run app.py
```
---
## Desactivar entorno virtual
```bash
deactivate
```
