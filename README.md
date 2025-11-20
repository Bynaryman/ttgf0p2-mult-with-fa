![](../../workflows/gds/badge.svg) ![](../../workflows/docs/badge.svg) ![](../../workflows/test/badge.svg) ![](../../workflows/fpga/badge.svg)

# Tiny Tapeout GF180 – Multiplier with FA Targets

This project is a stripped-down Tiny Tapeout design whose only job is to multiply two 4-bit operands from the UI bus and present the 8-bit product on `uo_out`.
The logic is intentionally tiny so we can experiment with enabling LibreLane/Yosys adder mapping and watch whether the flow starts using the full-adder cells provided by the GF180 PDK.
With the default configuration the pipeline is purely synchronous: operands are sampled every clock cycle (when `ena=1`) and the registered product feeds the output pins.

## How it works

- `ui_in[3:0]` carries operand A and `ui_in[7:4]` carries operand B.
- On each rising edge of `clk`, the module multiplies the two multiplicands and stores the product in a register (reset clears it to zero).
- `uo_out[7:0]` mirrors the registered product; `uio` pins are unused.

This gives us fully deterministic combinational logic plus one register stage, which is enough arithmetic structure for the synthesis flow to either keep generic adders or apply the FA/RCA mappings we plan to toggle.

## Repository layout

```
.
├── docs/              # Datasheet content (see docs/info.md)
├── info.yaml          # Tiny Tapeout metadata, pinout, authorship
├── src/
│   └── project.v      # Single-file design with the tt_um_binaryman_multfa top
├── test/
│   ├── Makefile       # Cocotb + icarus targets
│   ├── tb.v           # Simple structural testbench
│   └── test.py        # Cocotb regression that exercises a few operand pairs
└── README.md
```

## Testing

```
pip install -r test/requirements.txt
make -C test         # Cocotb + Icarus
make -C test sim     # Icarus-only smoke test
```

The regression sweeps several operand pairs, waits one cycle for the registered product, and asserts that the observed `uo_out` matches the expected multiplication result.
