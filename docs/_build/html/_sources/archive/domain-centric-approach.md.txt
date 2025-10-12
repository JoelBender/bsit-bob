# Domain-centric approach
#### Christian Tremblay, P.Eng.
#### 2022-03-12

Over the last weeks, we struggled in trying to get to a consensus on the approach in modeling with s223.
Here are the reasons why I think the domain-centric approach should be adopted by opposition to the physical-truth approach (aka cross-domain).

> Domain-centric approach in the context of s223 is a way to define relationships between entities by respecting the fields of interest. It doesn't prevent exchange of information between domains and this will be explained.

## Building are actually domain-centric
Working in the HVAC domain for more than 20 years now, I know that all apsects of the building are managed in a domain-centric way.
Different people (experts) will work on different aspects.
You will see some overlap sometimes but not that often. Domain-centric will feel familiar to domain experts.

## Blueprints are domain-centric
You probably already saw building blueprints. Drawings used to build a building. They are categorised per-domain. Architecture, structure, mechanic, electricity and so on. This allows drawing to be readable and ease the process of searching. 

Some parts of the drawings can also exists without needing a dependency on other parts. 

Very often, the HVAC Control system will be presented schematically. You can see typical schema presenting 1 VAV box that will be repeated x times. You will get a vague notion of the physical spaces (rooms) but it is not required to have all the details of the room to understand how it works.

## Modeling can also be domain-centric
It will be common to see models built by different teams as finding one person knowing everything about all domains for a building will be hard to find. We can imagine that an HVAC contractor will build its part of the model. Lighting expert will do the lighting part. Intrusion/Access/Security team will build their part, and so on.

The architect also will build its part (physical space).

Each of those teams should be able to build a working model out of their knowledge and work. They should not depend on the work of others and the ontology of s223 should be used to link all those aspects of the model together to build a complete model when everyone is done.

This doesn't mean that they will not work all together and won't share information. It just means that without an heavy dependency on other teams work, the modeling task is easier to do.

# Physical-Truth approach
Physical-truth approach is the actual concurrent to the domain-centric approach. It was recently also named cross-domain, so I will use both terms in the article.

In this approach, as soon as entities refering to a room needs to be connected, they must be connected to the physical space. The physical space is then filled with all sort of connection points, with different medium to assure the relationships with entities.

To keep track of the domain in which the entities are, `servesDomainSpace` must be used.

This approach creates a change of layer for any entity related to a room by mixing multiple domain connection points on the same entity. This is why we can also call this method "cross-domain".

> A Equipment-like entity
>
> Physical Spaces in this approach are very similar to Equipment. In fact, an entity, connectable, with connection points in different domains it is in s223 everywhere else known as a Equipment.

## What's wrong if all is connected to the physical space ?
First, this means that a physical space is mandatory, always required. So in the process of creating a complete model, this dependency will eventually create the needs for all teams to build their own physical spaces, so they can work. Which means that at a certain point in time, there will be a need for a merge of all those different point of view on physical spaces coming from different models.

There will be times where not everything will be completed by all the teams and things may change. There is no reason for an HVAC team to wait for the model coming from the architect team to build a HVAC model for 1 AHU and 20 VAV Boxes for 20 offices. 

There are also situations where the physical spaces doesn't mean so much. I may not need a room number or height to model air flow in a simple system. 

I may also just be starting to model a very complicated building. I may not have to consider doors, windows in my model. With a physical-space centric approach, I'm unable to proceed without creating the physical layer.

Sure, you could start with a very simple or approximate physical spaces model, but as you are not the domain-expert, chances are that your model will be wrong.

# Advantages of domain-centric approach
## Interoperability of model sections
As I explained previously, models could be built by different teams. Once everyone will have built their part of the model, there is nothing to modify in the said model of each teams. Physical spaces will be defined to "enclose" domain spaces based on the architecture of the building. But that's pretty it.

Inside a room, multiple domain spaces can cohabit and overlap. This is not an issue. 

All sensors are treated the same way, installed in a room or not. 

All domains work the same way so you don't need to be an domain-expert to browse other models.

## Scalability
Adding new domain-centric parts to a model is easy. The entities added are not typically overlapping with other models.

The only thing required is (if required) to enclose new domain spaces in existing physical spaces. 

> Which is not the case for cross-domain models where the new models will need to modify the physical spaces of the existing model to add more connection points (at the very least). This is a serious flaw that can lead to conflicts and all sort of errors.

## Maintenance, localisation and interoperability (again)
When physical spaces are created, it becomes possible for teams (or the maintenance team eventually) to use the `hasPhysicalLocation` to relate things to the physical space and answer the questions like : _"Where is the discharge air temperature sensor located ?"_.

The domain-centric approach allows to locate Equipment and sensors easily using this predicate when this information is available. 

It's also important to note that this information (`hasPhysicalLocation`) will be added in the domain-centric parts of the model, which means that once people are aware of physical spaces in the model, they can modify their part of the model to add this information without touching everyone else part. This also allow simultaneous workj from different teams.

> The cross-domain approach also uses `hasPhysicalLocation` but not for sensors installed in rooms where `hasObservationLocation` must be used to find them.

