import copy
import importlib
import re
import typing as t
import warnings
from pathlib import Path


from .core import Connection, ConnectionPoint, Equipment, System, BOB
from .introspection import get_class_from_name

# Optional rich import
try:
    from rich import print as rich_print
    from rich.console import Console
    from rich.panel import Panel

    _RICH_AVAILABLE = True
    console = Console()
except ImportError:
    _RICH_AVAILABLE = False
    rich_print = print  # type: ignore
    console = None  # type: ignore
    Panel = None  # type: ignore


try:
    import yaml  # type: ignore
    _YAML_AVAILABLE = True

except ImportError:
    _YAML_AVAILABLE = False


def print_console(msg, style=None, panel=False):
    if _RICH_AVAILABLE:
        if panel and Panel is not None:
            console.print(Panel(msg, style=style if style else ""))
        else:
            console.print(msg, style=style if style else "")
    else:
        print(msg)


def template_update(
    base: t.Dict = {},
    config: t.Optional[t.Dict] = None,
    bases: t.Optional[t.List] = None,
):
    """
    This utility allows to preserve module templates from
    undesired modification during creation of Equipment.

    Usage :
    _config = template_update(template, user_provided_config_dict)

    """

    def merge_dict(existing, new):
        for k in new:
            if k in existing:
                if isinstance(existing[k], dict) and isinstance(new[k], dict):
                    merge_dict(existing[k], new[k])
                else:
                    existing[k] = new[k]
            else:
                existing[k] = new[k]

    if bases:
        d1, d2 = bases
        _d1 = copy.deepcopy(d1)
        _d2 = copy.deepcopy(d2)
        merge_dict(_d1, _d2)
        if config:
            merge_dict(_d1, config)
        return _d1

    else:
        _d = copy.deepcopy(base)
        if config:
            merge_dict(_d, config)
        return _d


def get_instance(container: t.Union[Equipment, System], blob: str):
    # print('Looking for : ', container, blob)
    if "[" in blob:
        matches = re.findall(r'\[["\'](.*?)["\']\]', blob)  # sub-equipment
        property_match = re.search(
            r"\.(?P<property>\w+)$", blob
        )  # property => .something
        thing = container[matches.pop(0)]  # type: ignore

        for each in matches:
            thing = thing[each]
        # print('thing : ', thing, property_match)
        if property_match:
            property_name = property_match.group("property")
            # try:
            #
            #    thing_property = getattr(thing, property_name)
            #    if thing_property is None:
            #        thing_property = thing # in case thing_property is None, we give the part before .something
            # except AttributeError:
            #    thing_property = None
            # print(thing_property, property_name)
            return (thing, property_name)  # in case thing_property is None
        # print(thing, None)
        return (thing, None)
    else:
        _key = blob.split(".")[1]
        # try:
        thing = getattr(container, _key)
        # except AttributeError:
        #    thing = container[_key]
        # print(thing, _key)
        return (thing, _key)  # in case thing is None


def configure_boundaries(container: System, boundaries: t.List[str]):
    if len(boundaries) > 0:
        print_console("[green]Configuring boundaries[/green]")
    for _target in boundaries:
        target_element, target_key = get_instance(container, _target)

        if target_key is None:
            target = target_element
        else:
            target = getattr(target_element, target_key, None)

        if target is None and isinstance(target_element, ConnectionPoint):
            target = target_element
        elif target is None:
            raise AttributeError(f"Target {target_key} not found in {target_element}")

        print_console(f"{container} [green]|[/green] {target}")
        container | target


def configure_relations(
    container: t.Union[Equipment, System], relations: t.List[t.Tuple[str, str, str]]
):
    if len(relations) > 0:
        print_console("[green]Configuring relations[/green]")
    for relation in relations:
        _source, operator, _target = relation
        source_element, source_key = get_instance(container, _source)
        target_element, target_key = get_instance(container, _target)

        if source_key is None:
            source = source_element
        else:
            source = getattr(source_element, source_key, None)
        if source is None and isinstance(source_element, Connection):
            source = source_element
        elif source is None:
            try:
                source = source_element[source_key]
            except KeyError:
                raise AttributeError(
                    f"Source {source_key} not found in {source_element}"
                )

        if target_key is None:
            target = target_element
        else:
            target = getattr(target_element, target_key, None)

        if target is None and isinstance(target_element, Connection):
            target = target_element
        elif target is None and isinstance(target_element, ConnectionPoint):
            target = target_element
        elif target is None:
            print_console(
                f"[yellow]Target {target_key} not found in {target_element}[/yellow]"
            )
            try:
                target = target_element[target_key]
            except KeyError:
                raise AttributeError(
                    f"Target {target_key} not found in {target_element}"
                )

        print_console(f"{source} [green]{operator}[/green] {target}")

        if operator == "=":
            if source is None:
                # print(equipment, source_key, target)
                try:
                    setattr(source_element, source_key, target)
                except AttributeError:
                    setattr(container, source_key, target)
                except TypeError as error:
                    print_console(f"[red]{error}[/red]")
                    print_console(f"[yellow]Container :[/yellow] {container}")
                    print_console(f"[yellow]Source :[/yellow] {source} {source_key}")
                    print_console(f"[yellow]Target :[/yellow] {target} {target_key}")
            else:
                source = target
        elif operator == ">>":
            source >> target
        elif operator == "<<":
            source << target
        elif operator == "%":
            source % target
        elif operator == "mapsTo":
            source.maps_to(target)
        elif operator == "@":
            source @ target
        elif operator == "|":
            source | target
        elif operator == "executes":
            source.executes(target)
        elif operator == "hasInput":
            source.hasInput(target)
        elif operator == "hasOutput":
            source.hasOutput(target)
        elif operator == "hasProperty":
            source.add_property(target)
        elif operator == "observes":
            source.observes = target


