`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2021/12/27 17:03:21
// Design Name: 
// Module Name: select_32or5_bit
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

//选择从寄存器取值还是从指令里的sa取值，作为alu里的a
module select_32or5_bit(
    input [31:0] select_one,
    input [4:0] select_two,
    input control,
    output [31:0] result
    );
    
    wire[31:0] select_three;
    assign select_three[4:0] = select_two;
    assign select_three[31:5] = 1'b000000000000000000000000000;
    assign result = (control == 1'b0 ? select_one : select_three);
endmodule
