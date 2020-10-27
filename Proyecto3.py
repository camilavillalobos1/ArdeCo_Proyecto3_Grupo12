import argparse

def test():
    a = linea.index("(") + 1
    b = linea.index(")")
    a = linea[a:b]
    test_variables.append(a)
    return a

def ToBinary(a):
    if "#" in a:
        a = a.strip("#")
        a = int("0x" + a, 0)
    a = "{0:08b}".format(int(a))
    return a

parser = argparse.ArgumentParser()
parser.add_argument("--file", help="Assembly file to read", default = "p3F_1.ass")
parser.add_argument("--output", help="Output file written in binary", default = "datos")
args = parser.parse_args()
try:
    file = open(args.file, 'r') #Abre archivo de texto con assembly
except IOError:
    print("[!] No se encontro el archivo")
    exit()
file1 = open(args.output+".out", 'w')
file2 = open(args.output+".mem", 'w')

Lineas = file.readlines()
Code = []
Data = []
if "CODE:\n" in Lineas:
    a = Lineas.index("CODE:\n")
    for index, i in enumerate(Lineas):
        if index < a:
            Data.append(i.strip())
        else:
            Code.append(i.strip())
    Data.pop(0)
    Code.pop(0)
else:
    Code = Lineas[:]
instructions = ["CMP", "JEQ", "JMP","JNE", "JGT", "JLT", "JGE", "JLE", "JCR", "JOV" , "MOV", "SUB", "ADD", "AND", "OR","NOT", "XOR", "SHL", "SHR", "INC", "RST"]
instructions1 = ["SHL", "SHR", "INC", "RST"]
notDoubles = ["MOV", "CMP"]
listaMov = ["(A),B", "A,(A)", "A,A", "B,B","(B),B"]
listaC = ["A,(B)", "B,(B)", "B,(A)"]
binario = {'MOV A,B' : '0000000','MOV B,A':'0000001','ADD A,B':'0000100','ADD B,A':'0000101','SUB A,B':'0001000','SUB B,A':'0001001','AND A,B':'0001100','AND B,A':'0001101','OR A,B':'0010000','OR B,A':'0010001','NOT A,A':'0010100','NOT A,B':'0010101','NOT B,A':'0010110','NOT B,B':'0010111','XOR A,A':'0011000','XOR B,A':'0011001',
                    'SHL A,A':'0011100','SHL A,B':'0011101','SHL B,A':'0011110','SHL B,B':'0011111','SHR A,A':'0100000','SHR A,B':'0100001','SHR B,A':'0100010','SHR B,B':'0100011','INC B':'0100100','CMP A,B':'1001101','MOV A,(B)':'0101001','MOV B,(B)':'0101010','MOV (B),A':'0101011','ADD A,(B)':'0101110','SUB A,(B)':'0110010',
                    'AND A,(B)':'0110110','OR A,(B)':'0111010','NOT (B)':'0111110','XOR A,(B)':'1000001','SHL (B)':'1000101','SHR (B)':'1001000','CMP A,(B)':'1010010','INC (B)':'1001010','RST (B)':'1001100'
                    }
binario_literal = {'MOV A':'0000010','MOV B':'0000011','ADD A':'0000110','ADD B':'0000111','SUB A':'0001010','SUB B':'0001011','AND A':'0001110','AND B':'0001111',
                    'OR A':'0010010','OR B':'0010011','XOR A':'0011010','XOR B':'0011011','CMP A':'1001110','CMP B':'1001111'
                    }

binario_direccionamiento = {'MOV A':'0100101','MOV B':'0100110','MOV (),A':'0100111','MOV (),B':'0101000','ADD A':'0101100','ADD B':'0101101','ADD':'0101111', 'SUB A':'0110000','SUB B':'0110001','SUB':'0110011','AND A':'0110100','AND B':'0110101','AND':'0110111','OR A':'0111000','OR B':'0111001',
                            'OR':'0111011','NOT (),A':'0111100','NOT (),B':'0111101','XOR A':'0111111','XOR B':'1000000','XOR ()':'1000010','SHL (),A':'1000011','SHL (),B':'1000100','SHR (),A':'1000110','SHR (),B':'1000111','INC ()':'1001001','RST':'1001011','CMP A':'1010000','CMP B':'1010001',
                            }
binario_jump = {'JMP':'1010011','JEQ':'1010100','JNE':'1010101','JGT':'1010110','JLT':'1010111','JGE':'1011000','JLE':'1011001','JCR':'1011010','JOV':'1011011'}
hexadecimal = {'0E':'00001110','0D':'00001101','0C':'00001100','F2':'11110010'}
filecheck = True
variables = []
direcciones = {}
memo = 0

for i in Data:
    if " " not in i:
        filecheck = False
        print("Error en la linea: " + i + "\n" + "Debe entregar un valor a la variable", i)
    else:
        i = i.split()
        variables.append(i[0])
        a = i[1]
        if a.count("#") > 1:
            print("Error en la linea: " + i[0]+ " " + i[1] + "\n" + i[1] + " No es una direccion valida")
            continue
        else:
            a = ToBinary(a)
            file2.write(a+"\n")
