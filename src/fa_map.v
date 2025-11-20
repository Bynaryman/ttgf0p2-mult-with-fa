// Techmap for Yosys full adders to GF180 full-adder standard cell.

(* techmap_celltype = "$fa" *)
module _gf180_fa_map (
    input  A,
    input  B,
    input  C,
    output X, // carry out
    output Y  // sum
);
    // Smallest drive strength variant; swap if timing requires.
    gf180mcu_fd_sc_mcu7t5v0__addf_1 _TECHMAP_REPLACE_ (
        .A  (A),
        .B  (B),
        .CI (C),
        .CO (X),
        .S  (Y)
    );
endmodule
