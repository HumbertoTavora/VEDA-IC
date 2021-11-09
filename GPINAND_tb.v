`timescale 1ns / 100ps 

module GPINAND_tb;

integer f;
reg I0_tb;
reg I1_tb;
reg I2_tb;
reg I3_tb;
wire paridade_par_tb; 

GPINAND uut (
.I0(I0_tb),
.I1(I1_tb),
.I2(I2_tb),
.I3(I3_tb),
.paridade_par(paridade_par_tb)
);



initial begin
f = $fopen("output_NetlistGPINAND.txt","w");

I0_tb = 0; I1_tb = 0; I2_tb = 0; I3_tb = 0; #20;
$fwrite(f,"%d\n", paridade_par_tb);

I0_tb = 0; I1_tb = 0; I2_tb = 0; I3_tb = 1; #20;
$fwrite(f,"%d\n", paridade_par_tb);

I0_tb = 0; I1_tb = 0; I2_tb = 1; I3_tb = 0; #20;
$fwrite(f,"%d\n", paridade_par_tb);

I0_tb = 0; I1_tb = 0; I2_tb = 1; I3_tb = 1; #20;
$fwrite(f,"%d\n", paridade_par_tb);

I0_tb = 0; I1_tb = 1; I2_tb = 0; I3_tb = 0; #20;
$fwrite(f,"%d\n", paridade_par_tb);

I0_tb = 0; I1_tb = 1; I2_tb = 0; I3_tb = 1; #20;
$fwrite(f,"%d\n", paridade_par_tb);

I0_tb = 0; I1_tb = 1; I2_tb = 1; I3_tb = 0; #20;
$fwrite(f,"%d\n", paridade_par_tb);

I0_tb = 0; I1_tb = 1; I2_tb = 1; I3_tb = 1; #20;
$fwrite(f,"%d\n", paridade_par_tb);

I0_tb = 1; I1_tb = 0; I2_tb = 0; I3_tb = 0; #20;
$fwrite(f,"%d\n", paridade_par_tb);

I0_tb = 1; I1_tb = 0; I2_tb = 0; I3_tb = 1; #20;
$fwrite(f,"%d\n", paridade_par_tb);

I0_tb = 1; I1_tb = 0; I2_tb = 1; I3_tb = 0; #20;
$fwrite(f,"%d\n", paridade_par_tb);

I0_tb = 1; I1_tb = 0; I2_tb = 1; I3_tb = 1; #20;
$fwrite(f,"%d\n", paridade_par_tb);

I0_tb = 1; I1_tb = 1; I2_tb = 0; I3_tb = 0; #20;
$fwrite(f,"%d\n", paridade_par_tb);

I0_tb = 1; I1_tb = 1; I2_tb = 0; I3_tb = 1; #20;
$fwrite(f,"%d\n", paridade_par_tb);

I0_tb = 1; I1_tb = 1; I2_tb = 1; I3_tb = 0; #20;
$fwrite(f,"%d\n", paridade_par_tb);

I0_tb = 1; I1_tb = 1; I2_tb = 1; I3_tb = 1; #20;
$fwrite(f,"%d\n", paridade_par_tb);

$fclose(f);
end


endmodule

