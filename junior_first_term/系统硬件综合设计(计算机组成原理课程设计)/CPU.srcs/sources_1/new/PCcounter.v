`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2021/12/27 19:12:42
// Design Name: 
// Module Name: PCcounter
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
//决定你是顺序执行还是跳转

module PCcounter(
    input [1:0] PCSrc,
    input [31:0] currentAddress,
    output reg [31:0] newAddress,
    input [31:0] outData,
    input [25:0] jAddress
    );
    
    wire [31:0] temp_one, temp_two, temp_three;
    assign temp_one = currentAddress + 4;
    assign temp_two[25:0] = jAddress[25:0];
    assign temp_three = temp_two << 2;
    always@(PCSrc or currentAddress or outData or jAddress or temp_one or temp_three )
        begin
            case(PCSrc)
                2'b00:  newAddress = currentAddress+4;
                2'b01:  
                    begin
                        newAddress = (currentAddress+4)+ (outData << 2);
                        newAddress[1:0] = 1'b00;
                    end
                
                2'b10: 
                begin
                     newAddress[31:28] = temp_one[31:28];
                     newAddress[27:0] = temp_three[27:0];
                end
             endcase
        end
endmodule
