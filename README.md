# Gestor de Portapapeles en Python

Esta aplicaci\u00f3n permite mantener un historial del portapapeles y acceder a \u00e9l mediante una combinaci\u00f3n de teclas. Al presionar la combinaci\u00f3n configurada se muestra una ventana emergente con el historial para seleccionar el texto a pegar.

## Requisitos

- Python 3.8 o superior
- Las dependencias listadas en `requeriments.txt`

Instala las dependencias ejecutando:

```bash
pip install -r requeriments.txt
```

## Uso

Ejecuta el archivo principal:

```bash
python main.py
```

Al iniciar, la aplicaci\u00f3n mostrar\u00e1 en consola la combinaci\u00f3n de teclas actual (por defecto `ctrl+shift+h`). Puedes cambiarla en cualquier momento escribiendo `hotkey <nueva combinaci\u00f3n>` en la consola.

Cuando presiones la combinaci\u00f3n configurada se abrir\u00e1 una ventana emergente minimalista cerca del puntero del rat\u00f3n con las entradas del portapapeles. Haz doble clic sobre un elemento para copiarlo y cerrar la ventana. Tambi\u00e9n se cerrar\u00e1 autom\u00e1ticamente al perder el foco.

Para salir del programa escribe `salir` en la consola.

## Estructura del Proyecto

- `controllers/`: contiene la l\u00f3gica que conecta la interfaz con el modelo.
- `models/`: maneja el historial del portapapeles.
- `views/`: interfaz gr\u00e1fica con Tkinter.
- `main.py`: punto de entrada de la aplicaci\u00f3n.
- `requeriments.txt`: dependencias necesarias.

## Licencia

Este proyecto se distribuye bajo los t\u00e9rminos de la licencia MIT.
