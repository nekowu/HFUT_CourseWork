`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2021/12/29 15:59:18
// Design Name: 
// Module Name: Main
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

module Main(
    input CLK,  //时钟
    input Reset,    //重置信号
    output zero,pcWre,  //ALU结果是否为0， PC更改信号
    output[1:0] pcSrc,  //PC四选一选择器的控制信号
    output[2:0] aluop,  //ALU的执行信号
    output[5:0] op, //指令操作的代码
    output[31:0] readData1, readData2, extendData, writeData, o_p, currentAdd, Result   //寄存器1读取的值，寄存器2读取的值，拓展符号信号，写入寄存器的数据， 32位的整条指令， 当前指令的地址， ALU输出的结果
    );
    wire Zero, PCWre, ALUSrcA, ALUSrcB, DBDataSrc, RegWre, InsMemRW, mRD, mWR, RegDst, ExtSel;
    wire[1:0] PCSrc;
    wire[2:0] ALUOp;
    wire[4:0] fiveout;
    wire[31:0] NewAdd, CurrentAdd, o_pc, WriteData, ReadData1, ReadData2, ExtendData, rega, regb, result, RAMData;
    
    assign o_p = o_pc;
    assign op = o_pc[31:26];
    assign readData1 = ReadData1;
    assign readData2 = ReadData2;
    assign aluop = ALUOp;
    assign zero = Zero;
    assign writeData = WriteData;
    assign currentAdd = CurrentAdd;
    assign pcWre = PCWre;
    assign Result = result;
    assign pcSrc = PCSrc;
    assign extendData = ExtendData;
    ControlUnit cu(
        o_pc[31:26],
        Zero,
        Reset,
        PCWre,
        ALUSrcA,
        ALUSrcB,
        DBDataSrc,
        RegWre,
        InsMemRW,
        mRD,
        mWR,
        RegDst,
        ExtSel,
        PCSrc,
        ALUOp
        );
        
    PC pc(
        CLK,
        Reset,
        PCWre,//值为0时不更改，代表停机指令；值为1的时候进行更改
        NewAdd,
        CurrentAdd
        );
       
    ROM rom( 
        InsMemRW, 
        CurrentAdd, 
        o_pc
        );
        
    select_5_bit U5_1(
        o_pc[20:16],
        o_pc[15:11],
        RegDst,
        fiveout
        );
        
    RegFile rf(
        CLK,
        Reset,
        RegWre,
        o_pc[25:21],
        o_pc[20:16],
        fiveout,
        WriteData,
        ReadData1,
        ReadData2
        );
        
    Extend ex(
        o_pc[15:0],
        ExtSel,
        ExtendData
        );
        
    select_32or5_bit U32_1(
        ReadData1,
        o_pc[10:6],
        ALUSrcA,
        rega
        );
        
    select_32_bit U32_2(
        ReadData2,
        ExtendData,
        ALUSrcB,
        regb
        );
 
    ALU alu(
        ALUOp,
        rega,
        regb,
        result,
        Zero
        );  
        
    RAM ram(
        CLK,
        result,
        ReadData2, // [31:24], [23:16], [15:8], [7:0]
        mRD, // 为0， 正常读； 为1,输出高组态
        mWR, // 为1， 写； 为0， 无操作
        RAMData
        );
        
    select_32_bit U32_3(
        result,
        RAMData,
        DBDataSrc,
        WriteData
        );
        
    PCcounter pccounter(
        PCSrc,
        CurrentAdd,
        NewAdd,
        ExtendData,
        o_pc[25:0]
        );
endmodule
