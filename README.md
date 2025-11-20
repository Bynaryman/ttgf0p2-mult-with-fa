![](../../workflows/gds/badge.svg) ![](../../workflows/docs/badge.svg) ![](../../workflows/test/badge.svg) ![](../../workflows/fpga/badge.svg)

# Tiny Tapeout GF180 – Multiplier with FA Targets

This project is a stripped-down Tiny Tapeout design whose only job is to multiply two 24-bit operands and present a reduction of the 48-bit product on `uo_out`.
Operand data streams in eight bits at a time over `ui_in`: three consecutive bytes become operand A, the next three bytes become operand B, and the pattern repeats.
The goal is to force the LibreLane/Yosys flow to emit dense adder structures (and ideally map them to the GF180 full-adder cells) while keeping the HDL simple.

## How it works

- Every `ena`-qualified clock edge captures the current `ui_in` byte. The first three bytes form operand A (LSB last), the next three form operand B, and the pattern repeats.
- Once either register shifts in a new byte, the design recomputes the registered 24×24 product. `uo_out[7:0]` always mirrors eight copies of a single reduction bit (`1` if any product bit is high, `0` otherwise); `uio` pins stay unused.
- There is no additional framing or stall behavior: the multiplier keeps integrating bytes as they arrive, even if the operands are only partially updated.

This gives us a deterministic sequential datapath with enough partial products to encourage the synthesis flow to build compressor trees, making it easier to spot whether `SYNTH_FA_MAP` takes effect.

## Repository layout

```
.
├── docs/              # Datasheet content (see docs/info.md)
├── info.yaml          # Tiny Tapeout metadata, pinout, authorship
├── src/
│   ├── project.v      # Streaming 24x24 multiplier
│   └── fa_map.v       # Techmap that ties Yosys $fa cells to GF180 adders
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

The regression drives a deterministic byte stream into the design, mirrors the streaming protocol in Python, and checks that the replicated reduction bit matches the model. A second test freezes `ena` to confirm the pipeline holds its output.
