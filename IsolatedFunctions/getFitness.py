fnetlist = open("output_NetlistGPINAND.txt", 'r', encoding='utf-8')
ftrue = open("output_TrueGPINAND.txt", 'r', encoding='utf-8')

contador = 0

for i in range(0,16):
    out1 = ftrue.readline()
    out2 = fnetlist.readline()

    if out1 == out2:
        contador = contador + 1

fitness = float(contador/16)
fitness = "{:.2%}".format(fitness)

print("O Fitness é:", fitness )

fnetlist.close()
ftrue.close()

x = input()
