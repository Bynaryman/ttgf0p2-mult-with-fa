`default_nettype none
// Simple 4-bit by 4-bit multiplier design.
module tt_um_binaryman_multfa (
    input  wire [7:0] ui_in,
    output wire [7:0] uo_out,
    input  wire [7:0] uio_in,
    output wire [7:0] uio_out,
    output wire [7:0] uio_oe,
    input  wire       ena,
    input  wire       clk,
    input  wire       rst_n
);
    wire [3:0] operand_a = ui_in[3:0];
    wire [3:0] operand_b = ui_in[7:4];

    reg [7:0] product;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            product <= 8'd0;
        end else if (ena) begin
            product <= operand_a * operand_b;
        end
    end

    assign uo_out = product;

    assign uio_out = 8'h00;
    assign uio_oe  = 8'h00;
endmodule
