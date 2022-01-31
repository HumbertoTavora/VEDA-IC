def modela_frase(a,b,c):

    frase ="assign	"+a+" = ~("+b+" & "+c+");\n\n"
    return frase

n = 24
 
netlist = list(map(str,input("\nEnter the numbers : ").strip().split()))[:n]

print(netlist)

with open("test2.v",'w',encoding = 'utf-8') as f:
    
    f.write("module GPINAND(I0,I1,I2,I3,paridade_par);\n\n")

    
    f.write("input wire	I0;\ninput wire  I1;\ninput wire	I2;\ninput wire  I3;\noutput wire    paridade_par;\n\n")

    f.write("wire	SYNTHESIZED_WIRE_9;\nwire	SYNTHESIZED_WIRE_10;\nwire	SYNTHESIZED_WIRE_11;\nwire	SYNTHESIZED_WIRE_12;\nwire	SYNTHESIZED_WIRE_13;\nwire	SYNTHESIZED_WIRE_14;\nwire	SYNTHESIZED_WIRE_15;\nwire	SYNTHESIZED_WIRE_16;\nwire	SYNTHESIZED_WIRE_17;\nwire	SYNTHESIZED_WIRE_18;\nwire	SYNTHESIZED_WIRE_19;\nwire	SYNTHESIZED_WIRE_20;\nwire	SYNTHESIZED_WIRE_21;\nwire	SYNTHESIZED_WIRE_22;\nwire	SYNTHESIZED_WIRE_23;\nwire	SYNTHESIZED_WIRE_24;\nwire	SYNTHESIZED_WIRE_25;\nwire	SYNTHESIZED_WIRE_26;\nwire	SYNTHESIZED_WIRE_27;\nwire	SYNTHESIZED_WIRE_28;\n\n")
   

    count = 9
    for i in range(0,n):
        
        nout = str(count)
        count = count + 1
        nin1 = netlist[i][0:2]
        nin2 = netlist[i][2:4]
        

        if nin1 != "00" and nin2 != "00":

            if i==20:
                out = "paridade_par"
            else:
                out = "SYNTHESIZED_WIRE_"+nout
           
            if nin1 == "01":
                in1 = "I0" 
            elif nin1 == "02":
                in1 = "I1" 
            elif nin1 == "03":
                in1 = "I2" 
            elif nin1 == "04":
                in1 = "I3" 
            else:
                in1 = "SYNTHESIZED_WIRE_"+nin1
            
            if nin2 == "01":
                in2 = "I0" 
            elif nin2 == "02":
                in2 = "I1" 
            elif nin2 == "03":
                in2 = "I2" 
            elif nin2 == "04":
                in2 = "I3" 
            else:
                in2 = "SYNTHESIZED_WIRE_"+nin2

            frase = modela_frase(out,in1,in2)
            f.write(frase)

    f.write("\n\nendmodule")