class SystemFromTemplate(System):
    def __init__(self, config: t.Dict = {}, **kwargs):
        _label = kwargs.get("label", config.get("params", {}).get("label"))
        print_console(
            f"[bold blue]Creating System {_label}[/bold blue]",
            panel=True,
            style="bold blue",
        )
        required_class = (
            config.pop("template_class") if "template_class" in config else [System]
        )

        _config = template_update(config)
        kwargs = {**_config.pop("params", {}), **kwargs}

        _relations = _config.pop("relations", [])
        _boundaries = _config.pop("boundaries", [])

        # Class mutation, we want a more explicit System maybe (ex. schema.org ProductGroup)...
        _tuple = (
            tuple(required_class) + (System,)
            if System not in required_class
            else tuple(required_class)
        )
        _classname = f"Dynamic{'_'.join(cls.__name__ for cls in required_class)}"
        DynamicClass = type(
            _classname,
            _tuple,
            {"_class_iri": BOB.DynamicSystem},
        )
        self.__class__ = DynamicClass

        print_console(
            f"Instanciating as {[klass.__name__ for klass in required_class]}"
        )
        DynamicClass.__init__(self, _config, **kwargs)  # type: ignore
        print_console("[green]✔ System created.[/green]")
        configure_relations(self, _relations)
        configure_boundaries(self, _boundaries)


class EquipmentFromTemplate(Equipment):
    def __init__(self, config: t.Dict = {}, **kwargs):
        print_console(
            f"[bold blue]Creating Equipment {config['params']['label']}[/bold blue]",
            panel=True,
            style="bold blue",
        )
        required_class: t.Any = (
            config.pop("template_class") if "template_class" in config else Equipment
        )
        _config = template_update(config)
        kwargs = {**_config.pop("params", {}), **kwargs}
        _relations = _config.pop("relations", [])

        # Class mutation, we want a more explicit Equipment maybe...
        _tuple = (
            tuple(required_class) + (Equipment,)
            if Equipment not in required_class
            else tuple(required_class)
        )
        _classname = f"Dynamic{'_'.join(cls.__name__ for cls in required_class)}"
        DynamicClass = type(
            _classname,
            _tuple,
            {"_class_iri": BOB.DynamicEquipment},
        )
        self.__class__ = DynamicClass
        print_console(
            f"Instanciating as {[klass.__name__ for klass in required_class]}"
        )
        DynamicClass.__init__(self, _config, **kwargs)  # type: ignore
        print_console("[green]✔ Equipment created.[/green]")
        configure_relations(self, _relations)


