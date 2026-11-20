# Bus-Based Snooping Cache Coherence Simulator

## Overview

An event-driven cache coherence simulator developed in Python for the High Performance Computing course.

The simulator models multiple processors with private caches communicating through a shared bus and accessing shared main memory.

## Supported Protocols

- Write-Invalidate Write-Through
- Write-Invalidate Write-Back (Ownership)
- Goodman's Write-Once

## Features

- Configurable system with 1–3 processors.
- Support for 1–3 shared memory variables.
- Read, Write and Replace operations.
- Automatic cache state transitions.
- Cache invalidation and memory write-back.
- Dynamic input file parsing and configuration validation.
- Detailed operation trace tables.
- Final memory and cache state summaries.
- Execution statistics.

## Project Structure

```text
CacheCoherenceSimulator/
├── main.py
├── cache.py
├── memory.py
├── bus.py
├── protocols.py
├── simulator.py
├── parser.py
├── input.txt
├── README.md
├── .gitignore
└── tests/
    ├── benchmark1_wt.txt
    ├── benchmark1_wb.txt
    ├── benchmark1_wo.txt
    ├── benchmark2_wt.txt
    ├── benchmark2_wb.txt
    ├── benchmark2_wo.txt
    └── edge_cases.txt
```

## System Architecture

| Component | Responsibility |
|---|---|
| CacheBlock | Stores the tag, value and coherence state. |
| Cache | Manages each processor's private cache blocks. |
| MainMemory | Stores shared memory variables. |
| SharedBus | Handles snooping, invalidation and memory transactions. |
| Protocols | Implements the three cache coherence algorithms. |
| Parser | Parses and validates input configurations. |
| CoherenceSimulator | Executes operations, records traces and calculates statistics. |

## Requirements

- Python 3
- No external libraries required.

## How to Run

Run the default input file:

```bash
python main.py
```

Run a specific input file:

```bash
python main.py tests/benchmark1_wt.txt
```

## Input Format

```text
PROTOCOL: WRITE_INVALIDATE_WRITE_BACK
MEMORY: X=5, Y=10
PROCESSORS: P1, P2

P1: Read(X)
P2: Read(X)
P2: Write(X, 15)
P1: Read(X)
P2: Replace(X)
```

The protocol, memory variables, processors and operation sequence can be configured without modifying the source code.

## Output

The simulator generates:

- Initial system state.
- Numbered operation trace table.
- Memory values after every operation.
- Cache values and coherence states.
- Final system state.
- Read-hit and read-miss counts.
- Write-hit and write-miss counts.
- Replacement counts.
- Bus invalidation counts.
- Update broadcast counts.
- Memory write-back counts.

## Testing and Verification

Seven test scenarios were executed:

| Test | Result |
|---|---|
| Benchmark 1 — Write-Through | Passed |
| Benchmark 1 — Write-Back | Passed |
| Benchmark 1 — Write-Once | Passed |
| Benchmark 2 — Write-Through | Passed |
| Benchmark 2 — Write-Back | Passed |
| Benchmark 2 — Write-Once | Passed |
| Edge-case testing | Passed |

All seven tests produced the expected results according to the implemented protocol rules.

The tests cover multiple processors, multiple memory variables, cache hits and misses, ownership transfers, invalidation and block replacement.

## Implementation Assumptions

- Each memory variable represents one cache block.
- Cache replacement is explicitly requested through a Replace operation.
- Invalidated blocks retain their previous values but cannot be accessed as valid data.
- Invalidation statistics count broadcast commands rather than individual invalidated blocks.
- Write-Through transactions are counted separately from memory write-backs, with only write-backs reported in the execution statistics.
- Ownership transfers on write misses do not flush the previous owner's value to memory.
- Write-Once write misses acquire exclusive ownership and transition to DIRTY.

The benchmark outputs were checked against the expected behavior of the implemented rules. Direct textbook table comparison was not performed.
