import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles


# Reference model for gates
def logic_gate(sel, a, b):
    if sel == 0b000:  # AND
        return a & b
    elif sel == 0b001:  # OR
        return a | b
    elif sel == 0b010:  # NOT (ignore b)
        return (~a) & 1
    elif sel == 0b011:  # NAND
        return (~(a & b)) & 1
    elif sel == 0b100:  # NOR
        return (~(a | b)) & 1
    elif sel == 0b101:  # XOR
        return a ^ b
    elif sel == 0b110:  # XNOR
        return (~(a ^ b)) & 1
    else:
        return 0


@cocotb.test()
async def test_project(dut):
    dut._log.info("Starting Digital Logic Trainer Test")

    # Start clock
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    # Reset + init
    dut.rst_n.value = 0
    dut.user_project.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    await ClockCycles(dut.clk, 2)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 1)

    # Exhaustive test of gates
    for sel in range(7):
        for a in [0, 1]:
            for b in [0, 1]:
                dut.ui_in.value = (sel << 2) | (b << 1) | a
                await ClockCycles(dut.clk, 1)
                result = int(dut.uo_out.value)
                expected = logic_gate(sel, a, b)
                assert result == expected, \
                    f"Mismatch: sel={sel:03b}, a={a}, b={b}, got={result}, expected={expected}"

    # Test disable case
    dut.ena.value = 0
    dut.ui_in.value = (0b000 << 2) | (1 << 1) | 1  # AND gate, a=1, b=1
    await ClockCycles(dut.clk, 1)
    result = int(dut.uo_out.value)
    assert result == 0, f"Disable failed: got {result}, expected 0"

    dut._log.info("All tests completed successfully ✅")
