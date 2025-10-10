import argparse
from pathlib import Path

from header import ttl_test_header

from bob.core import data_graph, dump, System
from bob.equipment.hvac.fan import Fan
from bob.equipment.hvac.coil import ChilledWaterCoil

model_name = Path(__file__).stem

def example_code():
    ahu = System(label="AHU-2", comment="AHU created from class")
    fan = Fan(label="Fan-2", comment="Fan in AHU created from class")
    chilledWaterCoil = ChilledWaterCoil(label="ChWCoil-2", comment="Chilled Water Coil in AHU created from class")
    fan >> chilledWaterCoil
    ahu > fan 
    ahu > chilledWaterCoil


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
