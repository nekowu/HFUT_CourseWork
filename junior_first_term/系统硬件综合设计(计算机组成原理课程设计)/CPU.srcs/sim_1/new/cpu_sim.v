`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2021/12/30 20:11:16
// Design Name: 
// Module Name: cpu_sim
// Project Name: 
// Target Devices: 
// Tool Versions: 
// Description: 
// 
// Dependencies: 
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
//////////////////////////////////////////////////////////////////////////////////


module cpu_sim();

    reg CLK;
    reg Reset;
    wire zero;
    wire pcWre;
    wire[1:0] pcSrc;
    wire[2:0] aluop;
    wire[5:0] op;
    wire[31:0] readData1;
    wire[31:0] readData2;
    wire[31:0] Result;
    wire[31:0] extendData;
    wire[31:0] writeData;
    wire[31:0] currentAdd;
    wire[31:0] o_p;
    
    
    Main one(
        
        .CLK(CLK),
        .Reset(Reset),
        .zero(zero),
        .pcWre(pcWre),
        .pcSrc(pcSrc),
        .aluop(aluop),
        .op(op),
        .readData1(readData1),
        .readData2(readData2),
        .extendData(extendData),
        .writeData(writeData),
        .o_p(o_p),
        .currentAdd(currentAdd),
        .Result(Result)
        );
       
    initial
        begin
            CLK = 0;
            Reset = 0;
            #5;
                CLK = ~CLK;
            #5;
            Reset = 1;
        end
        
    always #5 CLK = ~CLK;
endmodule
