from __future__ import annotations

from aocd import get_data
import re

data = get_data(year=2018, day=7)
example_data = """Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin."""

class Step:
    def __init__(self, name):
        self.name = name
        self.is_ready = False
        self.is_done = False
        self.reqs = []

    def add_req(self, step: Step):
        self.reqs.append(step)

    def set_is_ready(self):
        if len(self.reqs) == 0:
            self.is_ready = True
        else:
            self.is_ready = all([r.is_done for r in self.reqs])
        return self.is_ready

    def get_is_ready(self):
        self.set_is_ready()
        return self.is_ready

def parse_steps(data):
    step_objects = {}
    step_regex = 'Step ([A-Z]+) must be finished before step ([A-Z]+) can begin.'
    steps = [re.match(step_regex, step).groups() for step in data.split('\n')]
    for first, second in steps:
        step_objects[first] = step_objects.get(first, Step(first))
        step_objects[second] = step_objects.get(second, Step(second))
        step_objects[second].add_req(step_objects[first])
    return step_objects

def get_order(step_objects):
    order = ''
    done = False
    while not done:
        q = []
        for name, step in step_objects.items():
            if step.get_is_ready() and not step.is_done:
                q.append(name)
        q = sorted(q)
        if len(q) == 0:
            done = True
        else:
            current_name = q[0]
            order += current_name
            current_step = step_objects[current_name]
            current_step.is_done = True
            step_objects[current_name] = current_step
    return order

def part_one(data):
    step_objects = parse_steps(data)
    part_one_answer = get_order(step_objects)
    return part_one_answer

#Part one correct
part_one_example_answer = part_one(example_data)
part_one_answer = part_one(data)