# Going back to definitions
It is essential to be in phase with the meaning of the terms we use.

## Connection and Medium
There should only be 1 medium per connection and connection points.

## Physical Space is not "physical truth"
A Physical space is not more "physical truth" than any other domain... it is just another aspect or "domain" of the physical truth (reality?), related to physical aspects (height, weight, width, position, etc). 

At some extent, this could be called architectural domain space. A field of interest consisting of everything covered by architecture.

Physical truth, reality, can only be defined by the addition of all the layers (domains) modeled and all the other ones that are not (which are probably infinite).

A connection in HVAC domain is not a duct... a segment, a junction, a connection point... nothing of that is real.
Even a `s223:Coil` is not a "physical coil" as-in "physical truth". It's a model of a physical coil limited to the properties defined. 

For example, I could model a water coil without any water connection points. Just because I'm only interested in the "air" domain. I am then modeling only one aspect of this coil. It has no size, no shape, no color, no physical location, no water connections points... Physical truth really means nothing here. It's just fields of interest.

> Similar to any mathematical equation that would describe our reality. The variables are not bound to any "physical truth". They are just there to model one aspect of reality. A shortcut that help understand reality, not embrace every aspects of it... And there is a place for different models
>
>...think Newton gravity laws vs Relativity, there is no physical truth there, just numbers and symbols. And both allow us to model our reality on different aspects.

# Origins
When we first defined DomainSpaces, we were trying to create a thing, an entity, that would represent a field of interest inside a room (a space). This field of interest is sometimes as big as the room itself, but often not. 

> **Example**
>
>I would refer to the Big Garage example for which I presented a model recently. 
> A big garage with 4 walls, but with two distinct lighting spaces. One near the entry, the other one in the back. Domain spaces allow to split physical spaces in different zone of interest, without having to subdivise the physical spaces with smaller physical spaces that would have no wall, no boundaries.

## What are physical spaces
Physical spaces came soon after the creation of domain spaces as a way to "enclose" domain spaces. This is a special relationship when we think about it. But it was required by the physical nature of the physical space, which is to provide boundaries to the spaces and explicitly tell that spaces HVAC, Lighting, Access Control are inside the same room. With physical spaces it was then possible to model room, buildings, floors, patio, roof, etc.

The "encloses" relationship is perfeclty meant to describe the fact that some "zones of interest", domain spaces, are inside a room.

It is good to notice that physical spaces can contain other physical spaces but a domain space cannot overlap two adjacent physical spaces. In other words, a domain space is no bigger than the smallest physical space that encloses it.

## Finding entities
`hasPhysicalLocation` is a perfect fit for any Equipment, sensors, system, when required, to be able to specify the location inside a building for those entities. When provided, it provides a direct relationshiip to query to find the location of something in a building.

> **Cross-domain approach**
> 
> One collateral effect of the cross-domain approach is the need to treat room sensors differently than other sensors. Remember, using cross-domain, the room temperature sensor is connected to the physical space, the light occupancy sensor too. To find the domain where the measure is taken and stay on the same layer of interest, we need to use `servesDomainSpace` predicate. But the return air temperature is still using `hasObservationLocation` on a connection point which is not findable by the physical space. This means that different set of queries will be needed to find sensors in one system. 


## Sensors
Sensors are subclasses of Equipment but are special in the way that the medium will not typically pass through them. They are used to make a measurement at a certain point in the flow of the medium.

Knowing where this measurement takes places is important. This is why typical sensors are connected to connection points or connections.

> Connection points and connections are defined by their medium, what is inside this duct, pipe, wire, etc. As sensors makes measurement of a property inside a medium, this relationship makes perfect sense.

## Sensors in rooms
In a domain-centric approach, when a sensor measures a property of space, `hasObservationLocation` is connected to the domain space. The domain space connection points are defined by compatible medium (ex. HVAC domain space uses medium Air). In this case, the temperature sensor measures the temperature of the air inside this space. 

> **Compatible Medium**
>
> In the domain-centric approach, adding an `electricalInletConnectionPoint` to a HVAC Domain space would be an error as `Medium-Electricity` connections should be part of the `Electricity` domain. This is what compatible medium means. Rules shall be defined in the standard to define what medium are compatible with domains.

### Using cross-domain approach
In cross-domain, you connect the sensor to the physical space. But in the case where the physical space is so big, (think of a really long corridor in a mall) this connection brings nothing more than confusion. You can use `servesDomainSpace` but do you see the detour it creates ? We go from the HVAC domain, to the physical domain, just to return to the HVAC domain to find the information we need. 

### Uniformity of sensors and queries
In the domain-centric approach, room sensors are no different than any other sensors. They are all connected to connection or connections points residing in the same domain.

For any sensors in the model, 

- You need to know where a measurement is taken : `hasObservationLocation`
- You need to know where a sensor is physically : `hasPhysicalLocation` <- a clear jump to another domain

> It can also be noted that even if `hasPhysicalLocation` is not defined for a room sensor in the domain-centric approach, it is possible to find the physical space by finding the HVAC domain space and find which physical space encloses this domain space. A trivial task.

