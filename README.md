# El Código Penal en JSON 

Just for fun!

# How-to

Para obtener un nuevo conjunto de datos primero tienes que descargar el documento desde la página oficial del BOE

https://www.boe.es/buscar/act.php?id=BOE-A-1995-25444

Selecciona la opción "Solo Texto" para visualizar el Código Penal en formato de texto plano y copialo en un fichero llamado cp.txt desde que empieza la introducción ("JUAN CARLOS I") hasta el final ("FELIPE GONZÁLEZ MÁRQUEZ")
El salto de linea recomendado es LF.

Luego ejecuta el script:

```
pip install networkx
pip install flask
python cpgraph.py
```

Esto creará un fichero graph.json con la estructura de nodos y aristas que se puede visualizar automaticamente en cuanto termine el script en http://127.0.0.1:8000
También se creará un fichero elements.json con la estructura de objetos usada para crear la anterior.

# FAQ

### ¿Cómo me aseguro de que no se pierde ni una coma en el proceso?

El script muestra el numero de caracteres que se han transformado en objetos. La suma sería:

```#caracteres en cp.txt = #caracteres en nombre + #caracteres en lineas + #lineas del fichero```

Ej.: en la actualización del 23/12/2022 hay 672009 caracteres tras copiar el texto a un fichero.
Tras pasar el texto a objetos el numero de caracteres se mantiene igual. Si hubiera alguna discrepacia el script avisaría de ello.

### ¿Qué pasa con los artículos 445 y 562 que no me los pone donde deberían estar?

Que empiezan llamandose "Disposición" y se confunden con los elementos de tipo Disposición que hay al final.
Se necesita un arreglo manual en el texto.

### Los UUIDs se cambian en cada ejecución

Esto no es un sistema de control de versiones, esto es solo para extraer el texto del BOE y volcarlo en un objeto.

