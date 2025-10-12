# Treatise on Domain-Centric and Cross-Domain Modeling
#### Christian Tremblay, P.Eng.
#### 2022-03-12

Over the last weeks, Strike Team Bravo has been trying to get to a consensus on
modeling the relationships between Equipment that provide domain specific services
to the topological model of the rooms in a facility called a **connection**.

One of the starting point for the modeling effort when it first changed from
being the *Application Profiles* working group to the *Semantic Interoperability*
Working Group and adopting Semantic Web technologies was the Smart Applications
REFerence ontology (SAREF).

One of the ontologies within the SAREF family is called SAREF For Systems
(SAREF4SYS).  It is a **system-centric** view where systems are an abstract
concept and are **connected** defined as:

> A connection between two s4syst:Systems, modelled by s4syst:connectedTo,
> describes the potential interactions between connected s4syst:Systems. A
> connection can be qualified using class s4syst:Connection. 

The other starting point for the SI-WG work was ASHRAE Guideline 36 (G36),
High Performance Sequence of Operations, and with it the schematic view of
BAS components like dampers, coils, fans, and the topological organization of
those components.

These two starting points were merged together, renaming "system" to "Equipment"
to make it more easily understood by the BAS audience.  This is similar to the
"equipment" view from Brick and Haystack.  At some point this text was
introduced into the model in the Container clause:

> This clause is the top level of the hierarchical structure of the portion of
> the model that represents the concept of a physical connection between
> Equipment. Examples of physical things that are represented by a connection are
> ducts, pipes, and wires.

At this point "Equipment" stopped being an abstract concept to a physical thing
and "potential interactions" was changed to physical things but it remained
being a relationship with a conceptual thing "space".

The next change was to make a distinction between a room and a portion of a
room specific to a particular service, so earlier concepts of "enclosure" and
"space" were renamed to **physical space** and **domain space**.

Now the debate is to (1) maintain the connection between the Equipment providing
a service and the domain space receiving the service, or (2) tighten the
restriction a connection to being between physical things and introduce a new
relationship for referring to a domain space.

The former, a **domain-centric** approach, is a way to define relationships
between entities by respecting the field of interest.  The latter, a
**cross-domain** approach, places all of the services into a physical space.

## Building services are domain-centric

Apsects of the building are managed in a domain-centric way. Different people
(experts) will work on different aspects. You will see some overlap sometimes
but not that often. Domain-centric will feel familiar to domain experts.

## Blueprints are domain-centric

Architectural, structural, mechanical, and electric distribution plans each
have their own organization and portions of the drawings can be interpreted
without needing a dependency on other parts. 

Very often, the HVAC Control system will be presented schematically. You can see
typical schema presenting 1 VAV box that will be repeated *x* times. You will get
a vague notion of the physical spaces (rooms) but it is not required to have
all the details of the room to understand how it works.

## Modeling can also be domain-centric

It will be common to see models built by different teams as finding one person
knowing everything about all domains for a building will be hard to find. We
can imagine that an HVAC contractor will build its part of the model. Lighting
expert will do the lighting part. Intrusion/Access/Security team will build
their part, and so on.

The architect also will build its part (physical space).

Each of those teams should be able to build a working model out of their
knowledge and work without requiring the work of others.  For example, an HVAC
engineer should be able to build an HVAC schematic without also requiring the
electrical distribution system to be modeled.  When both "layers" of the
model are available in the same graph, there should be a mechanism to allow
them to reference each other, for example, if the electrical distribution system
includes a meter then it can be associated with specific loads.

While there are modeling questions that cannot be answered without multiple
domains linked together, allowing the teams to work independantly will improve
the modeling process.

# Cross-domain approach

In this approach, as soon as entities providing a service to to a domain space
within a room need to be connected, they must first be connected to the physical
space. The physical space is then filled with all sort of connection points,
with different medium to assure the relationships with entities.

To keep track of the domain in which the entities are, the additional
`servesDomainSpace` is used.

This approach creates a change of layer for any entity related to a room by
mixing multiple domain connection points on the same entity.

Physical Spaces in this approach are very similar to Equipment. In fact, an
entity, connectable, with connection points in different domains it is in s223
everywhere else known as a Equipment.

