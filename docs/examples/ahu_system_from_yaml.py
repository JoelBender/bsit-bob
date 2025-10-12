import argparse
from pathlib import Path

from header import ttl_test_header

from bob.core import data_graph, dump
from bob.template import SystemFromTemplate, config_from_yaml

model_name = Path(__file__).stem

def example_code():
    yaml_path = Path(__file__).with_name("ahu_system.yaml")
    cfg = config_from_yaml(str(yaml_path))

    # Build the model from YAML (same pattern as fan_device.py)
    node = SystemFromTemplate(config=cfg, label="AHU-1") #noqa F841



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
