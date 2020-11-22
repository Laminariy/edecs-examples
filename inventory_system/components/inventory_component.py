from edecs import Component


class InventoryComponent(Component):

    defaults = {
        'max_volume': 10,
        'items': [] # [(item_id, count)]
    }

    @property
    def free_volume(self):
        return self.max_volume - len(self.items)

    def item_in_inventory(self, item_id, count=1):
        for item in self.items:
            if item[0] == item_id and item[1] >= count:
                return True

        return False
