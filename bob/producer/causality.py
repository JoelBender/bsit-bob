from ..core import BOB
from ..producer import Producer, ProducerInput, ProducerOutput

_namespace = BOB


class Causality(Producer):
    """
    Simple causality black box. Its goal is to express a
    simple relation between the output and the input.
    It tells : this input, causes an effect on that output.
    """

    cause_input: ProducerInput
    effect_output: ProducerOutput


class Differential(Producer):
    """
    This causality block goals explain that the output is the result
    of substracting high input and low input.
    """

    high_input: ProducerInput
    low_input: ProducerInput
    differential_output: ProducerOutput


class HandOffAutoMotorStarter(Producer):
    """
    Typically used in Electrical Motor Starter, where a selector allow manual, off, or auto
    The contactor position is commanded on or off depending on standard input (manual or auto + automatic command signal)
    Fire input, protection input and overload are protection that will turn off the contactor, stopping the load.
    """

    manual_or_off_input: ProducerInput  # front selector
    auto_input: ProducerInput  # from external source (ie. controller)
    fire_input: ProducerInput  # fire contact allowing the command to work
    protection_input: ProducerInput  # like freeze protection
    overload_input: ProducerInput  # Overloads from the contactor will make the starte go Off if current went too high
    contactor_output: ProducerOutput


class VFDProducer(Producer):
    """
    Very simple implementation of a VFD Producer.
    This is not Function, only relating different input properties with output properties.
    Any input causes an effect on all output in some way.

    NOTE : This is not the role of the producer to define in details the effects.
    """

    manual_or_off_input: ProducerInput  # front selector
    auto_input: ProducerInput  # from external source (ie. controller)
    speed_ref_input: ProducerInput
    fire_input: ProducerInput  # fire contact allowing the command to work
    run_enable_input: ProducerInput  # like freeze protection
    frequency_output: ProducerOutput
    voltage_output: ProducerOutput
    current_output: ProducerOutput
    torque_output: ProducerOutput
    rpm_output: ProducerOutput
    drive_running: ProducerOutput