def config_from_yaml(yaml_file: t.Union[str, Path, t.Dict] = ""):
    if _YAML_AVAILABLE is False:
        raise RuntimeError(
            "PyYAML is not installed. Install with `pip install .[yaml]` or `pip install bob[yaml]`."
        )
    if yaml_file == "":
        raise FileNotFoundError("No YAML file provided")
    else:
        if isinstance(yaml_file, dict):
            yaml_content = yaml_file
        else:
            yaml_file = Path(yaml_file)
            if not yaml_file.is_file():
                raise FileNotFoundError(f"YAML file {yaml_file} not found")
            with open(yaml_file, "r") as file:
                yaml_content = yaml.safe_load(file)
    # those values will be taken as-is
    _text_values = [
        "label",
        "comment",
        "hasValue",
        "config",
        "vendorIdentifier",
        "objectIdentifier",
        "objectName",
        "description",
    ]
    _dict = {}
    name = yaml_content["name"]
    params = yaml_content["params"]
    _template_class = yaml_content["template_class"]
    template_class = []
    if isinstance(_template_class, list):
        for each in _template_class:
            template_class.append(get_class_from_name(each))
    else:
        template_class.append(get_class_from_name(_template_class))
    _dict["template_class"] = template_class

    label = params.get("label", name)
    comment = params.get("comment", "")
    sensors = yaml_content.get("sensors", {})
    equipment = yaml_content.get("equipment", {})
    properties = yaml_content.get("properties", {})
    functions = yaml_content.get("functions", {})
    connections = yaml_content.get("connections", {})
    junctions = yaml_content.get("junctions", {})
    connection_points = yaml_content.get("cp", {})
    bacnet = yaml_content.get("bacnet", {})
    influxdb = yaml_content.get("influxdb", {})  # noqa F841 Future use

    # boundaries = yaml_content.get("boundaries", None)

    _dict["params"] = {"label": label, "comment": comment}  # type: ignore
    # Schema.org parameters treated as kwargs
    try:
        for key, value in yaml_content.items():
            if key.startswith("params_"):
                class_name = key.split("params_")[-1]
                package = value.pop("package", None)
                if package is None:
                    raise KeyError(
                        f"params_{class_name} must have a 'package' key to be imported"
                    )
                try:
                    module = importlib.import_module(package)
                    getattr(module, class_name)
                except ImportError as e:
                    raise ImportError(
                        f"Could not import package '{package}' for params_{class_name}: {e}, parameters not supported."
                    )
                _dict["params"].update(value)  # type: ignore
    except ImportError as e:
        warnings.warn(
            f"Could not import parameters from YAML file: {e}. Parameters will not be applied."
        )

    def define_entities(entities: t.Optional[dict] = None, entities_category: t.Optional[str] = None):
        if entities is None:
            return
        _dict[entities_category] = {}  # type: ignore
        if entities_category == "cp":
            # if len(entities.items()) > 0:
            #    console.rule(f"[bold yellow]Defining {entities_category}[/bold yellow]")
            for entity_name, _entity_class in entities.items():
                # entity_label = entity_params['label'] if 'label' in entity_params else entity_name
                entity_class = get_class_from_name(_entity_class)
                entity_label = entity_name
                # ConnectionPoint
                _dict[entities_category][entity_label] = entity_class
                # console.print(f"    {entity_label} [green]:[/green] {entity_class}")
        else:
            # if len(entities.items()) > 0:
            #    console.rule(f"[green]Defining {entities_category}[/green]")
            for entity_name, entity_params in entities.items():
                # entity_label = entity_params['label'] if 'label' in entity_params else entity_name
                entity_label = entity_params.pop("label", entity_name)
                # print(entity_label, entity_params, f"Looking for {entity_params['class']}")
                try:
                    entity_class = get_class_from_name(entity_params.pop("class"))
                except KeyError:
                    raise KeyError(
                        f"Entity {entity_name} in {entities_category} does not have a 'class' key"
                    )

                # If no exception, we can define the entity
                else:
                    _dict[entities_category][(entity_label, entity_class)] = {}  # type: ignore
                    # console.print(f"    {entity_label} [green]:[/green] {entity_class}")

                    for _name, _class_or_value in entity_params.items():
                        _value = (
                            _class_or_value
                            if _name in _text_values
                            else get_class_from_name(_class_or_value)
                        )
                        # Here maybe I could look for hasattr in the class to check if the attribute exists and use its value
                        _dict[entities_category][(entity_label, entity_class)][  # type: ignore
                            _name
                        ] = _value
                        # console.print(f"        {_name} [green]:[/green] {_value}")

    # print('Defining entities')
    define_entities(equipment, "equipment")
    define_entities(properties, "properties")
    define_entities(sensors, "sensors")
    define_entities(connections, "connections")
    define_entities(junctions, "junctions")
    if connection_points is not None:
        define_entities(connection_points, "cp")
    # define_entities(boundaries, "boundaries")
    from_catalog = yaml_content.get("from_catalog", None)

    if from_catalog is not None:
        # console.print("[green]Importing entities from catalog[/green]")
        catalog_module, catalog_lookup_function = yaml_content.get(
            "catalog_source", ""
        ).split("|")
        importlib.import_module(catalog_module)
        get_template = getattr(
            importlib.import_module(catalog_module), catalog_lookup_function
        )

        for entity_name, entity_params in from_catalog.items():
            # console.print(f"    [purple]Defining {entity_name} from catalog[/purple]: ")
            # entity_label = entity_params['label'] if 'label' in entity_params else entity_name
            entity_label = entity_params.pop("label", entity_name)
            # print(entity_label, entity_params, f"Looking for {entity_params['template']}")
            _template = entity_params.pop("template")
            _addon = entity_params.pop("addon", None)
            try:
                template = get_template(_template)
            except FileNotFoundError:
                # maybe it's a file
                if not Path(_template).is_file():
                    raise FileNotFoundError(
                        f"Template {entity_name} not found in catalog {catalog_module}"
                    )
                elif Path(_template).is_file():
                    with open(Path(_template)) as _template_file:
                        template = yaml.safe_load(_template_file)
                else:
                    template = _template

            try:
                if _addon is not None:
                    with open(Path(_addon)) as _addon_file:
                        _addon_dict = yaml.safe_load(_addon_file)
                    template = template_update(template, _addon_dict)

                _template_config = config_from_yaml(template)

                if "System" in _template_config["template_class"]:
                    _dict["equipment"][(entity_label, SystemFromTemplate)] = {  # type: ignore
                        "config": _template_config
                    }
                else:
                    _dict["equipment"][(entity_label, EquipmentFromTemplate)] = {  # type: ignore
                        "config": _template_config
                    }

            except KeyError:
                raise KeyError(
                    f"Entity {entity_name} in equipment_from_catalog does not have a 'template' key"
                )
    define_entities(bacnet, "bacnet")
    define_entities(functions, "functions")

    _dict["relations"] = []
    if template_class[0] is System:
        _dict["boundaries"] = []

    def parse_sub(a, include_self=True):
        parts = [p.strip() for p in a.split(".")]
        if not include_self:
            expr = f"[{parts[0]}]"
        else:
            expr = f"self['{parts[0]}']"
        for part in parts[1:-1]:
            expr += f"['{part}']"
        if len(parts) > 1:
            expr += f".{parts[-1]}"
        return expr

    def parse_sub_properties(a):
        parts = [p.strip() for p in a.split(" / ")]
        expr = f"self['{parts[0]}']"
        for part in parts[1:]:
            expr += f"{parse_sub(part, include_self=False)}"
        return expr

    def add_to_relation_dict(line, operator, separator=","):
        line = line.replace("(", "").replace(")", "").strip()
        _a, _b = line.split(separator)
        _dict["relations"].append((parse_sub(_a), operator, parse_sub(_b)))
        # print(parse_sub(_a), operator, parse_sub(_b))

    def add_reference_to_relation_dict(line, operator, separator=","):
        """
        References are using properties which are accessed using the square brackets
        instead of the dot notation.
        In the template, we are using " / " to separate the property name
        from the object name.
        Keeping the parse_sub option for the last part as we can have the need to
        access a property of the property, like the bacnet presentValue.
        """
        line = line.replace("(", "").replace(")", "").strip()
        _a, _b = line.split(separator)
        _dict["relations"].append(
            (parse_sub_properties(_a), operator, parse_sub_properties(_b))
        )
        # print(parse_sub(_a), operator, parse_sub(_b))

    # Explicit relations with operator in the yaml file
    _relations = yaml_content.get("relations", [])
    for _relation in _relations:
        add_to_relation_dict(_relation, ">>", separator=",")

    # Relations using label, no self, no operator (implicit >>)
    # Generalize handling of all *_connections sections
    for key, value in yaml_content.items():
        if re.match(r".*_connections$", key) and isinstance(value, list):
            for _connection in value:
                add_to_relation_dict(_connection, ">>", separator=" -> ")

        if re.match(r".*mapsTo$", key) and isinstance(value, list):
            for _connection in value:
                add_to_relation_dict(_connection, "mapsTo", separator=" -> ")

        if re.match(r".*_executes$", key) and isinstance(value, list):
            for _connection in value:
                add_to_relation_dict(_connection, "executes", separator=" -> ")
        if re.match(r".*functions_inputs$", key) and isinstance(value, list):
            for _connection in value:
                add_to_relation_dict(_connection, "hasInput", separator=" -> ")

        if re.match(r".*functions_outputs$", key) and isinstance(value, list):
            for _connection in value:
                add_to_relation_dict(_connection, "hasOutput", separator=" -> ")
        if re.match(r".*_references$", key) and isinstance(value, list):
            for _connection in value:
                add_to_relation_dict(_connection, "@", separator=" -> ")
        if re.match(r".*_hasProperty$", key) and isinstance(value, list):
            for _connection in value:
                add_to_relation_dict(_connection, "hasProperty", separator=" -> ")
        if re.match(r".*_observes$", key) and isinstance(value, list):
            for _connection in value:
                add_to_relation_dict(_connection, "observes", separator=" -> ")

    # observation location
    observation_location = yaml_content.get("sensors_observation_location", [])
    for _observations in observation_location:
        add_to_relation_dict(f"{_observations}", "%", separator=" -> ")
    boundaries = yaml_content.get("boundaries", [])
    for _boundary in boundaries:
        # add_to_relation_dict(_boundary, "|", separator=" -> ")
        _dict["boundaries"].append(f"self | {parse_sub(_boundary)}")  # type: ignore
    return _dict
