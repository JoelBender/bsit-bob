# Concept
I wanted to see where this would lead me so I tried the following.

Modeling a very simple Electrical Entry for a building using 600V (575V) feeding a main panel.
One breaker of the main panel feeds a transformer (575V/120_240V)
This transformer feeds a distribution panel (120V_240V) with breakers

## DistributionPanel
Distribution panels are to be chosen between SinglePhase (120-240V) or ThreePhases (480, 575, etc)
A distribution panel is just a metal box with bus bars in it.

## Main breaker
Each panel needs a main breaker. I modeled this breaker in a special way (a little tweak) that I will explain later.

## Circuit Breaker
A circuit breaker has one electricalInlet and one electricalOutlet. Even for Three phase breakers as it is illegal to use phases separatly. So a 3-phases breakers will have 1 connection possible.

## Transformer
A simple Equipment with an electricalInlet and an electricalOutlet

# Bus bars
The concept of a bus bar is that when installing the breaker, the inlet of the breaker will touch 1, 2 or 3 bus bar (depending on the type of the breaker) at the same time. Then the output of the breaker will serves as connection points. To do that, bus bars in panels have been modeled as `Connections`. This way we limit the number of hops from the main breaker to the circuit breakers themselves.

## Main breakers are special
They are as instead of one inlet and one outlet, I modeled them with multiple outlet so they can be connected to the bus bars in the panel. I also added one more connection which is a connection that model the usage of multiple bus bar at the same time.

> **Using 2 or 3 bus bars**
>
> When using a breaker for 240V or 575V, this breaker will be connected to more than one bus bar. For the sake of modeling electrical distribution, I see no advantages for now to explode the model with multiple connection points and connection to connections points on the breakers by splitting 575V in 3 lines of 347V. A 575V breakers will simply use the Medium `Electricity_575V_60Hz` to connect to a load. Not 3 lines of 347 + 1 neutral and a ground. Those details are implicit.

# Medium
To model this, I used medium in the form of enumerations (all siblings so they can't be mixed)

* _In this list, all flavours include connection points, inlet and outlet, systems CP (inlet and outlet)_
- s223:Medium-Electricity (generic)
- s223:Electricity-575V_60Hz
- s223:Electricity-480V_60Hz
- s223:Electricity-347V_60Hz
- s223:Electricity-277V_60Hz
- s223:Electricity-208V_60Hz
- s223:Electricity-120V_240V_60Hz (typically this comes from the street for your house, here)
- s223:Electricity-240V_60Hz
- s223:Electricity-120V_60Hz

The list should grow to include 24VAC, 12VDC, etc... and eventually, EU 50Hz...

It's a good thing to not use properties to set frequency in those as this should never change.
For links between a VFD, I would still use the same medium than if a starter was used.

# Next step : Metering
Now that I have a basic electrical network in the Pritoni Building, I'll be able to add meters.

# Connections
The way s223 works with connections and connection points... when dealing with electrical loads, the more natural
way is to start with a connection from the right type of Electricity Medium.

I don't know if I could automatically create the connections when adding a breaker to a panel.


# Metering
Electricity Sensor need to be using Medium-Electricity
Medium-Electricity needs to be connectable to any subclasses.

But for now.... let's use exact MEdium
Trick is :

1 measure per sensor
and an electrical meter needs a lot of readings...
VoltAN, BN, CN, AB, BC, CA, CurrentA, B, C, Frequency

Should I connect all those things.... or just make 1 connection to CP with right Medium 
and add external reference to all the variables needed ?
