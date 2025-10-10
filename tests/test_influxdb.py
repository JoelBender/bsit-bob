from pathlib import Path

from .header import ttl_test_header

from bob.core import bind_model_namespace, dump
from bob.externalreference import influxdb

model_name = Path(__file__).stem
_namespace = bind_model_namespace("ex", f"urn:ex/{model_name}/")

def test_create_influxdb(bob_fixture):
    influxdb_server = influxdb.InfluxDBServer(
        label='my_influxdb_server',
        url="http://localhost:8086",
        organization="my_org",
        influxdbAuthenticationMethod="API Token",
        influxdbTokenLocation="env:INFLUXDB_TOKEN"
    )

    influxdb_ref = influxdb.InfluxDBReferenceV2( #noqa F841
        label='my_V2_influxdb_ref',
        server=influxdb_server,
        bucket="my_bucket",
        measurement="my_measurement"
    )

    influxdb_ref_v3 = influxdb.InfluxDBReferenceV3( #noqa F841
        label='my_V3_influxdb_ref',
        server=influxdb_server,
        database="my_bucket",
        table="my_measurement"
    )

    dump(filename=f"tests/ttl/{model_name}.ttl", header=ttl_test_header(model_name))