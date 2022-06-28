`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2021/12/28 15:47:10
// Design Name: 
// Module Name: select_5_bit
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


module select_5_bit(
    input [4:0] select_one,//rd
    input [4:0] select_two,//rt
    input control,//1ÊÇrt£¬0ÊÇrd
    output [4:0] result
    );
    
    assign result = (control == 1'b0 ? select_one : select_two);
endmodule