file2.close()
test_variables = []

for idx, linea in enumerate(Code):
    line = linea.split()
    linea = linea.strip()
    if " " not in linea:
        if linea[-1] != ":":
            print("Error en la linea {}: {} \tNo se recibe parametro".format(idx + 1, linea, line[0]))
            filecheck = False
            continue
        else:
            direcciones[linea.strip(":")] = memo
            continue
    memo += 1
    operation = line[0]
    firstoperand = line[1]
    secondoperand = ""

    try:
        if line[0][0] != "J":
            first = line[1].split(",")[0]
            type(int(first))
            print("Error en la linea {}: {} \tEl primer parametro no puede ser un literal".format(idx + 1, linea, line[0]))
            filecheck = False
            continue
    except:
        pass
    if "," in line[1]:
        firstoperand = (line[1].split(","))[0]
        secondoperand = (line[1].split(","))[1]
    if line[0] not in instructions:
        print("Error en la linea {}: {} \t{} no es una instruccion valida".format(idx + 1, linea, line[0]))
        filecheck = False
    elif (secondoperand == "" and firstoperand == "A"):
        print("Error en la linea {}: {} \tInstruccion invalida".format(idx + 1, linea, line[0]))
        filecheck = False
    elif "," in linea:
        if firstoperand[0] == "(" and secondoperand[0] == "(":
            print("Error en la linea {}: {} \tNo se pueden recibir 2 direcciones.".format(idx + 1, linea, line[0]))
            filecheck = False
    elif line[0] in instructions: #Antes era MOV pero segun yo ninguna intruccion puede empezar con (A)
        if (line[1].split(","))[0] == "(A)":
           print("Error en la linea {}: {} \tEl primer elemento no puede ser (A)".format(idx + 1, linea, line[0]))
           filecheck = False
    if line[0] == "INC" or line[0] == "RST":
        if firstoperand[0] != "(":
            if line[0] == "INC" and firstoperand[0] == "B":
                continue
            print("Error en la linea {}: {} \tInstruccion debe recibir una direccion".format(idx + 1, linea, line[0]))
            filecheck = False
        else:
            if firstoperand[1] != "B":
                a = firstoperand.strip("()")
                if a in variables:
                    continue
                try:
                   a = ToBinary(a)
                except:
                    print("Error en la linea {}: {} \tDebe recibir una direccion.".format(idx + 1, linea))
                    filecheck = False
    if operation == "NOT" or operation == "SHL" or operation == "SHR":
        if "(" in linea:
            a = linea.index("(") + 1
            b = linea.index(")")
            z = linea[:a] + linea[b:]
            if z not in binario_direccionamiento:
                print("Error en la linea {}: {} \tOperacion no soportada.".format(idx + 1, linea, line[0]))
                filecheck = False
        else:
            if linea not in binario:
                print("Error en la linea {}: {} \tOperacion no soportada.".format(idx + 1, linea, line[0]))
                filecheck = False
    if operation == "MOV" or operation == "ADD" or operation == "SUB" or operation == "OR" or operation == "XOR" or operation == "AND":
        if "(" not in linea:
            try:
                int(secondoperand)
                continue
            except:
                if linea not in binario and linea not in binario_direccionamiento:
                    print(
                        "Error en la linea {}: {} \t{} con parametros invalidos.".format(
                            idx + 1, linea,operation))
                    filecheck = False
        else:
            if line[1] in listaMov:
                print("Error en la linea {}: {} \tMov con parametros invalidos.".format(idx + 1, linea))
                filecheck = False
    if line[0] == "ADD" or line[0] == "SUB" or line[0] == "AND" or line[0] == "OR" or line[0] == "XOR":
        if line[1][0] == "(" :
            if secondoperand != "":
                print("Error en la linea {}: {} \tSi se entrega una direccion no se puede recibir un segundo parametro.".format(idx + 1, linea))
                filecheck = False
            elif line[1][1] != "A" or line[1][1] != "B":
                if "#" in line[1]:
                    num = int("0x" + firstoperand.strip("(#)"), 0)
                else:
                    num = int(firstoperand.strip("()"), 0)
                if num > 256:
                    print("Error en la linea {}: {} \tEl literal excede el valor aceptado.".format(idx + 1, linea))
                    filecheck = False
        else:
            if secondoperand == "":
                print("Error en la linea {}: {} \tInstruccion invalida.".format(idx + 1, linea))
            elif secondoperand[0] != "(" and secondoperand != "A" and secondoperand != "B":
                if secondoperand[0] == "#":
                    num = int("0x" + secondoperand.strip("#\n"), 0)
                else:
                    num = int(secondoperand, 0)
                if num > 256:
                    print("Error en la linea {}: {} \tEl literal excede el valor aceptado.".format(idx + 1, linea))
                    filecheck = False

    if line[0] == "MOV" and line[1][0] == "(":
        if line[1][1] != "A" or line[1][1] != "B":
            if "#" in line[1]:
                num = int("0x" + firstoperand.strip("(#)"), 0)
            else:
                try:
                    num = int(firstoperand.strip("()"), 0)
                except:
                    test()
                    continue            
            if num > 256:
                print("Error en la linea {}: {} \tEl literal excede el valor aceptado.".format(idx + 1, linea))
                filecheck = False
        if line[1].strip("(),") == "B" and line[2] != "A":
            print("Error en la linea {}: {} \tInstruccion invalida.".format(idx + 1, linea))
            filecheck = False

    if line[0] == "MOV":
        if "," not in linea:
            print("Error en la linea {}: {} \tMOV debe recibir 2 parametros.".format(idx + 1, linea))
            filecheck = False
            continue

        if secondoperand[0] != "(" and secondoperand != "A" and secondoperand != "B":
            if secondoperand[0] == "#":
                num = int("0x" + secondoperand.strip("#\n"), 0)
            else:
                try:
                    num = int(secondoperand, 0)
                except:
                    test()
                    continue
            if num > 256:
                print("Error en la linea {}: {} \tEl literal excede el valor aceptado.".format(idx + 1, linea))
                filecheck = False
        if secondoperand[0] == "(" and line[1] not in listaC:
            try:
                num = int(secondoperand.strip("()"), 0)
            except:
                test()
                continue
            
                
    if ((operation in notDoubles) and (secondoperand[0] == "")):
        print("Error en la linea {}: {} \t{} debe recibir 2 parametros.".format(idx + 1, linea, line[0]))
        filecheck = False

    if firstoperand[0] == "(" and secondoperand == "(":
        print("Error en la linea {}: {} \tError de sintaxis, {} no se acepta (Dir),(Dir).".format(idx + 1, linea,line[0]))
        filecheck = False

    if line[0][0] == "J":
        if firstoperand != "A" and firstoperand != "B" and firstoperand[0] != "(":
            if "#" in firstoperand:
                num = int("0x" + firstoperand.strip("(#\n)"), 0)
            else:
                try:
                    num = int(firstoperand, 0)
                except:
                    test_variables.append(line[1])
                    continue

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
        if firstoperand[0] == "(" or secondoperand == "A" or line[1] in listaMov :
            print("Error en la linea {}: {} \tOperacion no soportada.".format(idx + 1, linea, line[0]))
            filecheck = False
            
