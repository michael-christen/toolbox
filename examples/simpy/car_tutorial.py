from __future__ import annotations
import dataclasses

import simpy
import time


def clock(env, name, tick):
    while True:
        print(name, env.now, tick)
        yield env.timeout(tick)


def clock_main():
    env = simpy.Environment()
    fast_proc = env.process(clock(env, 'fast', 0.5))
    slow_proc = env.process(clock(env, 'slow', 1))
    env.run(until=2)


def car(env):
    while True:
        print('Start parking at %d' % env.now)
        parking_duration = 5
        yield env.timeout(parking_duration)

        print('Start driving at %d' % env.now)
        trip_duration = 2
        yield env.timeout(trip_duration)


def car_main():
    env = simpy.Environment()
    env.process(car(env))
    env.run(until=15)


class Car(object):
    def __init__(self, env):
        self.env = env
        self.action = env.process(self.run())

    def run(self):
        while True:
            print('Start parking and charging at %d' % self.env.now)
            charge_duration = 5
            # We may get interrupted while charging the battery
            try:
                yield self.env.process(self.charge(charge_duration))
            except simpy.Interrupt:
                # When we received an interrupt, we stop charging and
                # switch to the "driving" state
                print('Was interrupted. Hope, the battery is full enough ...')

            print('Start driving at %d' % self.env.now)
            trip_duration = 2
            try:
                yield self.env.timeout(trip_duration)
            except simpy.Interrupt:
                print('trip was interrupted')

    def charge(self, duration):
        yield self.env.timeout(duration)


def driver(env, car):
    yield env.timeout(6)
    car.action.interrupt()


def car_class_main():
    env = simpy.Environment()
    car = Car(env)
    env.process(driver(env, car))
    env.run(until=15)

def car_with_breaks(env, name, bcs, driving_time, charge_duration):
    # Simulate driving to the BCS
    yield env.timeout(driving_time)

    # Request one of its charging spots
    print('%s arriving at %d' % (name, env.now))
    with bcs.request() as req:
        yield req

        # Charge the battery
        print('%s starting to charge at %s' % (name, env.now))
        yield env.timeout(charge_duration)
        print('%s leaving the bcs at %s' % (name, env.now))

def car_resource_main():

    env = simpy.Environment()
    bcs = simpy.Resource(env, capacity=2)
    for i in range(4):
        env.process(car_with_breaks(env, 'Car %d' % i, bcs, i*2, 5))
    env.run()

def car_example():
    # car_main()
    # car_class_main()
    car_resource_main()


if __name__ == '__main__':
    car_example()
