import argparse
from pathlib import Path

from header import ttl_test_header

from bob.core import data_graph, dump

# Adjust to the actual API — this mirrors your docs' template pattern
from bob.template import EquipmentFromTemplate, config_from_yaml

model_name = Path(__file__).stem

def example_code():
    # YAML (co-located with this script)
    yaml_path = Path(__file__).with_name("fan_device.yaml")
    cfg = config_from_yaml(str(yaml_path))
    node = EquipmentFromTemplate(config=cfg, label="SF-1") #noqa F841


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
