#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
# Copyright 2014 @trackmaze - @killr00t - @_d14m4nt3
#
# <trackmaze@gmail.com> <d14m4nte@gmail.com>
#
#
#Librerias
#####################################
import random						#
import sys							#
import os                           #
from optparse import OptionParser   #
from PIL import Image        		#
#####################################

if "linux" in sys.platform:
	os.system("clear")
elif "win" in sys.platform:
	os.system("cls")

print """
|---------------------------------------------------|
|                   StegoLSB.py                     |
|           .ed$$$$$eec.                            |
|       .e$$$$$$$$$$$$$$$$$$eeeee$$$$$c	            |
|      d$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$c           |
|    .$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$b.         |
|    $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ $b        |
|   d$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$F       |
|  .$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$       |
|  $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$       |
| .$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$**$ ^$$$$       |
| 4 $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$*"     4$$F       |
| 4 '$$$$$$$$$$$$$$$$$$$$$$$$$$$"        4$$        |
| 4  $$$$$$$$$$$$$$$$$$$$$$$$$$$        .$$%        |
| d   $$$$$          $$$$$*$$$$$$c   ..e$$"         |
|-    4$$$$          ^$$$$  *$$$$$F  ^""            |
|     4$$$$          4$$$$ z$$$$$                   |
|     4$$$$          4$$$$ ^$$$P                    |
|     ^$$$$b          $$$$e  F                      |
|---------------------------------------------------|
|                     StegoLSB.py                   |
|  Trackmaze.blogspot.com | d14m4nt3.wordpress.com  |
|        2014/08/05       |  Least Significant Bit  |
|---------------------------------------------------|
"""


def main():

	#datos iniciales
	#################
	flag=1			#
	firma="0100110001010011010000100111001101110100011001010110011101101111"#
	#################
	
	parser = OptionParser()
	parser.add_option("-x", dest="decrypt", action="store_true", help="Extraer mensaje oculto")
	parser.add_option("-i",  dest='image',  help="Imagen a analizar", metavar="<imagen>")
	parser.add_option("-l", dest="text", help="Archivo de texto a esconder", metavar="<archivo text>")
	(opts, args) = parser.parse_args()
	#flag=1

	if opts.decrypt == None:
		flag=0
		if opts.image == None or opts.text == None:
			exit("[+] Error [+] \n[+]Se deben ingresar ambos parametros, ejemplo: \n\nOcultar:\n\t>>>python StegoLSB.py -i example.png -l secret.txt \nExtraer:\n\t>>>python StegoLSB.py -x -i image.png")
	else:
		if opts.image == None:
			exit("[+] Error [+] \n[+]Se debe ingresar un parametro, ejemplo: \n\nOcultar:\n\t>>>python StegoLSB.py -i example.png -l secret.txt \nExtraer:\n\t>>>python StegoLSB.py -x -i image.png")

	try:
		img = Image.open(opts.image)
		print "#Cargando imagen			...[+]"
		im = img.load()
		print "#Indexando imagen			...[+]"
	except:
		exit("[+] Error al abrir la imagen, por favor verifiquelo [+]")


	tamx,tamy = img.size
	rand = random.randrange(100)
	
	if (flag == 0):
		
		info = extractext(opts.text)
		bits = len(info)
		print bits, int2bin(bits)
		info = int2bin(bits)+firma+info

		print "#Ocultando datos 			...[+]"
		
		for x in range (0, tamx):
			for y in range (0, tamy):
				for h in range (0,3):

					if len(info) != 0:
						Alpha = im[x,y][h]
						bAlpha = int2bin(Alpha)
						copy=list(im[x,y])
						copy[h] = int(secret(bAlpha,info[0]),2)
						im[x,y]=tuple(copy)
						info = info[1:]
					else:
						break
						
		print "#\n#Proceso terminado: 		...[+]\n#\n#\tSe ocultaron: \t",bits," bits de informacion\n#\tSe utilizaron: \t",bits/3," pixeles\n"
		print "#Guardando la informacion	...[+]\n#\n#\tImagen Original: \t",opts.image,"\n#\tArchivo Secreto: \t",opts.text,"\n#\tImagen con Secreto: \timgsecret"+str(rand)+".bmp"

		img.save("imgsecret"+str(rand)+".bmp")
		exit()
		
	else:
		img_bin = binImage(im, tamx, tamy)
		search = img_bin.find(firma)

		if search != -1:
			
			print "#Firma Encontrada			...[+]"
			bsize = img_bin[:search]
			size = int(bsize,2)
			img_bin = img_bin[search+len(firma):]
			n = size/8
			salida = ""
			letra = ""
			print "#Extrayendo Datos 			...[+]"
			
			for i in range (0, n):
				letra = img_bin[0:8]
				salida += chr(int(letra,2))
				img_bin=img_bin[8:]
			search_secret(salida, rand)
		else:

			print "#Firma NO Encontrada, se extraera todo	...[+]"
			n=len(img_bin)/8
			size=len(img_bin)
			salida = ""
			letra = ""
			print "#Extrayendo Datos 			...[+]"
			
			for i in range (0, n):
				letra = img_bin[0:8]
				salida += chr(int(letra,2))
				img_bin=img_bin[8:]

			search_secret(salida,rand)
		print "#\n#Proceso terminado: 			...[+]\n#\n#\tSe Extrajeron: \t",size," bits de informacion\n#\tSe utilizaron: \t",size/3," pixeles\n"
		print "#Guardando la informacion		...[+]\n#\n#\tImagen Original: \t",opts.image,"\n#\tSecreto Extraido: \tLSBsecret"+str(rand)+".txt"
	

def search_secret(dato, rand):
	salida=open("LSBsecret"+str(rand)+".txt","a")
	salida.write(dato)
	salida.close()

def binImage(image, m, n):
	print "#Creando Imagen Binaria 		...[+]"
	text_ext=""
	for x in range (0, m):
		for y in range (0, n):
			for h in range (0,3): 
				text_ext += str(int2bin(image[x,y][h]))[-1]
	return text_ext			

def secret(binario, bit):
	lsb = binario[:7]+bit
	return lsb

def int2bin(n): #conversion del entero a binario
	b=bin(n)
	bina=b[2:]
	resto=len(bina)%8
	if (resto!=0):
		bina="0"*(8-resto)+bina
	return bina
    
def extractext(path):	#extrae los datos a esconder
	try:
		archivo = open(str(path),"r")
		datos = archivo.read()
		print "#Cargarndo texto 			...[+]"
		dt_bin = ""
		for x in datos:
			dt_bin += int2bin(ord(x))
		print "#Generando archivo Binario		...[+]"
		return dt_bin
	except:
		exit("[+] Error al abrir el archivo de texto, por favor verifiquelo [+]")


if __name__ == "__main__":		
	main()
