@echo off
iverilog -o prog GPINAND_tb.v GPINAND.v
vvp prog
.\getFitness.py
pause
