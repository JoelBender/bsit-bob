import copy
import re
import typing as t
from pathlib import Path

import yaml

from .core import Connection, Equipment, System
from .introspection import get_class_from_name


def template_update(base: t.Dict = {}, config: t.Dict = None, bases: t.List = None):
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
        thing = container[matches.pop(0)]

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
        thing = getattr(container, _key)
        # print(thing, _key)
        return (thing, _key)  # in case thing is None


def configure_relations(
    container: t.Union[Equipment, System], relations: t.List[t.Tuple[str, str, str]]
):
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

        # if source_element is None:
        #    source_element = container

        # if source_key is None:
        #    source = source_element
        # else:
        #    source = getattr(source_element, source_key, None)

        # if source is None and isinstance(source_element, Connection):
        #    source = source_element
        # elif source is None:
        #    raise AttributeError(f"Source {source_key} not found in {source_element} | container {container} | relation {relation}")

        if target_key is None:
            target = target_element
        else:
            target = getattr(target_element, target_key, None)

        if target is None and isinstance(target_element, Connection):
            target = target_element
        elif target is None:
            raise AttributeError(f"Target {target_key} not found in {target_element}")

        if operator == "=":
            if source is None:
                # print(equipment, source_key, target)
                try:
                    setattr(source_element, source_key, target)
                except AttributeError:
                    setattr(container, source_key, target)
                except TypeError as error:
                    print(error)
                    print("Container :", container)
                    print("Source :", source, source_key)
                    print("Target :", target, target_key)

            else:
                source = target
        elif operator == ">>":
            source >> target
        elif operator == "<<":
            source << target
        elif operator == "%":
            source % target
        elif operator == "mapsTo":
            source.mapsTo = target
        elif operator == "@":
            source @ target
        # no @ here as we are creating relation "inside" the equipment or system


class SystemFromTemplate(System):
    def __init__(self, config: t.Dict = None, **kwargs):
        _config = template_update(config)
        kwargs = {**_config.pop("params", {}), **kwargs}
        _relations = _config.pop("relations", [])
        super().__init__(_config, **kwargs)
        configure_relations(self, _relations)


def config_from_yaml(yaml_file: t.Union[str, Path] = None):
    if yaml_file is None:
        raise FileNotFoundError("No YAML file provided")
    else:
        yaml_file = Path(yaml_file)
    with open(yaml_file, "r") as file:
        yaml_content = yaml.safe_load(file)
    _text_values = ["label", "comment"]
    _dict = {}
    name = yaml_content["name"]
    params = yaml_content["params"]
    label = params.get("label", name)
    comment = params.get("comment", "")
    sensors = yaml_content.get("sensors", None)
    equipment = yaml_content.get("equipment", None)

    _dict["params"] = {"label": label, "comment": comment}

    def define_entities(entities: dict = None, entities_category: str = None):
        if entities is None:
            return
        _dict[entities_category] = {}
        for entity_name, entity_params in entities.items():
            # entity_label = entity_params['label'] if 'label' in entity_params else entity_name
            entity_label = entity_params.pop("label", entity_name)
            # print(entity_label, entity_params, f"Looking for {entity_params['class']}")
            entity_class = get_class_from_name(entity_params.pop("class"))
            # print('Found class', entity_class)
            # entity_comment = entity_params.pop('comment', '')
            _dict[entities_category][(entity_label, entity_class)] = {}
            for _name, _class_or_value in entity_params.items():
                _value = (
                    _class_or_value
                    if _name in _text_values
                    else get_class_from_name(_class_or_value)
                )
                _dict[entities_category][(entity_label, entity_class)][_name] = _value

    # print('Defining entities')
    define_entities(equipment, "equipment")
    define_entities(sensors, "sensors")
    _dict["relations"] = []
    _relations = yaml_content.get("relations", [])
    for _relation in _relations:
        _relation = _relation.replace("(", "").replace(")", "").strip()
        _a, _b, _c = _relation.split(",")
        _dict["relations"].append((_a.strip(), _b.strip(), _c.strip()))
    return _dict
