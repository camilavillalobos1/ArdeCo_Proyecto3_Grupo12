try:
    file = open("Incorrecto.txt", 'r')
except IOError:
    print("No se encontro el archivo")
    exit()

Lineas = file.readlines()
instructions = ["CMP", "JEQ", "JMP","JNE", "JGT", "JLT", "JGE", "JLE", "JCR", "JOV" , "MOV", "SUB", "ADD", "AND", "OR",
                "NOT", "XOR", "SHL", "SHR", "INC", "RST"]
instructions1 = ["NOT","SHL", "SHR", "INC", "RST"]
notDoubles = ["MOV", "CMP"]
numeros = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9","#00","#01","#03","#04","#05","#06","#07","#08","#09",
           "#0A","#0B","#0C","#0D","#0E","#0F"]
listaMov = ["(A),B", "A,(A)", "A,A", "B,B"]

filecheck =True
for idx, linea in enumerate(Lineas):
    line = linea.split()

    #Quizas sea util para debugear despues
    operation = line[0]
    firstoperand = line[1]
    secondoperand = ""
    if "," in line[1]:
        firstoperand = (line[1].split(","))[0]
        secondoperand = (line[1].split(","))[1]
    print(operation, firstoperand, secondoperand)

    for a in numeros:  # Para que ninguna instruccion empiece con un literal
        if line[1][0] == a and line[0][0] != "J":
            print("Error en la linea {}: {} \tEl primer elemento no puede ser un literal".format(idx + 1, linea, line[0]))
            filecheck = False
            break

    if line[0] not in instructions:
        print("Error en la linea {}: {} \t{} no es una instruccion valida".format(idx + 1, linea, line[0]))
        filecheck = False

    if (secondoperand == "" and firstoperand == "A") or (secondoperand == "" and firstoperand == "A") and operation != "INC":
        print("Error en la linea {}: {} \t{} no es una instruccion valida".format(idx + 1, linea, line[0]))
        filecheck = False

    if line[0] == "ADD" or line[0] == "SUB" or line[0] == "AND":
        if line[1][0] == "(":
            if line[1].strip("(),") in numeros and line[2] != "":
                print("Error en la linea {}: {} \t{} (Dir), algo no es una instruccion valida".format(idx + 1, linea, line[0]))
                filecheck = False
            elif line[1].strip("(),") == "A" or line[1].strip("(),") == "B":
                print("Error en la linea {}: {} \t{} no acepta (A) o (B) como primer parametro".format(idx + 1, linea,
                                                                                                        line[0]))
                filecheck = False
    if line[0] == "MOV" and line[1][0] =="(":
        if line[1].strip("(),") == "B" and line[2] != "A":
            print("Error en la linea {}: {} \tInstruccion invalida.".format(idx + 1, linea)
            filecheck = False

    if ((operation in notDoubles) and (secondoperand == "")):
        print("Error en la linea {}: {} \t{} debe recibir 2 parametros.".format(idx + 1, linea, line[0]))
        filecheck = False

    if (operation not in notDoubles and (operation != "INC") and (firstoperand[0] != "(" and secondoperand == "")):
        print("Error en la linea {}: {} \tCuando {} recibe 1 parametro este debe ser una direccion.".format(idx + 1, linea, line[0]))
        filecheck = False

    if firstoperand[0] == "(" and secondoperand == "(":
        print("Error en la linea {}: {} \tError de sintaxis, {} no se acepta (Dir),(Dir).".format(idx + 1, linea,line[0]))
        filecheck = False

    if line[0] in instructions1:
        if line[1][0] != "(":
            print("Error en la linea {}: {} \tOperacion no valida'".format(idx + 1,linea,line[0]))
            filecheck = False

    if line[0][0] == "J" or line[0]== "INC" or line[0]== "RST":
        if "," in line[1]:
            print("Error en la linea {}: {} \tError de sintaxis, {} solo recibe un parametro.".format(idx + 1, linea,line[0]))
            filecheck = False

    if line[0] == "":
        if "," in line[1]:
            print("Error en la linea {}: {} \tError de sintaxis, {} solo recibe un parametro.".format(idx + 1, linea, line[0]))
            filecheck = False

    if line[0] == "CMP":
        if line[1] == "B,(A)" or line[1] == "B,A":
            print("Error en la linea {}: {} \tOperacion no soportada".format(idx + 1, linea,line[0]))
            filecheck = False

    if line[0] in instructions: #Antes era MOV pero segun yo ninguna intruccion puede empezar con (A)
        if (line[1].split(","))[0] == "(A)":
           print("Error en la linea {}: {} \tEl primer elemento no puede ser (A)".format(idx + 1, linea, line[0]))
           filecheck = False

    if operation == "OR":
        if secondoperand in listaMov or secondoperand[0] == "(A)" or firstoperand[0] == "(" and secondoperand[0] != "(" :
            print("Error en la linea {}: {} \tOperacion no soportada.".format(idx + 1, linea, line[0]))
            filecheck = False

    if operation == "NOT":
        if secondoperand in numeros or (firstoperand[0] == "(" and secondoperand == "") or secondoperand[0] == "(":
            print("Error en la linea {}: {} \tOperacion no soportada.".format(idx + 1, linea, line[0]))
            filecheck = False

    if operation == "XOR":
        if line[1] in listaMov or (firstoperand[0] == "(" and secondoperand != ""):
            print("Error en la linea {}: {} \tOperacion no soportada.".format(idx + 1, linea, line[0]))
            filecheck = False

    if operation == "SHL" or operation == "SHR":
        if secondoperand in numeros or firstoperand == "(A)" or (firstoperand == "(B)" and secondoperand != ""):
            print("Error en la linea {}: {} \tOperacion no soportada.".format(idx + 1, linea, line[0]))
            filecheck = False
        try:
            if firstoperand[1] in numeros or secondoperand[0] == "(":
                print("Error en la linea {}: {} \tOperacion no soportada.".format(idx + 1, linea, line[0]))
                filecheck = False
        except:
            pass

    if operation == "INC" or operation == "RST":
        if firstoperand[0] != "(" or firstoperand == "(A)" or firstoperand in numeros or firstoperand == "A":
            print("Error en la linea {}: {} \tOperacion no soportada.".format(idx + 1, linea, line[0]))
            filecheck = False

    if operation == "CMP":
        if firstoperand[0] == "(" or secondoperand == "A" or secondoperand == "(A)" or line[1] in listaMov :
            print("Error en la linea {}: {} \tOperacion no soportada.".format(idx + 1, linea, line[0]))
            filecheck = False

if filecheck == False:
    print("\nError: Uno o más errores encontrados a la hora de compilar")

file.close()
