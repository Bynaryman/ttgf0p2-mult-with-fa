# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, ReadOnly, RisingEdge, Timer


class StreamingModel:
    """Reference model for the 24x24 streaming multiplier."""

    def __init__(self):
        self.op_a = 0
        self.op_b = 0
        self.phase = 0  # 0-2 load operand A, 3-5 load operand B

    @staticmethod
    def _shift(value: int, byte: int) -> int:
        return (((value & 0xFFFF) << 8) | (byte & 0xFF)) & 0xFFFFFF

    def step(self, byte: int, enabled: bool) -> int:
        if enabled:
            if self.phase < 3:
                self.op_a = self._shift(self.op_a, byte)
            else:
                self.op_b = self._shift(self.op_b, byte)
            self.phase = 0 if self.phase == 5 else self.phase + 1
        return (self.op_a * self.op_b) & ((1 << 48) - 1)


async def initialize_dut(dut):
    clock = Clock(dut.clk, 20, unit="ns")
    cocotb.start_soon(clock.start())

    dut.ena.value = 0
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 4)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 1)
    dut.ena.value = 1


@cocotb.test()
async def test_streaming_product_matches_reference(dut):
    await initialize_dut(dut)

    model = StreamingModel()
    # Deterministic, non-trivial byte stream.
    for idx in range(120):
        byte = (idx * 37 + 13) & 0xFF
        dut.ui_in.value = byte
        await RisingEdge(dut.clk)
        await ReadOnly()
        expected_bit = 1 if model.step(byte, True) != 0 else 0
        expected = 0xFF if expected_bit else 0x00
        actual = int(dut.uo_out.value)
        assert actual == expected, f"Mismatch at index {idx}"
        await Timer(1, unit="ps")


@cocotb.test()
async def test_disable_holds_last_product(dut):
    await initialize_dut(dut)

    model = StreamingModel()
    # Load six bytes (full set for both operands).
    for byte in [0x12, 0x34, 0x56, 0x78, 0x9A, 0xBC]:
        dut.ui_in.value = byte
        await RisingEdge(dut.clk)
        await ReadOnly()
        expected = 0xFF if model.step(byte, True) != 0 else 0x00
        await Timer(1, unit="ps")

    dut.ena.value = 0
    for byte in [0xDE, 0xAD, 0xBE, 0xEF]:
        dut.ui_in.value = byte
        await RisingEdge(dut.clk)
        await ReadOnly()
        # Output should stay frozen while ena is low.
        assert int(dut.uo_out.value) == expected, "ena low should freeze output"
        model.step(byte, False)
        await Timer(1, unit="ps")
