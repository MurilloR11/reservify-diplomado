# Reservify

Aplicación web en **Flask** enfocada en la gestión de **reservas y comandas para restaurantes**.  
Actualmente implementa una landing page moderna y responsive que presenta la propuesta del proyecto, stack tecnológico, misión, visión y objetivos.

## Qué incluye el proyecto

### 1. Backend
- **Python + Flask**
  - Punto de entrada: `app.py`
  - Ruta disponible: `/`
  - Renderiza la vista `home.html` con plantillas Jinja2.

### 2. Frontend
- **Plantillas (Jinja2/HTML)**
  - `templates/base.html`: layout base, carga de fuentes, librerías frontend y bloques reutilizables.
  - `templates/home.html`: contenido principal de la landing.

- **Estilos**
  - `static/css/home.css`: estilos completos del sitio (layout, tipografía, componentes, animaciones y responsive).

- **Comportamiento en cliente (JavaScript)**
  - Inicialización de iconos Lucide (`lucide.createIcons()`).
  - Inicialización de animaciones AOS.
  - Script para menú móvil (abrir/cerrar navegación).

## Librerías y recursos usados

### Backend (Python)
- **Flask**: framework web principal.
- **Jinja2**: motor de plantillas (usado por Flask).

### Frontend (CDN)
- **AOS (Animate On Scroll)**  
  `https://unpkg.com/aos@2.3.4/dist/aos.css`  
  `https://unpkg.com/aos@2.3.4/dist/aos.js`

- **Lucide Icons**  
  `https://unpkg.com/lucide@0.468.0/dist/umd/lucide.min.js`

- **Google Fonts (Inter)**  
  `https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap`

## Componentes principales de UI

- Header fijo con navegación.
- Hero section con CTA e indicadores visuales.
- Sección “Qué es” con tarjetas de funcionalidades.
- Sección “Stack” con grid de tecnologías.
- Sección “Misión y visión”.
- Sección de objetivo general y objetivos específicos.
- Footer institucional.
- Menú responsive para dispositivos móviles.

## Íconos usados (Lucide)

- `arrow-down`
- `chevron-down`
- `code-2`
- `flask-conical`
- `file-code`
- `palette`
- `braces`
- `layers`
- `database`
- `target`
- `eye`

## Estructura del proyecto

```text
reservify-diplomado/
├── app.py
├── templates/
│   ├── base.html
│   └── home.html
├── static/
│   └── css/
│       └── home.css
└── venv/
```

## Cómo ejecutar el proyecto

1. Crear y activar entorno virtual (opcional si ya usas `venv/`):
   - Windows (PowerShell):
     ```powershell
     .\venv\Scripts\Activate.ps1
     ```
2. Instalar dependencias:
   ```bash
   pip install flask
   ```
3. Ejecutar la app:
   ```bash
   python app.py
   ```
4. Abrir en navegador:
   - `http://127.0.0.1:5000`

---

Proyecto base orientado a evolucionar hacia una plataforma completa de operación para restaurantes.
