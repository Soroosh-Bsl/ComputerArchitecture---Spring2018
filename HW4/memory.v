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
			array[0] = 8'h10;//BIPUSH 9
			array[1] = 8'h09;
			array[2] = 8'h10;//BIPUSH 13
			array[3] = 8'h0c;
		
			array[4] = 8'hB6;//INVOKE
			array[5] = 8'h01;
			array[6] = 8'h00;
		
			array[61] = 8'h02;//NUM OF ARGUMENTS
			array[62] = 8'h00;
			array[63] = 8'h00;//NUM OF LOCAL PARAMS
			array[64] = 8'h00;
			array[65] = 8'h15;//ILOAD
			array[66] = 8'h00;
			array[67] = 8'h15;//ILOAD
			array[68] = 8'h01;
			array[69] = 8'h60;//IADD
			array[70] = 8'hAC;//IRETURN
		
			array[168] <= 8'b00111101;
			
			
			
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
