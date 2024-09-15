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
    def __init__(self, name, time_left):
        self.name = name
        self.is_ready = False
        self.is_done = False
        self.reqs = []
        self.time_left = time_left

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

def parse_steps(data, part_two=False):
    step_objects = {}
    step_regex = 'Step ([A-Z]+) must be finished before step ([A-Z]+) can begin.'
    steps = [re.match(step_regex, step).groups() for step in data.split('\n')]
    for first, second in steps:
        if part_two:
            time_left_first = get_time(first)
            time_left_second = get_time(second)
        else:
            time_left_first = 0
            time_left_second = 0
        step_objects[first] = step_objects.get(first, Step(first, time_left=time_left_first))
        step_objects[second] = step_objects.get(second, Step(second, time_left=time_left_second))
        step_objects[second].add_req(step_objects[first])
    return step_objects

def get_order_part_one(step_objects):
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

def get_order_part_two(step_objects, num_workers):
    order = ''
    done = False
    worker_assignments = [None for i in range(num_workers)]
    total_time = 0
    while not done:
        q = []

        in_progress = [w for w in worker_assignments if w is not None]
        for current_name in in_progress:
            current_step = step_objects[current_name]
            current_step.time_left -= 1
            if current_step.time_left == 0:
                current_step.is_done = True
                worker_idx_to_clear = worker_assignments.index(current_name)
                worker_assignments[worker_idx_to_clear] = None
                order += current_name
            step_objects[current_name] = current_step

        for name, step in step_objects.items():
            if step.get_is_ready() and not step.is_done and name not in worker_assignments:
                q.append(name)
        q = sorted(q)
        #None to be worked and none in progress
        if len(q) == 0 and len([w for w in worker_assignments if w is not None]) == 0:
            done = True
        else:
            unassigned = [i for i, w in enumerate(worker_assignments) if w is None]
            if len(unassigned) > 0 and len(q) > 0:
                for i, cn in enumerate(q):
                    try:
                        worker_index = unassigned.pop(0)
                    except IndexError:
                        break
                    worker_assignments[worker_index] = cn
            total_time += 1
    return order, total_time

def part_one(data):
    step_objects = parse_steps(data)
    part_one_answer = get_order_part_one(step_objects)
    return part_one_answer

def get_time(step_name):
    return ord(step_name)-4

def part_two(data, num_workers):
    step_objects = parse_steps(data, part_two = True)
    order,total_time = get_order_part_two(step_objects, num_workers)
    return order,total_time

#Part one correct
part_one_example_answer = part_one(example_data)
part_one_answer = part_one(data)

part_two_example_order, part_two_example_answer = part_two(example_data, 2)
part_two_order, part_two_answer = part_two(data, 5)