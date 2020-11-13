module memory(RES, clk,reset,address,data_in,data_out,rwn,start,ready,address_test1,address_test2,address_test3,data_test1,data_test2,data_test3);
	input clk,reset,start,rwn;
	input [31:0] address,address_test1,address_test2,address_test3;
	input [31:0] data_in;
	output [31:0] data_test1,data_test2,data_test3;
	output reg [31:0] data_out;
	output ready;
	output RES;
	reg [7:0] array[179:0];
	reg state = 0;
	reg [15:0] ad_t;
	reg [31:0] data_t;
	reg [1:0] counter;
	reg rwn_t;
	integer i;
	assign RES = reset;
	assign ready=~state;
	assign data_test1={array[address_test1[15:0]+3][7:0], array[address_test1[15:0]+2][7:0], array[address_test1[15:0]+1][7:0], array[address_test1[15:0]][7:0]};
	assign data_test2={array[address_test2[15:0]+3][7:0], array[address_test2[15:0]+2][7:0], array[address_test2[15:0]+1][7:0], array[address_test2[15:0]][7:0]};
	assign data_test3={array[address_test3[15:0]+3][7:0], array[address_test3[15:0]+2][7:0], array[address_test3[15:0]+1][7:0], array[address_test3[15:0]][7:0]};
	always @(posedge clk or posedge reset)
	begin
//		data_out = 8'b1111_1111;
		i = 0;
		if(reset) begin
		array[0] = 8'h10;
      array[1] = 8'h03;
      array[2] = 8'h36;
      array[3] = 8'h01;
      array[4] = 8'h15; 
      array[5] = 8'h01;
      array[6] = 8'h99;
      array[7] = 8'h09;
      array[8]=  8'h00;
      array[9]=  8'h84;
      array[10]= 8'h01;        
      array[11]= 8'hFF;
      array[12]= 8'hA7;        
      array[13]= 8'hF8;
      array[14]= 8'hFF;
      array[15]= 8'h00;		
//
//			array[136] <= 8'b00001111;
//			array[172] <= 8'b00000011;
//
//			array[0] <= 8'b00010000;
//			array[1] <= 8'b11001100;
//			
//			array[2] <= 8'b00010000;
//			array[3] <= 8'b00000111;
//			
//			array[4] <= 8'b01100000;
//			
//			array[5] <= 8'b00110110;
//			array[6] <= 8'b00000000;
//			
//			array[7] <= 8'b00010000;
//			array[8] <= 8'b11000000;
//			
//			array[9] <= 8'b00010000;
//			array[10] <= 8'b00000100;
//			
//			array[11] <= 8'b10000100;
//			array[12] <= 8'b00000001;
//			array[13] <= 8'b00000010;
//			
//			array[14] <= 8'b01100000;
//			
//			array[15] <= 8'b00010000;
//			array[16] <= 8'b11000100;
//			
//			array[17] <= 8'b10011111;
//			array[18] <= 8'b00001101;
//			array[19] <= 8'b00000000;
//			
//			array[33] <= 8'b00010000;
//			array[34] <= 8'b00000000;
//			
//			array[35] <= 8'b10011001;
//			array[36] <= 8'b00000010;
//			array[37] <= 8'b00000000;
//			
//			array[40] <= 8'b00010000;
//			array[41] <= 8'b10000001;
//			
//			array[42] <= 8'b10011011;
//			array[43] <= 8'b00000111;
//			array[44] <= 8'b00000000;
//			
//			array[52] <= 8'b00010000;
//			array[53] <= 8'b10101010;
//			
//			array[54] <= 8'b00110110;
//			array[55] <= 8'b00000001;
//			
//			array[56] <= 8'b10100111;
//			array[57] <= 8'b00001111;
//			array[58] <= 8'b00000000;
//			
//			array[74] <= 8'b00010000;
//			array[75] <= 8'b00000000;
//			
//			array[76] <= 8'b10011011;
//			array[77] <= 8'b00001000;
//			array[78] <= 8'b00000000;
//			
//			array[87] <= 8'b10100111;
//			array[88] <= 8'b10100110;
//			array[89] <= 8'b11111111;
//			
//			for (i = 100; i <121; i = i +1) begin
//				array[i] <= 8'd0;
//			end
			data_out = 8'b0000_0001;
			state=0;
		end
		else if(start & ~state) begin
			ad_t=address[15:0];
			rwn_t=rwn;
			data_t=data_in;
			counter=address[1:0];
			state=1;
			data_out = 8'b0000_0010;
		end
		else if(|counter && state) begin
			counter=counter-1;
			data_out = 8'b0000_0100;
		end
		else if(state) begin
			if(rwn_t)
				data_out = {array[ad_t+3], array[ad_t+2], array[ad_t+1], array[ad_t]};
			else begin
				array[ad_t]   <= data_t[7:0];
				array[ad_t+1] <= data_t[15:8];
				array[ad_t+2] <= data_t[23:16];
				array[ad_t+3] <= data_t[31:24];
				data_out = 8'b0000_1000;
			end
			state=0;
		end
	end
endmodule
