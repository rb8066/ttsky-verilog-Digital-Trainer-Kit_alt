`default_nettype none
`timescale 1ns / 1ps

module tb ();

    // Testbench signals
    reg  [7:0] ui_in;
    wire [7:0] uo_out;
    reg  [7:0] uio_in;
    wire [7:0] uio_out;
    wire [7:0] uio_oe;
    reg        clk;
    reg        rst_n;
    reg        ena;

    // DUT instance
    tt_um_remya_digital_trainer dut (
        .ui_in(ui_in),
        .uo_out(uo_out),
        .uio_in(uio_in),
        .uio_out(uio_out),
        .uio_oe(uio_oe),
        .ena(ena),
        .clk(clk),
        .rst_n(rst_n)
    );

    // Clock generator
    initial clk = 0;
    always #5 clk = ~clk;

    // Reset
    initial rst_n = 1;

    // Test procedure
    initial begin
        $display("Starting testbench...");
        uio_in = 8'b0;
        ui_in  = 8'b0;
        ena    = 1;

        for (integer s = 0; s < 7; s = s + 1) begin
            for (integer aa = 0; aa < 2; aa = aa + 1) begin
                for (integer bb = 0; bb < 2; bb = bb + 1) begin
                    ui_in[0] = aa;        // a
                    ui_in[1] = bb;        // b
                    ui_in[4:2] = s[2:0];  // sel
                    #10;
                    $display("ena=%b sel=%03b a=%b b=%b => y=%b",
                              ena, ui_in[4:2], ui_in[0], ui_in[1], uo_out[0]);
                end
            end
        end

        // Test disable
        ena = 0;
        ui_in[0] = 1; ui_in[1] = 1; ui_in[4:2] = 3'b000; // AND
        #10;
        $display("ena=%b sel=%03b a=%b b=%b => y=%b (should be 0)",
                  ena, ui_in[4:2], ui_in[0], ui_in[1], uo_out[0]);

        $display("Testbench finished.");
        $finish;
    end

endmodule
