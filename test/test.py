# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, ReadOnly, RisingEdge, Timer


def pack_operands(a: int, b: int) -> int:
    """Lower nibble is multiplicand, upper nibble is multiplier."""
    return ((b & 0xF) << 4) | (a & 0xF)


async def initialize_dut(dut):
    clock = Clock(dut.clk, 20, unit="ns")
    cocotb.start_soon(clock.start())

    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 4)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 1)


@cocotb.test()
async def test_all_operand_pairs(dut):
    await initialize_dut(dut)

    for a in range(16):
        for b in range(16):
            dut.ui_in.value = pack_operands(a, b)
            await RisingEdge(dut.clk)
            await ReadOnly()  # allow registered product to settle after the edge
            assert int(dut.uo_out.value) == a * b, f"{a}*{b} mismatch"
            await Timer(1, unit="ps")  # exit read-only before driving next vector


@cocotb.test()
async def test_disable_holds_last_product(dut):
    await initialize_dut(dut)

    dut.ui_in.value = pack_operands(3, 7)
    await ClockCycles(dut.clk, 1)
    expected = 21

    dut.ena.value = 0
    dut.ui_in.value = pack_operands(15, 15)
    await RisingEdge(dut.clk)
    await RisingEdge(dut.clk)

    await ReadOnly()
    assert int(dut.uo_out.value) == expected, "ena low should freeze the register"
