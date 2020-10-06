
try:
    file = open("p3_1-correccion2.ass", 'r') #Abre archivo de texto con assembly
except IOError:
    print("No se encontro el archivo")
    exit()


file1 = open("datos1.txt", 'w')



Lineas = file.readlines()
instructions = ["CMP", "JEQ", "JMP","JNE", "JGT", "JLT", "JGE", "JLE", "JCR", "JOV" , "MOV", "SUB", "ADD", "AND", "OR",
                "NOT", "XOR", "SHL", "SHR", "INC", "RST"]
instructions1 = ["SHL", "SHR", "INC", "RST"]
notDoubles = ["MOV", "CMP"]
numeros = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9","#00","#01","#03","#04","#05","#06","#07","#08","#09",
           "#0A","#0B","#0C","#0D","#0E","#0F"]
listaMov = ["(A),B", "A,(A)", "A,A", "B,B"]


binario = {'MOV A,B' : '0000000',
                    'MOV B,A':'0000001',

                    'ADD A,B':'0000100',
                    'ADD B,A':'0000101',

                    'SUB A,B':'0001000',
                    'SUB B,A':'0001001',

                    'AND A,B':'0001100',
                    'AND B,A':'0001101',

                    'OR A,B':'0010000',
                    'OR B,A':'0010001',

                    'NOT A,A':'0010100',
                    'NOT A,B':'0010101',
                    'NOT B,A':'0010110',
                    'NOT B,B':'0010111',
                    'XOR A,A':'0011000',
                    'XOR B,A':'0011001',

                    'SHL A,A':'0011100',
                    'SHL A,B':'0011101',
                    'SHL B,A':'0011110',
                    'SHL B,B':'0011111',
                    'SHR A,A':'0100000',
                    'SHR A,B':'0100001',
                    'SHR B,A':'0100010',
                    'SHR B,B':'0100011',
                    'INC B':'0100100'}

binario_literal = {'MOV A':'0000010',
                    'MOV B':'0000011',
                    'ADD A':'0000110',
                    'ADD B':'0000111',
                    'SUB A':'0001010',
                    'SUB B':'0001011',
                    'AND A':'0001110',
                    'AND B':'0001111',
                    'OR A':'0010010',
                    'OR B':'0010011',
                    'XOR A':'0011010',
                    'XOR B':'0011011',
                    }

literales = {'0':'00000000'}



