"""
CLI tool to profile search performance
"""
import time
import sys
from utils.db import JLCPCBDatabase

def profile_search(component_type, value, package):
    """Profile a single search and print timing breakdown"""
    db = JLCPCBDatabase("cache.sqlite3")

    print(f"\n[*] Profiling {component_type} search: value='{value}', package='{package}'")
    print("="*60)

    # Open database
    start = time.time()
    db.open()
    db_open_time = time.time() - start
    print(f"Database open: {db_open_time*1000:.1f}ms")

    # Perform search with profiling
    start = time.time()
    if component_type == "resistor":
        results, timings = db.get_resistors(value, package, profile=True)
    else:
        results = db.get_capacitors(value, package)
        timings = {}
    search_time = time.time() - start

    print(f"\nTotal search:  {search_time*1000:.1f}ms")
    print(f"Results found: {len(results)}")

    # Detailed breakdown
    if timings:
        print("\nDetailed breakdown:")
        for key, val in sorted(timings.items(), key=lambda x: -x[1]):
            print(f"  {key:20s}: {val*1000:7.1f}ms ({val/search_time*100:5.1f}%)")

    print(f"\nTotal time (incl DB open): {(db_open_time + search_time)*1000:.1f}ms")

    return search_time, timings

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python profile_search.py <resistor|capacitor> <value> [package]")
        print("Examples:")
        print("  python profile_search.py resistor 1k 0805")
        print("  python profile_search.py capacitor 100n")
        sys.exit(1)

    component_type = sys.argv[1].lower()
    value = sys.argv[2]
    package = sys.argv[3] if len(sys.argv) > 3 else ""

    # Run multiple times for average
    print("\n" + "="*60)
    print("SEARCH PERFORMANCE PROFILING")
    print("="*60)

    times = []
    all_timings = []
    for i in range(3):
        print(f"\n[Run {i+1}/3]")
        t, timings = profile_search(component_type, value, package)
        times.append(t)
        all_timings.append(timings)
        time.sleep(0.5)

    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"Average search time: {sum(times)/len(times)*1000:.1f}ms")
    print(f"Min: {min(times)*1000:.1f}ms, Max: {max(times)*1000:.1f}ms")
