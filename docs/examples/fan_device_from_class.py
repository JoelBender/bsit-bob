import argparse
from pathlib import Path

from header import ttl_test_header

from bob.core import data_graph, dump

# Adjust to the actual API — this mirrors your docs' template pattern
from bob.equipment.hvac.fan import Fan

model_name = Path(__file__).stem

def example_code():
    # Now create a Fan using the class, not the template
    fan = Fan(label="SF-2", comment="Fan created from class") #noqa F841
    # the fan will be added as a Node in the graph


# Main function to parse arguments and run the example
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, required=True, help="Output TTL path")
    args = ap.parse_args()

    example_code()

    ttl_path = args.out
    dump(
        data_graph,
        filename=f"{ttl_path}",
        header=ttl_test_header(model_name),
    )
    print(f"[example] wrote {ttl_path}")

if __name__ == "__main__":
    main()
