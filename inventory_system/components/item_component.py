from edecs import Component


class ItemComponent(Component):

    defaults = {
        'stackable':True,
        'stack_size': 64
    }
