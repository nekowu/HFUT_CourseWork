`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2021/12/28 18:25:54
// Design Name: 
// Module Name: ROM
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


module ROM ( rd, addr, dataOut); // 存储器模块
    input rd; // 读使能信号
    input [ 31:0] addr; // 存储器地址
    output reg [31:0] dataOut; // 输出的数据

    reg [7:0] rom [99:0]; // 存储器定义必须用reg类型， 存储器存储单元8位长度， 共100个存储单元
    
    initial // 加载数据到存储器rom。 注意： 必须使用绝对路径， 如： E:/Xlinx/VivadoProject/ROM/（自己定）
    begin     
        $readmemb ("D:\\vivadoproject\\singleCPUhlz\\rom_data.txt", rom); // 数据文件rom_data（.coe或.txt） 。 未指定， 就从0地址开始存放。
        //rom[addr][7:0] = 1'b00000100;
        dataOut = 0;
    end
    
    always @( rd or addr ) begin
        if (rd==1) begin // 为0， 读存储器。 大端数据存储模式
            dataOut[31:24] = rom[addr];
            dataOut[23:16] = rom[addr+1];
            dataOut[15:8] = rom[addr+2];
            dataOut[7:0] = rom[addr+3];
        end
    end
endmodule
