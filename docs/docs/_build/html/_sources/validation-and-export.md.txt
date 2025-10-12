# Validation and Export

Validate with tests (Windows)
```bash
cd d:\0Programmes\Ashrae\si-builder
pytest -q
```

Common checks
- Medium compatibility (see test_media.py).
- Connection directions and CP types (connection-00x).
- Sensors observation/reference (sensor-00x).
- References (internal/external) bindings.

Exporting TTL
- si-builder builds an RDF graph; projects typically dump TTL during their own build step.
- Use the same patterns found in tests to serialize the graph in your pipeline.
