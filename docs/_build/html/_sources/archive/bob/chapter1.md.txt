# Bob the SI-WG models builder

This package allows the creation of TTL files conforming to s223 Standard using RDF.

## Installation
### Clone the repo
First clone the repo found here : 
```bash
git clone https://bas-im.emcs.cornell.edu/223/si-builder.git
```

### install
Once the repo is on your machine, install it.

For example
```bash
pip install . #inside the repo
```

#### pipenv
You can also use virtual environments...

### First import
If everything went well, you should be able to import bob in the repl.

```Python
# ipython
import bob
```

## How it works
Bob uses rdflib Graph library to build an in-memory graph databse that can then be exported in a supported format. By default, 
TTL (Turtle will be used).

### Suggested files organization
Small models can be put inside one file. But things will quickly become complicated when  details will be added. 

One way of overcome this complexity is by splitting your models into files with clear fields of interest.

The way bob is made, it will support using imports of other files to build the model.

For example, here is an example of a folder containing different files with different goals. 
The model is built by executing the code on the file named `sample_pritoni_model.py`


# sample Pritoni
    - __init__.py
    - bacnet_reference.py
    - electrical_Equipment.py
    - electricity.poy
    - header.py
    - hvac_Equipment.py
    - hvac_spaces.py
    - hvac.py
    - lighting_Equipment.py
    - lighting_spaces.py
    - lighting.py
    - occupancy.py
    - physical_space.py
    - sample_pritoni_model.py

This is not the only way to do it, the idea is that we strongly suggest you organize your files to reduce complexity.

## Model files
### TTL
As explained previously, Bob will export the content of your model in the form of a TTL file. Turtle files are a human-readable
format for RDF models.

But the rdflib library allows for other type of export but this will not be covered here.

## s223 concepts
The goal here is not to cover s223 but only how Bob will deal with it. So let's proceed...

### Bob classes
Before starting to talk about Equipment and sensors, let's talk about class definitions in Bob.

Bob makes usage of type annotation to create classes. This way, it is possible to define all the properties 
with the right type.

For example, 

```Python
class NewClass(ExistingClass):
    node_type: URIRef = s223.NewClass
    airInlet: AirInletConnectionPoint
    airOutlet: AirOutletConnectionPoint
```

Here we define a new class that will inherit from the `ExistingClass` class. This means that this new Equipment will get all the properties and method of a `ExistingClass`. It will also being created with an identifier `s223:NewClass` given by `node_type` property. 

> node type
> 
> Those identifiers are defined in the standard if they start by `s223:`. Custom URI identifier, it is recommended to define a prefix in your model.

#### Defining a prefix
One way of deining a prefix for your model is by defining a special variable called `__namespace__`. 

```Python
__namespace__ = bind_model_namespace(model_name, f"urn:ex/{model_name}/")
```

> Joel will add some nice theory about graph and RDF here

#### Inheritance
When this new class will be instanciated, the `NewClass` property will be added. Then the ExistingClass magic will be injected in the NewClass.

#### Adding dynamic properties
Sometimes you need to add dynamic properties to the NewClass. When doing this, you need  not to define those properties in the annotated way we saw.

For example, I need an Electrical Inlet for my NewClass but this inlet will be defined at instanciation time based on a keyword argument. For this to work, 
we need to deal with inheritance first, then we add supplemental stuff.

Like this : 

```Python
class NewClass(ExistingClass):
    node_type: URIRef = s223.NewClass
    airInlet: AirInletConnectionPoint
    airOutlet: AirOutletConnectionPoint

    def __init__(self, **kwargs):
        _electricalInlet = kwargs.pop(electricalInlet)
        super().__init__(**kwargs)
        self.electricalInlet = get_class_from(_electricalInlet)
```

First we must define an `__init__` method. We remove the wanted parametr from kwargs.
We passed kwargs (minus the wanted param) to the parent class
Then after that, we add our new property using any logic required from the value that was given in argument.

For example : 

```Python
a_new_class = NewClass(label='NewClass_120V', comment='Super nice shiny new class', electricalInlet='120V')
```

> Label and Comment
> 
> Labels are mandatory when creating classes in Bob. Comments are not, but it is a good thing to provide one.

### Equipment
```
A Equipment is the modeling construct used to represent  a physical entity or piece of mechanical equipment that one might buy from a vendor - a tangible object designed to accomplish a specific task. Examples of possible Equipment include a pump, fan, heat exchanger, luminaire, temperature sensor, or flow meter.
```

In Bob, you can build a Equipment by subclassing `bob.core.Equipment`

#### Pre-made Equipment
To facilitate the work of building models, Bob propose already made Equipment. These will evolve with time. They are stored in the module
`bob.Equipment` and are organized by `domains`

- hvac
- electricity
- lighting
- etc (more to come)

### Connections, Connection points and Mediums
As you probably know, Equipment are connected together. Those "links" are made of a connection point, a connection, then another connection point. 

> Again, Joel will sparkle RDF details here.

For a connection to be made, it needs to be defined with the same Medium

> Medium
> 


### System


### Space


### Properties


### External References


### Domains