# Physical Space Connections and connection points
As seen earlier, connections and connection points are a way to model the fact that a certain medium is flowing through something. 

**What medium could be compatible with a physical space domain ?**

## The door example
Before answering the question on physical spaces medium, I think we could start by modeling a door. We can imagine a door in the physical space as an important part of connections between physical spaces. Looks to me like a good starting point.

So here we are. Imagine a door and make that a Equipment. A door modeled as a Equipment makes sense. We can imagine the thing, it can be controlled, open or close automatically or manually, monitored and can affect its environment. It works.

All aspects of the door can clearly be defined by the domain-centric approach by layering the different concepts and making a clear boundary between them.  

### Airflow
If studying the airflow (domain of interest), this door can be used by the HVAC domain so we could add a airConnectionPoint to it. This connection point should be bidirectional as air can flow from both sides, depending on pressures. This connection point could be used to make a specific relationship to tha HVAC spaces of interest. So for now, if someone is interested by the impact of a door on airflow, starting from the HVAC Domain will allow to quickly find the door.

### Access control and security
We can monitor this door in the access control domain. Let's add an `intrusionDetectionOutletConnectionPoint` to the Equipment, which can be connected to the access control and security domain space. This way we'll know if someone tries to force the door open. 

### Light
Light can pass through this door, we can add a `LightConnectionPoint` and depending on the situation as understood by the domain expert, this can be unidirectional, bidirectional, etc... and connected to the light domain space. No need to go further with the physic details of light propagation, it's supposed to be a simple example.

## People
What would be the field of interest specifically in the physical domain ? People using that door ? That may be useful. So there could be a bidirectional connection points between two physical spaces defined by a medium `People` (maybe, or `Air` and see people as big particulates inside air... it'S undefined for now ?) and it would allow the possibility of finding the shortest path to an emergency exit for example, or a shortcut to the coffee machine.

## What are the connections and connection point in regard to physical spaces ?

In the domain-centric approach, connection points added to domain spaces must be compatible with the domain of interest. By demonstrating the door example, I wanted to show that all aspects of the door is related to the different fields of interest. Airflow, access control, each of those aspect is covered by a domain space **if required**. And this is a major point. Spaces are used to model fields of interest. If there is no interest, there is no obligation to model those aspects. 

But when you are connecting physical spaces together, you are modeling some kind of undefined medium (for now) in which people and other entities travel from one physical space to another.

Because that is the field of interest.

> Note 
>
>In the domain-centric approach we do not allow connections to be made outside of the field of interest. Keeping this boundary clear, we don't need the supplemental predicate `servesDomainSpace` to fix the broken path created by using the cross-domain approach.

# Sharing information between domain spaces
This is an important point and real buildings are actually doing this, sharing information from one domain to another domain. And it's always made using some kind of **controller**. An HVAC system that can use the light occupancy sensor to adjust the temperature setpoint for example. **This is not done at the Equipment layer.** It is the result of an algorithm, a function block and in the context of s223, this abstraction is well served by the use of a `System`.

In a domain-centric approach, sharing information across domains requires the abstraction provided by Systems.

> `s223:System`
>
> By definition, Equipment can belongs to multiple systems at the same time. Systems are very flexible and can overlap other systems. This is a very powerful feature.

## If everything was in the physical space ?
In the cross-domain approach, entities inside rooms are connected to the physical space. But putting everything in the same jar isn't sufficient to demonstrate the interactions between entities. At some point, systems and function blocks will be required. Relationships will be required and this will not be easier to find them inside the physical space as you will have to make different queries to find information which are not in physical spaces.

Connecting entities to a physical spaces using cross-domain approach is the equivalent of treating the room as a Equipment. It is not a way to learn more things about the relationship of connections. It doens't make requests easier. It is not a replacement for systems and or function blocks.

# Sharing information with other data-driven services
BIM, maintenance softwares, haystack, brick, they will all work in a domain-centric way. By keeping our side organized with strong boundaries between domain spaces, it will be easier to build gateways between s223 world an others.

> I call gateway an entity that would serves alignment between s223 and another external system.

## Gateways
Physical spaces could be bound to BIM or other maintenance systems.
As an example, a `s223:System` could be used to align the physical spaces ontology to BIM ontology. By not including all connection points from other domains, we make it simple and maintainable. The same applies for all other domains that could be aligned to other ontologies.

For haystack, there could be a query over the model that would create a system to align the different pieces required by presenting tag equivalents. 

Energy modeling will also benefit from domain-centric approach as all connection points for specific medium will be available directly in the space of interest. ex. This could allow to estimate the impact of a radiant heater and a Windows on a specific part of a physical space (namely a HVAC domain space) by using direct relationship. 

# Conclusion
Domain-specific approach eliminates the need for different predicates to build queries on sensor depending on their location.

This approach allows teams to work on their part of the model without having strong dependencies between each other work.

Domain-specific approach is close to the reality of buildings and the nature of work done in them (domain-expert driven).

For those reasons and all the other presented here I'm convinced that the domain-centric approach is superior and easier to implement than the cross-domain approach. I already built different models and the flexibility of this approach has been proven each times. 
