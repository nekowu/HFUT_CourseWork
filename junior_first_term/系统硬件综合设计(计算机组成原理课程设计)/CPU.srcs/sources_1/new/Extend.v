`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2021/12/27 18:44:32
// Design Name: 
// Module Name: Extend
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


module Extend(
    input [15:0] immediate,
    input ExtSel,
    output reg[31:0] outData
    );
    
    always@(immediate or ExtSel)
    begin
        case(ExtSel)
            1'b0:
                begin
                    outData[15:0] = immediate;
                    outData[31:16] = 16'h0000;
                end
            1'b1:
                begin
                    outData[15:0] = immediate;
                    outData[31:16] = (immediate[15])? 16'hffff : 16'h0000;
                end 
        endcase
    end
endmodule
