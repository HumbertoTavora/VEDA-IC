def modela_frase(a,b,c):

    frase ="assign	"+a+" = ~("+b+" & "+c+");\n\n"
    return frase

with open("test.v",'w',encoding = 'utf-8') as f:
    
    f.write("module GPINAND(I0,I1,I2,I3,paridade_par);\n\n")

    
    f.write("input wire	I0;\ninput wire  I1;\ninput wire	I2;\ninput wire  I3;\noutput wire    paridade_par;\n\n")

    f.write("wire	SYNTHESIZED_WIRE_18;\nwire	SYNTHESIZED_WIRE_19;\nwire	SYNTHESIZED_WIRE_5;\nwire	SYNTHESIZED_WIRE_6;\nwire	SYNTHESIZED_WIRE_8;\nwire	SYNTHESIZED_WIRE_9;\nwire	SYNTHESIZED_WIRE_10;\nwire	SYNTHESIZED_WIRE_11;\nwire	SYNTHESIZED_WIRE_12;\nwire	SYNTHESIZED_WIRE_13;\nwire	SYNTHESIZED_WIRE_14;\nwire	SYNTHESIZED_WIRE_15;\nwire	SYNTHESIZED_WIRE_16;\nwire	SYNTHESIZED_WIRE_17;\n\n")
   

    frase = modela_frase("SYNTHESIZED_WIRE_6","SYNTHESIZED_WIRE_18","SYNTHESIZED_WIRE_18")
    f.write(frase)
    frase = modela_frase("SYNTHESIZED_WIRE_5","SYNTHESIZED_WIRE_19","SYNTHESIZED_WIRE_19")
    f.write(frase)
    frase = modela_frase("SYNTHESIZED_WIRE_9","SYNTHESIZED_WIRE_18","SYNTHESIZED_WIRE_5")
    f.write(frase)
    frase = modela_frase("SYNTHESIZED_WIRE_8","SYNTHESIZED_WIRE_6","SYNTHESIZED_WIRE_19")
    f.write(frase)
    frase = modela_frase("paridade_par","SYNTHESIZED_WIRE_8","SYNTHESIZED_WIRE_9")
    f.write(frase)
    frase = modela_frase("SYNTHESIZED_WIRE_13","I1","SYNTHESIZED_WIRE_10")
    f.write(frase)
    frase = modela_frase("SYNTHESIZED_WIRE_15","I3","I3")
    f.write(frase)
    frase = modela_frase("SYNTHESIZED_WIRE_14","I2","I2")
    f.write(frase)
    frase = modela_frase("SYNTHESIZED_WIRE_12","SYNTHESIZED_WIRE_11","I0")
    f.write(frase)
    frase = modela_frase("SYNTHESIZED_WIRE_19","SYNTHESIZED_WIRE_12","SYNTHESIZED_WIRE_13")
    f.write(frase)
    frase = modela_frase("SYNTHESIZED_WIRE_11","I1","I1")
    f.write(frase)
    frase = modela_frase("SYNTHESIZED_WIRE_10","I0","I0")
    f.write(frase)
    frase = modela_frase("SYNTHESIZED_WIRE_17","I3","SYNTHESIZED_WIRE_14")
    f.write(frase)
    frase = modela_frase("SYNTHESIZED_WIRE_16","SYNTHESIZED_WIRE_15","I2")
    f.write(frase)
    frase = modela_frase("SYNTHESIZED_WIRE_18","SYNTHESIZED_WIRE_16","SYNTHESIZED_WIRE_17")
    f.write(frase)
    

    
    f.write("\n\nendmodule")