StegoLSB.py
===========

Esta herramienta nos permite realizar la técnica LSB en imágenes, con la cual podemos ocultar textos (y otras cosas) en los bits menos significativos de la imagen y de forma reciproca, revelarlos

===
Ocultar Información:
  example.png : es la imagen donde se ocultara el secreto
  secret.txt : es el mensaje que queremos incrustar en la imagen
  
>>>python StegoLSB.py -i example.png -l secret.txt  

===
Extraer Información:
  image.png : es la imagen con el texto oculto, con la opción -x se revela

>>>python StegoLSB.py -x -i image.png
