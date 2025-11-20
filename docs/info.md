<!---

This file is used to generate your project datasheet. Please fill in the information below and delete any unused
sections.

You can also include images in this folder and reference them in the markdown. Each image must be less than
512 kb in size, and the combined size of all images must be less than 1 MB.
-->

## How it works

`tt_um_binaryman_multfa` streams 8-bit chunks from the UI bus into two 24-bit shift registers and multiplies them together. The first three `ena`-qualified bytes fill operand A (LSB last), the next three bytes fill operand B, and the pattern repeats forever. Each time either register shifts, the 24×24 product is recomputed and stored; `uo_out[7:0]` mirrors eight copies of a single bit that goes high whenever any bit of the 48-bit product is high. Every `uio` pin remains unused (held as input).

## How to test

1. Install the Python requirements (`pip install -r test/requirements.txt`).
2. Run `make -C test` for the full Cocotb suite or `make -C test sim` for the Icarus-only path.
3. Inspect `test/results.xml` or `test/tb.vcd` for pass/fail information and waveforms.

The regression mirrors the byte-stream protocol in Python, drives a deterministic sequence of 8-bit values into `ui_in`, and compares the observed low byte of the product against the model each cycle. A second test drops `ena` to verify the output register freezes when the pipeline is disabled.

## External hardware

- Stream 8-bit values onto `ui_in[7:0]` while `ena` is asserted. Every three bytes update one operand register, and the following three update the other; no extra framing is required.
- Observe the replicated “product-nonzero” flag on `uo_out[7:0]` with LEDs, a logic analyzer, or a microcontroller.
- Leave all `uio` pins floating or tied low; they are unused inputs in this design.