filecheck = True
for idx, linea in enumerate(Lineas):
    
    line = linea.split()

    
    linea = linea.strip()
    
    operation = line[0]
    firstoperand = line[1]
    secondoperand = ""
    if "," in line[1]:
        firstoperand = (line[1].split(","))[0]
        secondoperand = (line[1].split(","))[1]
    print(operation, firstoperand, secondoperand)
    


    #Quizas sea util para debugear despues

    

                

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
            if secondoperand[0] != "(" and secondoperand != "A" and secondoperand != "B":
                if secondoperand[0] == "#":
                    num = int("0x" + secondoperand.strip("#\n"), 0)
                else:
                    num = int(secondoperand, 0)
                if num > 256:
                    print("Error en la linea {}: {} \tEl literal excede el valor aceptado.".format(idx + 1, linea))
                    filecheck = False
            if line[1][1] in numeros:
                print("Error en la linea {}: {} \t{} (Dir), algo no es una instruccion valida".format(idx + 1, linea, line[0]))
                filecheck = False
            if line[1].strip("(),") in numeros and line[2] != "":
                print("Error en la linea {}: {} \t{} (Dir), algo no es una instruccion valida".format(idx + 1, linea, line[0]))
                filecheck = False
            if line[1].strip("(),") == "A" or line[1].strip("(),") == "B":
                print("Error en la linea {}: {} \t{} no acepta (A) o (B) como primer parametro".format(idx + 1, linea,line[0]))
                filecheck = False


    if line[0] == "MOV" and line[1][0] == "(":
        if line[1].strip("(),") == "B" and line[2] != "A":
            print("Error en la linea {}: {} \tInstruccion invalida.".format(idx + 1, linea))
            filecheck = False

    if line[0] == "MOV":
        if secondoperand[0] != "(" and secondoperand != "A" and secondoperand != "B":
            if secondoperand[0] == "#":
                num = int("0x" + secondoperand.strip("#\n"), 0)
            else:
                num = int(secondoperand, 0)
            if num > 256:
                print("Error en la linea {}: {} \tEl literal excede el valor aceptado.".format(idx + 1, linea))
                filecheck = False

    if ((operation in notDoubles) and (secondoperand[0] == "")):
        print("Error en la linea {}: {} \t{} debe recibir 2 parametros.".format(idx + 1, linea, line[0]))
        filecheck = False

    if firstoperand[0] == "(" and secondoperand == "(":
        print("Error en la linea {}: {} \tError de sintaxis, {} no se acepta (Dir),(Dir).".format(idx + 1, linea,line[0]))
        filecheck = False

    if line[0] in instructions1:
        if line[1][0] != "(":
            print("Error en la linea {}: {} \tOperacion no valida".format(idx + 1,linea,line[0]))
            filecheck = False

    if line[0][0] == "J" or line[0]== "INC" or line[0]== "RST":
        if firstoperand != "A" and firstoperand != "B" and firstoperand[0] != "(":
            if firstoperand[0] == "#":
                num = int("0x" + firstoperand.strip("#\n"), 0)
            else:
                num = int(firstoperand, 0)
            if num > 256:
                print("Error en la linea {}: {} \tEl literal excede el valor aceptado.".format(idx + 1, linea))
                filecheck = False
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
        if secondoperand[0] != "(" and secondoperand != "A" and secondoperand != "B":
            if secondoperand[0] == "#":
                num = int("0x" + secondoperand.strip("#\n"), 0)
            else:
                num = int(secondoperand, 0)
            if num > 256:
                print("Error en la linea {}: {} \tEl literal excede el valor aceptado.".format(idx + 1, linea))
                filecheck = False
        if secondoperand in listaMov or secondoperand[0] == "(A)" or firstoperand[0] == "(" and secondoperand[0] != "(" :
            print("Error en la linea {}: {} \tOperacion no soportada.".format(idx + 1, linea, line[0]))
            filecheck = False

    if operation == "NOT":
        if secondoperand in numeros or (firstoperand[0] == "(" and secondoperand == "") or secondoperand[0] == "(":
            print("Error en la linea {}: {} \tOperacion no soportada.".format(idx + 1, linea, line[0]))
            filecheck = False

    if operation == "XOR":
        if secondoperand[0] != "(" and secondoperand != "A" and secondoperand != "B":
            if secondoperand[0] == "#":
                num = int("0x" + secondoperand.strip("#\n"), 0)
            else:
                num = int(secondoperand, 0)
            if num > 256:
                print("Error en la linea {}: {} \tEl literal excede el valor aceptado.".format(idx + 1, linea))
                filecheck = False
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
            
    

    


if filecheck:
    print("\nCompilación realizada con exito")
else:
    print("\nError: Uno o más errores encontrados a la hora de compilar")
#direccion out of bound
#MOV literales

#META 2
if filecheck:
    for idx, linea in enumerate(Lineas):
        linea = linea.strip()
        line = linea.split(",")
        print("Esta es la linea " + linea)
        if linea in binario:
            print("\tSi esta")
            #print(binario[linea]+"00000000")
            #print("La linea es: " + linea + " y en binario es: " + binario[linea])
            file1.write(binario[linea] + "00000001" + "\n")

        if linea not in binario:
            if line[0] in binario_literal:
                if line[1][0] != "(":
                    #print("\tSi esta en dic literal "+"{0:b}".format(int(line[1])))
                    file1.write(binario_literal[line[0]]+"{0:08b}".format(int(line[1]))+"\n")
                else:
                    print("\tNo implementado para meta 2")
            else:
                print("\tNo implementado para meta 2")
           # for a in numeros:
                #if operation == "MOV" and firstoperand == "A":
                    #file1.write(binario_literal['MOV A,Lit'] + literales["'" + a + "'"] + "\n")




        

    



      


file.close()
file1.close()
