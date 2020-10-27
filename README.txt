Nota:
Archivo Proyecto3.py funciona con flags por lo que es recomendable ejecutar mediante consola. 
En caso contrario el programa buscara automaticamente el archivo "p3F_1.ass" por lo que no podra ejecutarse de no llamarse asi.

Instrucciones de uso:
Ejecutar el programa mediante consola (python Proyecto3.py) recibe 2 flags opcionales:
--file: Para el archivo assembly a leer. Es necesario agregar la extension del archivo (Ej: --file Correcto.txt)
--output: Para definir el nombre de los archivos de salida (mem y out comparten nombre para evitar ambiguedad)

Ejemplos:
Para leer un archivo particular sin especificar output: 

	python Proyecto3.py --file NombreArchivoALeer.txt

	Leera el archivo y generara el archivo mem (vacio en caso de no definirlas al inicio del codigo) y out. 
	Llamados datos.mem y datos.out.

Para especificar un nombre de salida:

	python Proyecto3.py --file ArchivoALeer.ass --output Output

	En caso de no encontrar problemas los datos quedaran en Output.out y Output.mem

Debido a que ambos flags son opcionales tambien es posible:

	python Proyecto3.py

	Como fue mencionado al principio esto solo buscara al archivo "p3F_1.ass" por lo que para evitar sobreescribir
	este archivo y mayor comodidad se recomienda usar consola. El output quedara como datos.mem y datos.out
	en caso de no encontrar error. 




