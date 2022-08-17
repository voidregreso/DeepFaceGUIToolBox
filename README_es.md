# DeepFace GUI Toolbox



*Léalo en otros idiomas: [Inglés](README.md), [Español](README_es.md), [Francés](README_fr.md), [Portugués Brasileño](README_pt-BR.md), [Árabe](README_ar.md), [Chino Simplificado](README_zh-CN.md).*

### 1. Introducción

> Deepface es un framework ligero en Python para el reconocimiento facial y el análisis de atributos faciales (edad, género, emoción y raza). Es un marco de reconocimiento facial híbrido envuelto con modelos del estado de la técnica. VGG-Face, Google FaceNet, OpenFace, Facebook DeepFace, DeepID, ArcFace, Dlib y SFace.

Sin embargo, el proyecto original sólo contaba con un módulo API y un programa de consola de ejemplo, que no eran cómodos de utilizar y operar; además, como los archivos de modelos correspondientes debían descargarse de Internet para reconocer los rasgos faciales, y estos archivos son muy grandes y sus URL en algunos países (China, Irán, Venezuela ......) están interferidos y bloqueados, desarrollé un programa con una interfaz visual utilizando Python+PyQt5. Soporta las siguientes características: 

- Representar las zonas faciales reconocidas mediante casillas rectangulares; 
- Realice un análisis exhaustivo de la edad, el sexo, la raza y las emociones, donde el análisis de la raza y la expresión puede ser preciso hasta el porcentaje de cada posible resultado de reconocimiento;
- Verificar si dos caras representan a la misma persona, es decir, inferir la similitud con el porcentaje;
- Múltiples opciones de backends de detectores de rostros y modelos de verificación;
- Configuración del proxy para acelerar la descarga de los archivos del modelo (actualmente sólo admite el protocolo HTTP(S), el proxy del protocolo SOCKS aún debe ser estudiado y mejorado);
- Interfaz de usuario fácil de usar.

### 2. Utilización

1. Descargar e instalar Python 3.9;

2. Instalar los paquetes mediante los siguientes comandos:

   ```bash
   pip install deepface dlib configparser urlib3 PyQt5 PyQt5-tools
   ```

3. Ejecutar main.py

Ahora también se está empaquetando el entorno de ejecución de un solo archivo y se liberará a las versiones más adelante.

Si desea rediseñar los archivos de la interfaz de usuario, debe regenerar los archivos de código de inicialización correspondientes después de su edición mediante los siguientes comandos:

```bash
pyuic5 -o ventana.py ventana.ui
```

### 3. Ejemplo de activos de imagen facial

Puse las fotos de caras de las razas correspondientes en cinco carpetas: *asian, black, hispanic, india_arab, white*, donde cada carpeta tiene unas 15 fotos. Pueden utilizarlas libremente para el análisis y las pruebas.

### 4. Captura de interfaz de este software

![](scrshot.jpg)