## What are the downsides of everything connected to the physical space?

First, this means that a physical space is mandatory, it will always be
required. So in the process of developing a model, this dependency will eventually
create the need for each teams to build their own physical spaces. A certain
point in time, there will be a need to merge of all those different points of
view of physical spaces coming from different models and reconcile the room
identifiers (URIs).

There will be times where not everything will be completed by all the teams and
things may change. There is no reason for an HVAC team to wait for the model
coming from the architect team to build a HVAC model for 1 AHU and 20 VAV Boxes
for 20 offices. 

There are also situations where the attributes of physical spaces doesn't
impact a domain model.

The modeler may also just be starting to design a very complicated building where
it may not be necessary to consider doors or windows in the model.

Teams could start with a very simple or approximate physical spaces model,
but as you are not the domain-expert, chances are that your model will be wrong.

# Advantages of domain-centric approach

## Interoperability of model sections

As I explained previously, models could be built by different teams. Once
everyone will have built their part of the model, there is nothing to modify in
the said model of each teams. Physical spaces will be defined to "enclose"
domain spaces based on the architecture of the building.

Inside a room, multiple domain spaces can cohabit and overlap. This is not an
issue. 

All sensors are treated the same way, installed in a room or not. 

All domains work the same way so you don't need to be an domain-expert to browse
other models.

## Scalability

Adding new domain-centric parts to a model is easy. The entities added are not
typically overlapping with other models.

The only thing required is (if required) to enclose new domain spaces in
existing physical spaces. 

Cross-domain models do not need to to modify the physical spaces to add more
connection points.

## Maintenance, localisation and interoperability

When physical spaces are created, it becomes possible for teams (or the
maintenance team eventually) to use the `hasPhysicalLocation` to relate things
to the physical space and answer the questions like:
_"Where is the discharge air temperature sensor located ?"_.

The domain-centric approach allows to locate Equipment and sensors easily using
this predicate when this information is available. 

It's also important to note that this information (`hasPhysicalLocation`) will
be added in the domain-centric parts of the model, which means that once people
are aware of physical spaces in the model, they can modify their part of the
model to add this information without touching everyone else part. This also
allow simultaneous work from different teams.

The cross-domain approach also uses `hasPhysicalLocation` but not for sensors
installed in rooms where `hasObservationLocation` must be used to find them.

# Going back to definitions

It is essential to be in phase with the meaning of the terms we use.

## Connection and Medium

There should only be 1 medium per connection and connection points.

## Physical Space is not "physical truth"

A Physical space is not more "physical truth" than any other domain... it is
just another aspect or "domain" of the physical truth (reality?), related to
physical aspects (height, weight, width, position, etc). 

At some extent, this could be called architectural domain space. A field of
interest consisting of everything covered by architecture.

Physical truth, reality, can only be defined by the addition of all the layers
(domains) modeled and all the other ones that are not (which are probably
infinite).

A connection in HVAC domain is not a duct... a segment, a junction, a connection
point... nothing of that is real.  Even a `s223:Coil` is not a "physical coil"
as-in "physical truth". It's a model of a physical coil limited to the
properties defined. 

For example, I could model a water coil without any water connection points.
Just because I'm only interested in the "air" domain. I am then modeling only
one aspect of this coil. It has no size, no shape, no color, no physical
location, no water connections points... Physical truth really means nothing
here. It's just fields of interest.

> Similar to any mathematical equation that would describe our reality. The
> variables are not bound to any "physical truth". They are just there to model
> one aspect of reality. A shortcut that help understand reality, not embrace
> every aspects of it... And there is a place for different models
> ...think Newton gravity laws vs Relativity, there is no physical truth there,
> just numbers and symbols. And both allow us to model our reality on different
> aspects.

# Origins

When we first defined DomainSpaces, we were trying to create a thing, an entity,
that would represent a region of interest inside a room (a space). This region of
interest is sometimes as big as the room itself, but not necessarily. 

> **Example**
> 
> Ehe Big Garage example has 4 walls, but with two distinct lighting spaces;
> one near the entry, the other one in the back. Domain spaces allow to split
> physical spaces in different zone of interest, without having to subdivise
> the physical spaces with smaller physical spaces that would have no wall, no
> boundaries.

