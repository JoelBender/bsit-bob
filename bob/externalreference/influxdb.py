from rdflib import Literal

from ..core import BOB, Node, bind_namespace, prefixes  # type: ignore[attr-defined]
from .timeseries import TimeSeriesReference

_namespace = BOB

INFLUXDB = bind_namespace("influxdb", prefixes["influxdb"])


class InfluxDBServer(Node):
    """InfluxDB server
    """

    _class_iri = INFLUXDB.InfluxdbServer
    # _node_iri: URIRef = INFLUXDB.InfluxdbServer
    _attr_uriref = {
        "url": INFLUXDB["url"],
        "organization": INFLUXDB["organization"],
        "influxdbAuthenticationMethod": INFLUXDB["influxdbAuthenticationMethod"],
        "influxdbTokenLocation": INFLUXDB["influxdbTokenLocation"],
    }
    url: Literal
    organization: Literal
    influxdbAuthenticationMethod: Literal
    influxdbTokenLocation: Literal


class _InfluxDBReference(TimeSeriesReference):
    _class_iri = INFLUXDB.InfluxdbReference
    _attr_uriref = {
        "server": INFLUXDB["InfluxdbServer"],
        # Version 2
        "bucket": INFLUXDB["bucket"],
        "measurement": INFLUXDB["measurement"],
        # Version 3
        "database": INFLUXDB["database"],
        "table": INFLUXDB["table"],
        "tag": INFLUXDB["tag"],
    }
    server: InfluxDBServer
    bucket: Literal
    measurement: Literal
    database: Literal
    table: Literal
    tag: Literal


class InfluxDBReferenceV2(_InfluxDBReference):
    _class_iri = INFLUXDB.InfluxdbReference

    def __init__(self, server=None, bucket=None, measurement=None, **kwargs) -> None:
        if not isinstance(server, InfluxDBServer):
            raise TypeError(
                f"server must be an InfluxDBServer instance, got {type(server)}",
            )
        if bucket is None or measurement is None:
            raise ValueError("bucket and measurement are required")
        kwargs["server"] = server
        kwargs["bucket"] = bucket
        kwargs["measurement"] = measurement
        super().__init__(**kwargs)


class InfluxDBReferenceV3(_InfluxDBReference):
    _class_iri = INFLUXDB.InfluxdbReference

    def __init__(self, server=None, database=None, table=None, **kwargs) -> None:
        if not isinstance(server, InfluxDBServer):
            raise TypeError(
                f"server must be an InfluxDBServer instance, got {type(database)}",
            )
        if table is None or database is None:
            raise ValueError("table and database are required")
        kwargs["server"] = server
        kwargs["database"] = database
        kwargs["table"] = table
        super().__init__(**kwargs)
