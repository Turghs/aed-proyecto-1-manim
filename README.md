# Proyecto 1 - Animando Estructuras de Datos

## Tema seleccionado

**Binary Search Tree (BST) — Árbol Binario de Búsqueda.**

## Integrantes

- Escobar Hinojosa, Darlene Priyanka
- Luciani Dávila, Itzel Yadira Arellys
- Vasquez de Velasco Quintana, Nicolás Agustín

## Descripción

Animación educativa creada con Manim que muestra cómo funciona un BST y cómo su altura afecta el costo de búsqueda. Las operaciones se ejecutan sobre una implementación real en Python, separada de la representación gráfica. El árbol principal se construye insertando `50, 30, 70, 20, 40, 60, 80`.

## Contenido

- Concepto de BST: valores menores a la izquierda y mayores a la derecha.
- Construcción e inserción paso a paso.
- Búsqueda de un valor.
- Recorridos Preorder, Inorder y Postorder.
- Eliminación de nodos con cero, uno o dos hijos mediante sucesor inorder.
- Efecto de la altura sobre la eficiencia: BST relativamente balanceado frente a degenerado. Un BST común no garantiza búsqueda en `O(log n)`.

## Software requerido

- Git para clonar el repositorio.
- Python con `pip` y `venv`. Manim 0.21.0 requiere Python 3.11 o superior; este proyecto se comprobó con **Python 3.14.3 en Windows**.
- **Manim Community 0.21.0**, instalado mediante `requirements.txt`.
- Visual Studio Code como editor si se desea; no es necesario para renderizar.

Las escenas usan `Text` y figuras de Manim, sin requerir LaTeX. La introducción y los créditos usan Arial; si el sistema no dispone de esa fuente, Pango puede sustituirla y variar ligeramente la presentación.

## Cómo ejecutar el proyecto

Los siguientes comandos se ejecutan en **PowerShell, en Windows**.

### 1. Clonar el repositorio

```powershell
git clone https://github.com/Turghs/aed-proyecto-1-manim.git
```

### 2. Entrar a la carpeta del proyecto

```powershell
cd aed-proyecto-1-manim
```

Ejecuta los comandos restantes desde esta carpeta, donde está `main.py`.

### 3. Crear un entorno virtual

```powershell
python -m venv .venv
```

### 4. Instalar dependencias

Las dependencias están declaradas en `requirements.txt`. Se fija la versión de Manim comprobada en el proyecto.

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

No es necesario activar el entorno: invocar directamente su intérprete evita problemas con la política de ejecución de PowerShell. La instalación necesita acceso a Internet. Si pip debe compilar dependencias nativas y solicita Microsoft Visual C++, instala las herramientas de compilación de C++ de Microsoft y repite la instalación.

### 5. Renderizar el video

Para una prueba rápida en baja calidad:

```powershell
.\.venv\Scripts\python.exe -m manim -ql main.py ProyectoCompleto
```

`-ql` genera un render rápido de 854 × 480 a 15 fps.

Para la versión final en alta calidad:

```powershell
.\.venv\Scripts\python.exe -m manim -qh main.py ProyectoCompleto
```

`-qh` genera 1920 × 1080 a 60 fps y tarda más. Ambas opciones se comprobaron en la ayuda de Manim 0.21.0. El comando de alta calidad está documentado; la verificación del proyecto se realiza con el render de baja calidad.

### 6. Ubicación del video

El archivo se genera bajo:

```text
media/videos/main/<calidad>/ProyectoCompleto.mp4
```

Con la configuración predeterminada, `<calidad>` es `480p15` para `-ql` y `1080p60` para `-qh`. La carpeta puede cambiar si se personalizan la resolución, los fps o la salida de Manim. Puedes abrir el `.mp4` desde VS Code o un reproductor de video.

## Estructura del proyecto

| Archivo | Función |
| --- | --- |
| `main.py` | Define `ProyectoCompleto` y coordina introducción, explicación, contenido técnico y cierre. |
| `codigo/bst.py` | Implementa `Nodo`, `BST`, inserción, búsqueda, recorridos y eliminación sin depender de Manim. |
| `codigo/intro.py` | Presenta el tema con un pequeño árbol animado. |
| `codigo/explicacion.py` | Explica la propiedad de orden de los subárboles. |
| `codigo/algoritmo.py` | Anima inserción y búsqueda, aporta funciones visuales y enlaza las secciones técnicas. |
| `codigo/recorridos.py` | Anima los tres recorridos mediante puntos y secuencias progresivas. |
| `codigo/eliminacion.py` | Ilustra los tres casos de eliminación con BST independientes. |
| `codigo/comparacion.py` | Compara la búsqueda en árboles de distinta altura y explica su costo. |
| `codigo/cierre.py` | Muestra el resumen, la conclusión y los integrantes. |
| `requirements.txt` | Fija la dependencia Manim utilizada. |
| `.gitignore` | Excluye entornos virtuales, cachés y archivos generados. |
| `README.md` | Describe el contenido y las instrucciones de ejecución. |

`.venv/`, `__pycache__/` y `media/` son directorios locales generados y no necesitan incluirse en el repositorio. Los recursos visuales se crean por código; no se necesita copiar un `media/` anterior para ejecutar el proyecto.
