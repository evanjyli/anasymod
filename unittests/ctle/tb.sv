`timescale 1ns/1ps

`include "svreal.sv"
`include "msdsl.sv"

`default_nettype none

module tb;
    // input is voltage square wave
    `PWM(0.50, 1e9, in_dig);  // 50% duty, 1 GHz frequency
    `MAKE_CONST_REAL(+1.0, in_hi);
    `MAKE_CONST_REAL(-1.0, in_lo);
    `ITE_REAL(in_dig, in_hi, in_lo, v_in);

    `MAKE_REAL(v_out, 15.0);

    initial begin
        $display(`DT_MSDSL);
    end

    // filter instantiation
    ctle #(
        `PASS_REAL(v_in, v_in),
        `PASS_REAL(v_out, v_out)
    ) dut_i (
        .v_in(v_in),
        .v_out(v_out)
    );

endmodule

`default_nettype wire