## What are physical spaces

The definition of a PhysicalSpace was done as a way to distinguish a "space" or
"enclosure" from a domain space to facilitate the modeling of a room, floor or
building.  The alternatives were to subclass "space" but it could lead to
interopability problems as modelers selected different instances.

Note that the Building Topology Ontology (BOT) describes everything in terms of a
Zone which has a different meaning in the HVAC industry which uses it to collect
together "spaces" according to the delivery of a specific service.

Physical spaces came soon after the creation of domain spaces as a way to
anchor a domain spaces within the physical environment by providing a
relationship (originally called "contains" and then renamed to "encloses")
between them.  This relationship helps provide boundaries to the spaces and
explicitly tell that spaces HVAC, Lighting, Access Control are inside the same room.

Subdividing the PhysicalSpace concept with identifiers such as rooms, floors,
and buildings is left to other models such as BOT and Real Estate Core (REC).

A physical space can contain other physical spaces but a domain space cannot
overlap two adjacent physical spaces. In other words, a domain space is no
larger than the smallest physical space that encloses it.

## Finding entities

`hasPhysicalLocation` is a perfect fit for any Equipment, sensors, system, when
required, to be able to specify the location inside a building for those
entities. When provided, it provides a direct relationshiip to query to find
the location of something in a building.

> **Cross-domain approach**
> 
> One collateral effect of the cross-domain approach is the need to treat room
> sensors differently than other sensors. Remember, using cross-domain, the
> room temperature sensor is connected to the physical space, the light
> occupancy sensor too. To find the domain where the measure is taken and stay
> on the same layer of interest, we need to use `servesDomainSpace` predicate.
> But the return air temperature is still using `hasObservationLocation` on a
> connection point which is not findable by the physical space. This means that
> different set of queries will be needed to find sensors in one system. 

## Sensors

Sensors are subclasses of Equipment but are special in the way that the medium
will not typically pass through them. They are used to make a measurement at a
certain point in the flow of the medium.

Knowing where this measurement takes places is important. This is why typical
sensors are associated with connection points or connections using
`hasObservationLocation`.  The physical location of a sensor is not as important
to a domain specialist, it would be more important for maintenance and repair to
help locate the sensor in the "real world" rather than in the "schematic".

> Connection points and connections are defined by their medium, what is inside
> this duct, pipe, wire, etc. As sensors makes measurement of a property inside
> a medium, this relationship makes perfect sense.

## Sensors in rooms

In a domain-centric approach, when a sensor measures a property of space,
`hasObservationLocation` is connected to the domain space. The domain space
connection points are defined by compatible medium (ex. HVAC domain space uses
medium Air). In this case, the temperature sensor measures the temperature of
the air inside this space. 

> **Compatible Medium**
> 
> In the domain-centric approach, adding an `electricalInletConnectionPoint` to
> a HVAC Domain space would be an error as `Medium-Electricity` connections
> should be part of the `Electricity` domain. This is what compatible medium
> means. Rules shall be defined in the standard to define what medium are
> compatible with domains.

### Using cross-domain approach

In cross-domain, you connect the sensor to the physical space. But in the case
where the physical space is large, (think of a really long corridor in a mall)
this connection brings ambiguity that has to be resolved with an addition
relationship `servesDomainSpace` but that requires path traversal to go from
the HVAC domain, to the physical domain, just to return to the HVAC domain to
find the information we need. 

### Uniformity of sensors and queries

In the domain-centric approach, room sensors are no different than any other
sensors. They are all related to connection or connections points residing in
the same domain.

For any sensors in the model, 

- You need to know where a measurement is taken : `hasObservationLocation`
- You need to know where a sensor is physically : `hasPhysicalLocation` <- a clear jump to another domain

> It can also be noted that even if `hasPhysicalLocation` is not defined for a
> room sensor in the domain-centric approach, it is possible to find the
> physical space by finding the HVAC domain space and find which physical space
> encloses this domain space.

# Physical Space Connections and connection points

As seen earlier, connections and connection points are a way to model the fact
that a certain medium is flowing through something. 

**What medium could be compatible with a physical space domain ?**

## Door Example

