# coding=utf-8

class System(object):
    def __init__(self, world, component_labels):
        self.world = world
        self.component_labels = component_labels

    # component_tuples: [(eid, component_tuple)]
    def update(self, dt, component_tuples):
        pass
