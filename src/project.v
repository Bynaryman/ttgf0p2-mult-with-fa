`default_nettype none
// Streaming 24-bit by 24-bit multiplier built from 8-bit UI samples.
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
    reg [23:0] operand_a;
    reg [23:0] operand_b;
    reg [47:0] product;
    reg [2:0]  stream_pos;

    wire [23:0] next_operand_a = {operand_a[15:0], ui_in};
    wire [23:0] next_operand_b = {operand_b[15:0], ui_in};

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            operand_a  <= 24'd0;
            operand_b  <= 24'd0;
            product    <= 48'd0;
            stream_pos <= 3'd0;
        end else if (ena) begin
            if (stream_pos < 3'd3) begin
                operand_a <= next_operand_a;
            end else begin
                operand_b <= next_operand_b;
            end

            product <= (stream_pos < 3'd3 ? next_operand_a : operand_a) *
                       (stream_pos >= 3'd3 ? next_operand_b : operand_b);

            if (stream_pos == 3'd5) begin
                stream_pos <= 3'd0;
            end else begin
                stream_pos <= stream_pos + 3'd1;
            end
        end
    end

    wire product_nonzero = |product;
    assign uo_out = {8{product_nonzero}};
    assign uio_out = 8'h00;
    assign uio_oe  = 8'h00;
endmodule
