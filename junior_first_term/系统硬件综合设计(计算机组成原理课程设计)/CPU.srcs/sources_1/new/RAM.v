`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2021/12/27 18:30:57
// Design Name: 
// Module Name: RAM
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


module RAM(
    input clk,
    input [31:0] address,
    input [31:0] writeData, // [31:24], [23:16], [15:8], [7:0]
    input nRD, // 为0， 正常读； 为1,输出高组态
    input nWR, // 为1， 写； 为0， 无操作
    output [31:0] Dataout
    );
    
    reg [7:0] ram [0:60]; // 存储器定义必须用reg类型
    
    // 读
    //assign是随时赋值语句，Data有变化，随时写进到ram中去
    assign Dataout[7:0] = (nRD==1)?ram[address + 3]:8'bz; // z 为高阻态
    assign Dataout[15:8] = (nRD==1)?ram[address + 2]:8'bz;
    assign Dataout[23:16] = (nRD==1)?ram[address + 1]:8'bz;
    assign Dataout[31:24] = (nRD==1)?ram[address ]:8'bz;
    // 写
    always@( negedge clk ) begin // 用时钟下降沿触发写存储器， 个例
        if( nWR==0 ) begin
            ram[address] <= writeData[31:24];
            ram[address+1] <= writeData[23:16];
            ram[address+2] <= writeData[15:8];
            ram[address+3] <= writeData[7:0];
        end
    end
endmodule
