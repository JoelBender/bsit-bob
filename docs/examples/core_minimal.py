import argparse
from pathlib import Path

from header import ttl_test_header

from bob.core import Equipment, Property, data_graph, dump

model_name = Path(__file__).stem

def example_code():
    # Minimal model: one Equipment with one Property
    fan = Equipment(label="SF-1")
    fan_speed = Property(label="SF-1.Speed")
    fan.add_property(fan_speed)


# Main function to parse arguments and run the example
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, required=True, help="Output TTL path")
    args = ap.parse_args()
    example_code()
    dump(
        data_graph,
        filename=f"{args.out}",
        header=ttl_test_header(model_name),
    )
    print(f"[example] wrote {args.out}")

if __name__ == "__main__":
    main()
