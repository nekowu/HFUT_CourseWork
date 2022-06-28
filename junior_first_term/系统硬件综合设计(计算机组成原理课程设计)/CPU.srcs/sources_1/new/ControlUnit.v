`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2021/12/29 11:01:16
// Design Name: 
// Module Name: ControlUnit
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


module ControlUnit(
    input [5:0] op,
    input zero,
    output reg Reset,
    output reg PCWre,
    output reg ALUSrcA,
    output reg ALUSrcB,
    output reg DBDataSrc,
    output reg RegWre,
    output reg InsMemRW,
    output reg mRD,
    output reg mWR,
    output reg RegDst,
    output reg ExtSel,
    output reg [1:0] PCSrc,
    output reg [2:0] ALUOp
    );
    
    initial
        begin
            //Reset = 1;
            PCWre = 1;
            ALUSrcA = 0;
            ALUSrcB = 0;
            DBDataSrc = 0;
            RegWre = 0;
            InsMemRW = 1;
            mRD = 0;
            mWR = 0;
            RegDst = 0;
            ExtSel = 0;
            PCSrc = 0;
            ALUOp = 0;
        end
    
    always@(op or zero)
    begin
        case(op)
            //add
            6'b000000:
                begin
                    Reset = 1; //重置信号
                    PCWre = 1;//PC改变（next+4）
                    ALUSrcA = 0;//选择寄存和sa
                    ALUSrcB = 0;//寄存、扩展立即数
                    DBDataSrc = 0;//选择输出数据还是地址（0是数据，1地址）
                    RegWre = 1;//寄存器可写
                    mWR = 0;//只与写数据寄存器（sw）有关（1）
                    RegDst = 1;//存rt\rd
                    ALUOp = 000;//选择功能
                    PCSrc = 00;//决定下一个地址是否跳转
                end
            
            //addi
            6'b000001:
                begin
                    Reset = 1;
                    PCWre = 1;
                    ALUSrcA = 0;
                    ALUSrcB = 1;
                    DBDataSrc = 0;
                    RegWre = 1;
                    mWR = 0;
                    RegDst = 0;
                    ExtSel = 1;
                    ALUOp = 000;
                    PCSrc = 00;
                end
            
            //sub
            6'b000010:
                begin
                    Reset = 1;
                    PCWre = 1;
                    ALUSrcA = 0;
                    ALUSrcB = 0;
                    DBDataSrc = 0;
                    RegWre = 1;
                    mWR = 0;
                    RegDst = 1;
                    ALUOp = 001;
                    PCSrc = 00;
                end
            
            //ori
            6'b010000:
                begin
                    Reset = 1;
                    PCWre = 1;
                    ALUSrcA = 0;
                    ALUSrcB = 1;
                    DBDataSrc = 0;
                    RegWre = 1;
                    mWR = 0;
                    RegDst = 0;
                    ExtSel = 0;
                    ALUOp = 011;
                    PCSrc = 00;
                end
            
            //and
            6'b010001:
                begin
                    Reset = 1;
                    PCWre = 1;
                    ALUSrcA = 0;
                    ALUSrcB = 0;
                    DBDataSrc = 0;
                    RegWre = 1;
                    mWR = 0;
                    RegDst = 1;
                    ALUOp = 100;
                    PCSrc = 00;
                end
            
            //or
            6'b010010:
                begin
                    Reset = 1;
                    PCWre = 1;
                    ALUSrcA = 0;
                    ALUSrcB = 0;
                    DBDataSrc = 0;
                    RegWre = 1;
                    mWR = 0;
                    RegDst = 1;
                    ALUOp = 011;
                    PCSrc = 00;
                end
            
            //sll
            6'b011000:
                begin
                    Reset = 1;
                    PCWre = 1;
                    ALUSrcA = 1;
                    ALUSrcB = 0;
                    DBDataSrc = 0;
                    RegWre = 1;
                    mWR = 0;
                    RegDst = 1;
                    ALUOp = 010;
                    PCSrc = 00;
                end
            
            //slti
            6'b011011:
                begin
                    Reset = 1;
                    PCWre = 1;
                    ALUSrcA = 0;
                    ALUSrcB = 1;
                    DBDataSrc = 0;
                    RegWre = 1;
                    mWR = 0;
                    RegDst = 0;
                    ExtSel = 1;
                    ALUOp = 101;
                    PCSrc = 00;
                end
            
            //sw
            6'b100110:
                begin
                    Reset = 1;
                    PCWre = 1;
                    ALUSrcA = 0;
                    ALUSrcB = 1;
                    RegWre = 0;
                    mWR = 1;
                    ExtSel = 1;
                    PCSrc = 00;
                    ALUOp = 000;
                end
            
            //lw
            6'b100111:
                begin
                    Reset = 1;
                    PCWre = 1;
                    ALUSrcA = 0;
                    ALUSrcB = 1;
                    DBDataSrc = 1;
                    RegWre = 0;
                    mRD = 1;
                    mWR = 0;
                    RegDst = 0;
                    ExtSel = 1;
                    PCSrc = 00;
                    ALUOp = 000;
                end
            
            //beg
            6'b110000:
                begin
                    Reset = 1;
                    PCWre = 1;
                    ALUSrcA = 0;
                    ALUSrcB = 0;
                    DBDataSrc = 0;
                    RegWre = 0;
                    mWR = 0;
                    ExtSel = 1;
                    ALUOp = 001;
                    if(zero == 1) begin 
                            PCSrc = 1'b01;
                        end
                    else begin
                            PCSrc = 1'b00;
                        end
                end
            
            
            //bne
            6'b110001:
                begin
                    if(zero == 1) begin 
                        PCSrc = 1'b00;
                    end
                else begin
                        PCSrc = 1'b01;
                    end
                    Reset = 1;
                    PCWre = 1;
                    ALUSrcA = 0;
                    ALUSrcB = 0;
                    DBDataSrc = 0;
                    RegWre = 0;
                    mWR = 0;
                    ExtSel = 1;
                    ALUOp = 001;

                end
            
            
            //j
            6'b111000:
                begin
                    Reset = 1;
                    PCWre = 1; 
                    RegWre = 0;
                    PCSrc = 10;
                end
                
                
            //halt
            6'b111111:
                begin
                    Reset = 0;
                    PCWre = 0;
                    ALUSrcB = 0;  
                    RegWre = 0;                                                                                                                                                       
                end
        endcase
    end
endmodule


    
 
