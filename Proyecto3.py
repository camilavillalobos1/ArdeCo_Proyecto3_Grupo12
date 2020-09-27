try:
    file = open("Incorrecto.txt", 'r')
except IOError:
    print("No se encontro el archivo")
    exit()

Lineas = file.readlines()
instructions = ["CMP", "JEQ", "MOV", "SUB", "ADD", "JMP"]
numeros = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
listaMov = ["(A),B", "A,(A)", "A,A", "B,B"]
for idx, linea in enumerate(Lineas):
    line = linea.split()

    for a in numeros:  # Revisar esto, segun yo ninguna instruccion puede empezar con un literal
        if line[1][0] == a and line[0][0] != "J" and line[0] != "CMP":
            print("Error en la linea {}: {} \tEl primer elemento no puede ser un literal".format(idx + 1, linea, line[0]))
            break

    if line[0] not in instructions:
        print("Error en la linea {}: {} \t{} no es una instruccion valida".format(idx + 1, linea, line[0]))

    elif line[0][0] == "J":
        if "," in line[1]:
            print("Error en la linea {}: {} \tError de sintaxis, {} solo recibe un parametro.".format(idx + 1, linea,
                                                                                                      line[0]))
    elif line[0] == "CMP" or line[0] == "MOV":  # MOV tampoco puede tener un numero al principio
        if line[1][0] != "#":
            try:
                float(line[1])
            except ValueError:
                print("Error en la linea {}: {} \tEl primer elemento no puede ser un literal".format(idx + 1, linea,
                                                                                                     line[0]))
        else:
            print(
                "Error en la linea {}: {} \tEl primer elemento no puede ser un literal".format(idx + 1, linea, line[0]))

    elif line[0] == "ADD":
        if line[1][0] == "(":
            print(
                "Error en la linea {}: {} \tPara la instrucción ADD no existe el uso con (Dir), 'algo'".format(idx + 1,
                                                                                                               linea,
                                                                                                               line[0]))

    elif line[0] == "MOV":
        i = 0
        if (line[1].split(","))[0] == "(A)":
            print("Error en la linea {}: {} \tEl primer elemento no puede ser (A)".format(idx + 1, linea, line[0]))
            
        for i in listaMov:
            if line[1] == listaMov[i]:
                print("Error en la linea {}: {} \tEl primer elemento no puede ser una direccion".format(idx + 1, linea,
                                                                                                        line[0]))
                i += 1
    elif line[0] == "":
        if "," in line[1]:
            print("Error en la linea {}: {} \tError de sintaxis, {} solo recibe un parametro.".format(idx + 1, linea,
                                                                                                      line[0]))


file.close()
