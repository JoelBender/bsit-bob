"""Performs validation of the model/schema and data files in the 223P repository
"""

import argparse
import logging
import os
import subprocess
import tempfile
from pathlib import Path
from typing import Optional

from rdflib import OWL, SH, Graph, Literal, Namespace

# logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

# globals
args = None

# working directory mapped as a volume in validate-run.sh
DATA_DIRECTORY = Path("/data")

S223 = Namespace("http://data.ashrae.org/standard223#")

MIN_ITERATIONS = 2
MAX_ITERATIONS = 4


def copy_graph(g: Graph) -> Graph:
    c = Graph()
    for t in g.triples((None, None, None)):
        c.add(t)
    return c


def test_data_validation(data_file_name: str, schema_file_name: str | None = None):
    """Validates a graphs in the /data/ folder against the data and model shapes

    WARNS but does not fail the test on a validation error for a shape with sh:Info severity
    """
    # load the data graph
    data_file_path = DATA_DIRECTORY / data_file_name
    data_file_root, _ = os.path.splitext(data_file_path)
    logger.debug(f"{data_file_path = }, {data_file_root = }")

    data_graph = Graph().parse(data_file_path, format="turtle")
    logger.debug(f"{len(data_graph) = }")

    # make a copy of the data graph
    model = copy_graph(data_graph)

    # add the schema file and ontology
    if schema_file_name:
        model.parse(DATA_DIRECTORY / schema_file_name, format="turtle")
    model.parse("223standard.ttl", format="turtle")

    # remove OWL imports
    model.remove((None, OWL.imports, None))

    # Create a temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir_path = Path(temp_dir)

        # run the inference until there's nothing new
        iteration_count = 0
        while iteration_count < MAX_ITERATIONS:
            iteration_count += 1
            logger.info(f"Running inference iteration {iteration_count}")

            # Define the target path within the temporary directory
            model_file_path = temp_dir_path / f"model-{iteration_count}.ttl"
            logger.debug(f"    - {model_file_path = }")

            # serialize the model
            model.serialize(model_file_path, format="ttl")
            logger.debug(f"    - {len(model) = }")

            # get the shacl-1.4.2/bin/shaclinfer.sh script
            script = "shacl-1.4.2/bin/shaclinfer.sh"
            try:
                logger.info(f"Running {script} -datafile {model_file_path}")
                output = subprocess.check_output(
                    ["/bin/bash", script, "-datafile", model_file_path],
                    stderr=subprocess.STDOUT,
                    universal_newlines=True,
                )
            except subprocess.CalledProcessError as e:
                output = e.output  # Capture the output of the failed subprocess

            # write the output to a file in the temporary directory
            inferred_file_path = temp_dir_path / f"inferred-{iteration_count}.ttl"
            with open(inferred_file_path, "w") as f:
                for line in output.splitlines():
                    if "::" not in line:
                        f.write(f"{line}\n")

            inferred_graph = Graph().parse(inferred_file_path, format="ttl")
            logger.debug(f"    - {len(inferred_graph) = }")
            # inferred_graph.serialize(sys.stdout.buffer, format="ttl")
            # print()

            inferred_triple_count = 0
            for trip in inferred_graph:
                if trip not in model:
                    logger.debug("    - %s", trip)
                    inferred_triple_count += 1

                    # add the inferred triple to the model
                    model.add(trip)

                    # add it to the data graph that will be saved as "compiled"
                    data_graph.add(trip)
            logger.debug(f"    - {inferred_triple_count = }")

            # nothing inferred that isn't already in the model
            if inferred_triple_count == 0:
                break

        # save the updated data graph as the compiled graph
        compiled_file_path = data_file_root + ".compiled.ttl"
        logger.debug(f"{compiled_file_path = }")
        data_graph.serialize(compiled_file_path, format="ttl")

        # skip the rest if we're not validating
        if args.skip_validation:
            return

        # get the shacl-1.4.2/bin/shaclvalidate.sh script
        script = "shacl-1.4.2/bin/shaclvalidate.sh"
        try:
            logger.info(f"Running {script} -datafile {model_file_path}")
            output = subprocess.check_output(
                ["/bin/bash", script, "-datafile", model_file_path],
                stderr=subprocess.STDOUT,
                universal_newlines=True,
            )
        except subprocess.CalledProcessError as e:
            output = e.output  # Capture the output of the failed subprocess

        # write the output to a file in the temporary directory
        report_file_path = temp_dir_path / "report.ttl"
        with open(report_file_path, "w") as f:
            for line in output.splitlines():
                if "::" not in line:  # filter out log output
                    f.write(f"{line}\n")

        # load it in and save a copy
        report_graph = Graph().parse(report_file_path, format="turtle")

        report_file_path = data_file_root + ".report.ttl"
        logger.debug(f"{report_file_path = }")
        report_graph.serialize(report_file_path, format="ttl")

    # find the prefix definitions so the select can find them
    namespace_map = {}
    for prefix, uriref in report_graph.namespaces():
        namespace_map[prefix] = Namespace(uriref)
    if "sh" not in namespace_map:
        namespace_map["sh"] = SH

    logger.debug(f"{namespace_map = }")

    # find the validation results
    qs = """
        SELECT ?resultSeverity ?sourceShape ?resultMessage ?focusNode ?value
        WHERE {
            ?report rdf:type sh:ValidationReport ;
                sh:result ?result .
            ?result sh:focusNode ?focusNode ;
                sh:resultMessage ?resultMessage ;
                sh:resultSeverity ?resultSeverity ;
                sh:sourceShape ?sourceShape .
            OPTIONAL { ?result sh:value ?value } .
            }
        """

    # pretty colors
    color_map = {SH.Violation: 33, SH.Info: 34, SH.Warning: 35, S223.g36: 36}

    # run the query, sort the results
    results = sorted(report_graph.query(qs, initNs=namespace_map))

    prev = None
    report_lines = []
    for resultSeverity, sourceShape, resultMessage, focusNode, value in results:
        if sourceShape != prev:
            color = color_map[resultSeverity]
            report_lines.append(f"\x1b[{color}m{resultMessage}\x1b[0m")
            prev = sourceShape
        report_lines.append(f"    {report_graph.qname(focusNode)}{' ' + str(value) if value else ''}")

    # save the report as text
    with open(data_file_root + ".report.txt", "w") as report_file:
        report_file.write("\n".join(report_lines) + "\n")

    if 0:
        # check if there are any sh:resultSeverity sh:Violation predicate/object pairs
        has_violation = len(
            list(
                report_graph.subjects(predicate=SH.resultSeverity, object=SH.Violation),
            ),
        )
        conforms = len(
            list(report_graph.subjects(predicate=SH.conforms, object=Literal(True))),
        )
        assert (not has_violation) or conforms


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Validate a graph against the data and model shapes",
    )

    # turtle files to load
    parser.add_argument(
        "data_file_name",
        type=str,
        help="data file to load",
    )
    # turtle files to load
    parser.add_argument(
        "schema_file_name",
        type=str,
        nargs="?",
        help="optional schema file to load",
        default=None,
    )
    # debug option
    parser.add_argument(
        "--skip-validation",
        action="store_true",
        help="run the inferencing but skip validation",
    )
    # debug option
    parser.add_argument(
        "--debug",
        action="store_true",
        help="turn on debugging",
    )

    # parse the args, turn on debugging
    args = parser.parse_args()
    if args.debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    test_data_validation(args.data_file_name, args.schema_file_name)
