"""Show a thermostat controlling a system."""

from __future__ import annotations

import dataclasses
import time

import simpy

THERMOSTAT_PERIOD = 1


@dataclasses.dataclass
class ThermalObject:
    thermal_mass: float
    temperature_c: float
    current_thermal_power_in_w: float
    last_change_in_power_t: float

    def update_power(self, now_t: float, new_power_w: float) -> None:
        dt = now_t - self.last_change_in_power_t
        thermal_energy = dt * self.current_thermal_power_in_w
        temperature_change_c = thermal_energy / self.thermal_mass
        # TODO(XXX): As you get colder or hotter, it will be harder and harder
        # to actually apply this power into the system (eg, there are no
        # perfect transducers of energy into temperature)
        self.temperature_c += temperature_change_c
        self.current_thermal_power_in_w = new_power_w
        self.last_change_in_power_t = now_t

    def get_temperature_c(self, now_t: float) -> float:
        self.update_power(
            now_t=now_t, new_power_w=self.current_thermal_power_in_w
        )
        return self.temperature_c


@dataclasses.dataclass
class ThermalContainer:
    thermal_object: ThermalObject
    power_combiner: dict[str, float]

    def apply_power(self, now_t: float, name: str, power_w: float) -> None:
        self.power_combiner[name] = power_w
        total_power = sum(self.power_combiner.values())
        self.thermal_object.update_power(now_t=now_t, new_power_w=total_power)


def thermostat(
    env, setpoint_c: float, hysteresis_c: float, container: ThermalContainer
):
    while True:
        yield env.timeout(THERMOSTAT_PERIOD)
        temp_c = container.thermal_object.get_temperature_c(env.now)
        print(f"TEMPERATURE: {temp_c}")
        if temp_c >= (setpoint_c + hysteresis_c):
            hvac_power_w = -1.0
        elif temp_c <= (setpoint_c - hysteresis_c):
            hvac_power_w = +1.0
        else:
            hvac_power_w = 0.0
        container.apply_power(now_t=env.now, name="HVAC", power_w=hvac_power_w)


def temperature_transducer(env, name: str, container: ThermalContainer):
    power_w = 4
    container.apply_power(now_t=env.now, name=name, power_w=power_w)


def thermostat_main():
    """Model a thermostat with control of a sensor and a HVAC unit.

    There are other "actors" at play that can modify the temperature of the
    sensor in addition to the HVAC unit.

    The thermostat will work to get its sensor to the setpoint as desired.
    """
    SIM_DURATION = 30
    INITIAL_TIME = 0

    container = ThermalContainer(
        thermal_object=ThermalObject(
            thermal_mass=1,
            temperature_c=0,
            current_thermal_power_in_w=0,
            last_change_in_power_t=INITIAL_TIME,
        ),
        # Each transducer can affect the power combiner
        power_combiner={
            "bias": 0.5,
        },
    )

    env = simpy.Environment(initial_time=INITIAL_TIME)

    env.process(
        thermostat(env, setpoint_c=20, hysteresis_c=1.0, container=container)
    )

    env.run(until=SIM_DURATION)


def main():
    start = time.monotonic_ns()
    thermostat_main()
    end = time.monotonic_ns()
    duration_ns = end - start
    duration_us = duration_ns / 1e3
    print(f"Took: {duration_us:.3f}(us)")


if __name__ == "__main__":
    main()
