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

## Implementación del BST

Cada nodo tiene como máximo dos hijos. Todos los valores del subárbol izquierdo son menores que el del nodo y todos los del derecho son mayores. Esta propiedad se cumple en cada nodo, no solo en la raíz.

La implementación en `codigo/bst.py` es independiente de Manim y no realiza balanceo automático. El orden de inserción determina la forma del árbol.

- `insertar(valor)` devuelve el nodo insertado. Si el valor ya existe, devuelve el nodo existente sin agregar duplicados.
- `buscar(valor, camino=None)` devuelve el nodo encontrado o `None`. Si se proporciona una lista `camino`, agrega los nodos visitados sin borrar su contenido anterior.
- `eliminar(valor)` devuelve `True` si elimina el valor y `False` si no existe. En el caso de dos hijos, copia el valor del sucesor inorder y retira ese sucesor; el nodo reemplazado conserva su identidad, pero cambia de valor.
- `preorder()`, `inorder()` y `postorder()` devuelven listas de valores. En un árbol vacío devuelven `[]`; inorder devuelve los valores en orden ascendente.

Los valores almacenados deben ser comparables entre sí y tener un orden total coherente. Los ejemplos usan enteros.

### Complejidad

Sea `n` la cantidad de nodos y `h` la altura medida en aristas: una raíz sin hijos tiene altura 0. Se escribe `O(h + 1)` para incluir ese caso; habitualmente se abrevia como `O(h)` al analizar árboles de altura creciente.

| Operación | Tiempo en función de la altura | Con altura logarítmica | Peor caso: árbol degenerado |
| --- | --- | --- | --- |
| Insertar, buscar o eliminar | `O(h + 1)` | `O(log n)` | `O(n)` |
| Recorrer todos los nodos | `O(n)` | `O(n)` | `O(n)` |

El árbol ocupa `O(n)` espacio. La inserción y eliminación iterativas usan `O(1)` espacio auxiliar; la búsqueda también, salvo que se guarde el camino, que ocupa `O(h + 1)`. Los recorridos usan una pila recursiva de `O(h + 1)` y sus listas de resultados ocupan `O(n)`. En árboles muy profundos, los recorridos pueden alcanzar el límite de recursión de Python.

## Pruebas de la estructura de datos

Desde la raíz del proyecto, ejecuta:

```powershell
python -B -m unittest discover -s tests -v
```

Las pruebas usan `unittest`, incluido en Python: no requieren instalar Manim ni generar un video. Si prefieres usar el entorno virtual del proyecto, sustituye `python` por `.\.venv\Scripts\python.exe`.

Se comprueban el árbol vacío, los duplicados, los recorridos, los caminos de búsqueda, las búsquedas fallidas y la eliminación de hojas, raíces y nodos con uno o dos hijos. Se incluyen sucesores con hijo derecho, árboles degenerados y 4 000 operaciones mezcladas con semilla fija, contrastadas con un conjunto de Python. También se verifican los enlaces y la propiedad de orden de todos los subárboles. Estas pruebas validan la lógica del BST; no verifican la presentación de las animaciones.

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
| `tests/test_bst.py` | Pruebas automatizadas del BST, ejecutables sin Manim mediante `unittest`. |
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
