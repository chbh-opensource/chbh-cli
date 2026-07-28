import os
import re
from datetime import datetime, timedelta
from collections import Counter

TIME_FMT = "%a %b %d %H:%M:%S %Y"

def parse_hms(s):
    h, m, s = map(int, s.split(':'))
    return h * 3600 + m * 60 + s

def parse_file(path):
    cpu = mem = wall = None
    start = end = None
    req_cpu = req_mem = req_wall = None
    state = exitcode = reason = None

    with open(path) as f:
        text = f.read()

    # Usage
    m = re.search(r'CPU Utilized:\s*(\d+:\d+:\d+)', text)
    if m:
        cpu = parse_hms(m.group(1))

    m = re.search(r'Job Wall-clock time:\s*(\d+:\d+:\d+)', text)
    if m:
        wall = parse_hms(m.group(1))

    m = re.search(r'Memory Utilized:\s*([\d.]+)\s*GB', text)
    if m:
        mem = float(m.group(1))

    # Requested
    m = re.search(r'Requested cpu=(\d+),mem=(\d+)G.*-\s*(\d+:\d+:\d+) walltime', text)
    if m:
        req_cpu = int(m.group(1))
        req_mem = float(m.group(2))
        req_wall = parse_hms(m.group(3))

    # Timing
    m = re.search(r'Starting at (.+?) for', text)
    if m:
        start = datetime.strptime(m.group(1), TIME_FMT)

    m = re.search(r'Finished at (.+?) for', text)
    if m:
        end = datetime.strptime(m.group(1), TIME_FMT)

    # State + exit code
    m = re.search(r'State:\s*([A-Z]+)', text)
    if m:
        state = m.group(1)

    m = re.search(r'Exitcode\s+(\d+:\d+)', text)
    if m:
        exitcode = m.group(1)

    # Failure reason (two possible formats)
    m = re.search(r'JobState\s+\w+\s+-\s+Reason\s+(.+)', text)
    if m:
        reason = m.group(1).strip()

    m = re.search(r'State:\s*FAILED\s+\((.+?)\)', text)
    if m:
        reason = m.group(1).strip()

    return cpu, mem, wall, req_cpu, req_mem, req_wall, start, end, state, exitcode, reason


def summarise(vals):
    vals = [v for v in vals if v is not None]
    return min(vals), max(vals), sum(vals) / len(vals)

def fmt_time(s):
    return str(timedelta(seconds=int(s)))

def main(directory):
    cpus, mems, walls = [], [], []
    cpu_props, mem_props, wall_props = [], [], []
    starts, ends = [], []
    states, exitcodes = [], []
    fail_reasons = []
    failed_files = []

    files = [f for f in os.listdir(directory) if f.endswith(".stats")]

    for f in files:
        (cpu, mem, wall, rcpu, rmem, rwall,
         start, end, state, exitcode, reason) = parse_file(os.path.join(directory, f))

        if cpu: cpus.append(cpu)
        if mem: mems.append(mem)
        if wall: walls.append(wall)

        if cpu and rcpu and rwall:
            cpu_props.append(cpu / (rcpu * rwall))

        if mem and rmem:
            mem_props.append(mem / rmem)

        if wall and rwall:
            wall_props.append(wall / rwall)

        if start: starts.append(start)
        if end: ends.append(end)
        if state: states.append(state)
        if exitcode: exitcodes.append(exitcode)

        if state and state != "COMPLETED":
            fail_reasons.append(reason or "UNKNOWN")
            failed_files.append(f)


    print(f"\nTotal files: {len(files)}")

    if starts and ends:
        print("\nRun window:")
        print(f"  earliest: {min(starts)}")
        print(f"  latest:   {max(ends)}")


    def print_table(title, rows):
        print(f"\n{title}")
        print("-" * 60)
        print(f"{'Metric':<20} {'Average':<15} {'Min':<15} {'Max':<15}")
        print("-" * 60)
        for name, avg, mn, mx in rows:
            print(f"{name:<20} {avg:<15} {mn:<15} {mx:<15}")
        print("-" * 60)

    # Build table data
    cpu_min, cpu_max, cpu_avg = summarise(cpus)
    mem_min, mem_max, mem_avg = summarise(mems)
    wall_min, wall_max, wall_avg = summarise(walls)

    table_rows = [
        ("CPU time", fmt_time(cpu_avg), fmt_time(cpu_min), fmt_time(cpu_max)),
        ("Memory (GB)", f"{mem_avg:.2f}", f"{mem_min:.2f}", f"{mem_max:.2f}"),
        ("Wall time", fmt_time(wall_avg), fmt_time(wall_min), fmt_time(wall_max)),
    ]

    print_table("Resource usage summary", table_rows)


    # Efficiency table
    eff_rows = []

    if cpu_props:
        eff_rows.append((
            "CPU efficiency",
            f"{sum(cpu_props)/len(cpu_props):.2%}",
            f"{min(cpu_props):.2%}",
            f"{max(cpu_props):.2%}"
        ))

    if mem_props:
        eff_rows.append((
            "Memory efficiency",
            f"{sum(mem_props)/len(mem_props):.2%}",
            f"{min(mem_props):.2%}",
            f"{max(mem_props):.2%}"
        ))

    if wall_props:
        eff_rows.append((
            "Walltime usage",
            f"{sum(wall_props)/len(wall_props):.2%}",
            f"{min(wall_props):.2%}",
            f"{max(wall_props):.2%}"
        ))

    if eff_rows:
        print_table("Efficiency summary", eff_rows)

    # States
    if states:
        print("\nJob states:")
        for s, c in Counter(states).items():
            print(f"  {s}: {c}")

    if exitcodes:
        print("\nExit codes:")
        for e, c in Counter(exitcodes).items():
            print(f"  {e}: {c}")

    # Failure reasons
    if fail_reasons:
        print("\nFailure reasons:")
        for r, c in Counter(fail_reasons).items():
            print(f"  {r}: {c}")

    if failed_files:
        print("\nFailed job files:")
        for f in failed_files:
            print(f"  {f}")



if __name__ == "__main__":
    import sys
    main(sys.argv[1])
