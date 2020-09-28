try:
    file = open("Incorrecto.txt", 'r')
except IOError:
    print("No se encontro el archivo")
    exit()

Lineas = file.readlines()
instructions = ["CMP", "JEQ", "JMP","JNE", "JGT", "JLT", "JGE", "JLE", "JCR", "JOV" , "MOV", "SUB", "ADD", "AND", "OR",
                "NOT", "XOR", "SHL", "SHR", "INC", "RST"]
instructions1 =  ["NOT","SHL", "SHR", "INC", "RST"]
numeros = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
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
    print(operation, firstoperand,secondoperand)

    for a in numeros:  # Para que ninguna instruccion empiece con un literal
        if line[1][0] == a and line[0][0] != "J":
            print("Error en la linea {}: {} \tEl primer elemento no puede ser un literal".format(idx + 1, linea, line[0]))
            filecheck = False
            break

    if line[0] not in instructions:
        print("Error en la linea {}: {} \t{} no es una instruccion valida".format(idx + 1, linea, line[0]))
        filecheck = False

    elif line[0][0] == "J" or line[0]== "INC" or line[0]== "RST":
        if "," in line[1]:
            print("Error en la linea {}: {} \tError de sintaxis, {} solo recibe un parametro.".format(idx + 1, linea,line[0]))
            filecheck = False

    elif line[0] == "CMP":
        if line[1] == "B,(A)" or line[1] == "B,A":
            print("Error en la linea {}: {} \tOperacion no soportada".format(idx + 1, linea,line[0]))
            filecheck = False

        #elif firstoperand in numeros:
        #    print("Error en la linea {}: {} \tOperacion no soportada (Lit,Lit)".format(idx + 1, linea,line[0]))
        #    filecheck = False

    elif line[0] == "MOV":
        if line[1][0] == "(" and (line[1].split(","))[0] == "(A)":
           print("Error en la linea {}: {} \tEl primer elemento no puede ser (A)".format(idx + 1, linea, line[0]))
           filecheck = False

    elif line[0] == "":
        if "," in line[1]:
            print("Error en la linea {}: {} \tError de sintaxis, {} solo recibe un parametro.".format(idx + 1, linea, line[0]))
            filecheck = False

    # elif line[0] == "NOT" or line[0] == "SHR" or line[0] == "SHL" or line[0] == "INC" or line[0] == "RST":
    #     if line[1][0] != "(":
    #         print("Error en la linea {}: {} \tOperacion no valida'".format(idx + 1,linea,line[0]))
    #         filecheck = False

        if "," in line[1]:
            print("Error en la linea {}: {} \tError de sintaxis, {} solo recibe un parametro.".format(idx + 1, linea, line[0]))
            filecheck = False

    elif operation == "OR":
        if secondoperand in listaMov or secondoperand[0] == "(A)" or (firstoperand[0] == "(" and secondoperand != ""):
            print("Error en la linea {}: {} \tOperacion no soportada.".format(idx + 1, linea, line[0]))
            filecheck = False

    elif operation == "NOT":
        if secondoperand in numeros or (firstoperand[0] == "(" and secondoperand == "") or secondoperand[0] == "(":
            print("Error en la linea {}: {} \tOperacion no soportada.".format(idx + 1, linea, line[0]))
            filecheck = False

    elif operation == "XOR":
        if line[1] in listaMov or (firstoperand[0] == "(" and secondoperand != ""):
            print("Error en la linea {}: {} \tOperacion no soportada.".format(idx + 1, linea, line[0]))
            filecheck = False

    elif operation == "SHL" or operation == "SHR":
        if (secondoperand in numeros) or (firstoperand[0] == "(" and secondoperand != "") or firstoperand == "(A)":
            print("Error en la linea {}: {} \tOperacion no soportada.".format(idx + 1, linea, line[0]))
            filecheck = False
        try:
            if firstoperand[1] in numeros or secondoperand[0] == "(":
                print("Error en la linea {}: {} \tOperacion no soportada.".format(idx + 1, linea, line[0]))
                filecheck = False
        except:
            pass

    elif operation == "INC" or operation == "RST":
        if firstoperand[0] != "(" or firstoperand == "(A)" or firstoperand in numeros or firstoperand == "A":
            print("Error en la linea {}: {} \tOperacion no soportada.".format(idx + 1, linea, line[0]))
            filecheck = False

    elif operation == "CMP":
        if firstoperand[0] == "(" or secondoperand == "A" or secondoperand == "(A)" or line[1] in listaMov:
            print("Error en la linea {}: {} \tOperacion no soportada.".format(idx + 1, linea, line[0]))
            filecheck = False



if filecheck == False:
    print("\nError: Uno o más errores encontrados a la hora de compilar")

file.close()
