<!---

This file is used to generate your project datasheet. Please fill in the information below and delete any unused
sections.

You can also include images in this folder and reference them in the markdown. Each image must be less than
512 kb in size, and the combined size of all images must be less than 1 MB.
-->

## How it works

`tt_um_binaryman_multfa` samples two 4-bit operands from the UI bus and registers their 8-bit product. `ui_in[3:0]` supplies operand A, `ui_in[7:4]` supplies operand B. On every rising edge of `clk`, if `rst_n` is asserted and `ena` is high, the operands are multiplied and the result is stored; the register resets to zero when `rst_n` goes low. `uo_out[7:0]` always reflects the registered product, and every `uio` pin is unused (held as input).

## How to test

1. Install the Python requirements (`pip install -r test/requirements.txt`).
2. Run `make -C test` for the full Cocotb suite or `make -C test sim` for the Icarus-only path.
3. Inspect `test/results.xml` or `test/tb.vcd` for pass/fail information and waveforms.

The regression drives several operand pairs, waits one clock for the registered product, and checks that `uo_out` matches the expected 8-bit multiply result after reset comes up.

## External hardware

- Drive the Tiny Tapeout UI bus with two 4-bit values (`ui_in[3:0]` = A, `ui_in[7:4]` = B). Update on the rising clock edge while `ena` is asserted.
- Observe the 8-bit registered product on `uo_out[7:0]` with LEDs, a logic analyzer, or a microcontroller.
- Leave all `uio` pins floating or tied low; they are unused inputs in this design.
