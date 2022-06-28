`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2021/12/27 15:50:08
// Design Name: 
// Module Name: select_32_bit
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

//从寄存器里取值还是从从扩展后的立即数取值，作为ALU里的B
module select_32_bit(
    input [31:0] select_one,
    input [31:0] select_two,
    input control,
    output [31:0] result
    );
    
    assign result = (control == 1'b0 ? select_one : select_two);
endmodule