Before answering the question on physical spaces medium, I think we could start
by modeling a door. We can imagine a door in the physical space as an important
part of relationships between physical spaces.

Consider a door modeled as a physical Equipment, very similar to damper. The door
can be controlled, open or close automatically or manually, monitored and can
affect its environment.

All aspects of the door can clearly be defined by the domain-centric approach
by layering the different concepts and making a clear boundary between them.  

### Airflow

When studying air flow (HVAC domain of interest), this door has a pair of
bidirectional air connection points. This connection point could be used to
make a specific relationship to the HVAC spaces of interest. So for now, if someone is interested by the impact of a
door on airflow, starting from the HVAC Domain will allow to quickly find the
door.

### Access control and security

If the door is "smart" and provides access control and communications, we can
monitor this door by adding an `intrusionDetected` property to the Equipment, in
addition to other observable properties the door might have such as being open
or closed.

### Light

When light can pass through this door, we can add a `LightConnectionPoint` and
depending on the situation as understood by the domain expert, this can be
unidirectional or bidirectional and connected to the light domain space.

## What are the connections and connection point in regard to physical spaces ?

In the domain-centric approach, connection points added to domain spaces must
be compatible with the domain of interest. By demonstrating the door example,
I wanted to show that all aspects of the door is related to the different fields
of interest. Airflow, access control, each of those aspect is covered by a
domain space **if required**. And this is a major point. Spaces are used to
model fields of interest. If there is no interest, there is no obligation to
model those aspects. 

But when connecting physical spaces together, the model presents (a) some kind
of medium (undefined for now), or (b) leaves the physical space connections
without a medium and assumes that every medium is somehow implicitly connected.

> In the domain-centric approach we currently do not allow connections to be
> made outside of the field of interest.

# Sharing information between domain spaces

This is an important point and real buildings are actually doing this, sharing
information from one domain to another domain. And it's always made using some
kind of **controller**. An HVAC system that can use the light occupancy sensor
to adjust the temperature setpoint for example.
**This is not done at the "application" layer, not at the Equipment layer.**
It is the result of an algorithm, a function block and in the context of s223.

In both a domain-centric and cross-domain approaches, sharing information
across domains requires the abstraction provided by function blocks.

## If everything was in the physical space?

In the cross-domain approach, entities inside rooms are connected to the
physical space. But putting everything in the same jar isn't sufficient to
demonstrate the interactions between entities. At some point, systems and
function blocks will be required. Relationships will be required and this will
not be easier to find them inside the physical space as you will have to make
different queries to find information which are not in physical spaces.

Connecting entities to a physical spaces using cross-domain approach is the
equivalent of treating the room as a Equipment. It is not a way to learn more
things about the relationship of connections. It doens't make requests easier.
It is not a replacement for systems and or function blocks.

---- clip ----

# Sharing information with other data-driven services

BIM, maintenance softwares, haystack, brick, they will all work in a
domain-centric way. By keeping our side organized with strong boundaries
between domain spaces, it will be easier to build gateways between s223 world
an others.

> I call gateway an entity that would serves alignment between s223 and another
> external system.

## Gateways

Physical spaces could be bound to BIM or other maintenance systems. As an
example, a `s223:System` could be used to align the physical spaces ontology
to BIM ontology. By not including all connection points from other domains, we
make it simple and maintainable. The same applies for all other domains that
could be aligned to other ontologies.

For haystack, there could be a query over the model that would create a system
to align the different pieces required by presenting tag equivalents. 

Energy modeling will also benefit from domain-centric approach as all connection
points for specific medium will be available directly in the space of interest.
ex. This could allow to estimate the impact of a radiant heater and a Windows
on a specific part of a physical space (namely a HVAC domain space) by using
direct relationship. 

# Conclusion

Domain-specific approach eliminates the need for different predicates to build
queries on sensor depending on their location.

This approach allows teams to work on their part of the model without having
strong dependencies between each other work.

Domain-specific approach is close to the reality of buildings and the nature of
work done in them (domain-expert driven).

For those reasons and all the other presented here I'm convinced that the
domain-centric approach is superior and easier to implement than the
cross-domain approach. I already built different models and the flexibility of
this approach has been proven each times. 