for i in test_variables:
    if i not in direcciones and i not in variables:
        print("Variable "+ i +" invalida")
        filecheck = False

if filecheck:
    print("\nCompilación realizada con exito.")
else:
    print("\n[!] Error: Uno o más errores encontrados a la hora de compilar")

if filecheck:
    for idx, linea in enumerate(Code):

        if " " not in linea and linea[-1] == ":":
            continue
        linea = linea.strip()
        line = linea.split(",")
        lineaa = linea.split()
        
        if linea in binario:
            file1.write(binario[linea] + "00000000" + "\n")

        if linea not in binario:
            if line[0] in binario_literal:
            
                if line[1][0] != "(":
                    file1.write(binario_literal[line[0]]+"{0:08b}".format(int(line[1]))+"\n")
                    
            if line[0] in binario_direccionamiento:
                if line[1][0] == "(":
                    a = test()
                    if a in variables:
                        a = variables.index(a)
                        a = "{0:08b}".format(int(a))
                        file1.write(binario_direccionamiento[line[0]]+str(a)+"\n")
                    else:
                        a = line[1].strip("()")
                        a = ToBinary(a)
                        file1.write(z + a + "\n")


            if line[0].split(" ")[1][0] == "(":
                a = linea.index("(") + 1
                b = linea.index(")")
                if linea[:a] + linea[b:] in binario_direccionamiento and "," in linea:
                    z = binario_direccionamiento[linea[:a] + linea[b:]]
                    a = linea[a:b]
                    try:
                        a = variables.index(a)
                        a = "{0:08b}".format(int(a))
                        file1.write(z + a + "\n")
                    except:
                        a = ToBinary(a)
                        file1.write(z+a+"\n")
                if line[0].split(" ")[0] == "INC" and line[0].split(" ")[1] != "B":
                    z = binario_direccionamiento[linea[:a] + linea[b:]]
                    a = linea[a:b]
                    a = variables.index(a)
                    a = "{0:08b}".format(int(a))
                    file1.write( z + a + "\n")

            if lineaa[0] in binario_jump:
                if lineaa[1] in direcciones:
                    a = direcciones[lineaa[1]]
                    a = "{0:08b}".format(int(a))
                    file1.write(binario_jump[lineaa[0]] + a + "\n")
                else:
                    a = lineaa[1]
                    a = ToBinary(a)
                    file1.write(binario_jump[lineaa[0]]+ a + "\n")
            if not "," in linea and lineaa[0] in binario_direccionamiento:
                a = lineaa[1].strip("()").strip("#")
                try:
                    file1.write(binario_direccionamiento[lineaa[0]] + "{0:08b}".format(
                        int(lineaa[1].strip("()").strip("#"))) + "\n")
                except:
                    file1.write(binario_direccionamiento[lineaa[0]] + str(((hexadecimal[a]))) + "\n")

if filecheck == True:
    print("Archivos escritos con exito.\n")

file.close()
file1.close()
