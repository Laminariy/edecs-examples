from edecs import System


class InventorySystem(System):

    def inventory_exists(self, inventory_id):
        if not self.entity_manager.entity_exists(inventory_id):
            self.generate_event('EntityDoesNotExistEvent', {'entity_id': inventory_id})
            return False

        if not self.component_manager.component_exists(self.comp_name, inventory_id):
            self.generate_event('EntityHasNo%sEvent' % self.comp_name, {'entity_id': inventory_id})
            return False

        return True

    def item_exists(self, item_id):
        if not self.entity_manager.entity_exists(item_id):
            self.generate_event('EntityDoesNotExistEvent', {'entity_id': item_id})
            return False

        if not self.component_manager.component_exists('ItemComponent', item_id):
            self.generate_event('EntityHasNoItemComponentEvent', {'entity_id': item_id})
            return False

        return True

    def add_item(inventory_id, item_id, count=1):
        if self.inventory_exists(inventory_id) and self.item_exists(item_id):
            inventory = self.component_manager.component_types[self.comp_name][inventory_id]
            item = self.component_manager.component_types['ItemComponent'][item_id]

            if item.stackable:
                stack_size = item.stack_size

                for i, inv_item in enumerate(inventory.items): # item with free space in stack
                    if inv_item[0] == item_id and inv_item[1] < stack_size:
                        item_count = inventory.items[inventory_item][1]
                        new_item_count = min(item_count + count, stack_size)

                        inventory.items[inventory_item] = (item_id, new_item_count)
                        self.generate_event('AddItemSucsessEvent',
                                            {'inventory_id':inventory_id,
                                            'item_id':item_id,
                                            'count':count})
                        count -= new_item_count - item_count
                        break

                for _ in range(count // stack_size): # add stacks
                    if inventory.free_volume > 0:
                        inventory.items.append((item_id, stack_size))
                        count -= stack_size
                        self.generate_event('AddItemSucsessEvent',
                                            {'inventory_id':inventory_id,
                                            'item_id':item_id,
                                            'count':count})

                    else:
                        self.generate_event('InventoryHasNoFreeSpaceEvent',
                                            {'inventory_id':inventory_id,
                                            'item_id':item_id,
                                            'count':count})
                        return

                if count > 0:
                    if inventory.free_volume > 0:
                        inventory.items.append((item_id, count))
                        self.generate_event('AddItemSucsessEvent',
                                            {'inventory_id':inventory_id,
                                            'item_id':item_id,
                                            'count':count})

                    else:
                        self.generate_event('InventoryHasNoFreeSpaceEvent',
                                            {'inventory_id':inventory_id,
                                            'item_id':item_id,
                                            'count':count})

            else: # item isn't stackable
                for _ in range(count):
                    if inventory.free_volume > 0:
                        inventory.items.append((item_id, 1))
                        self.generate_event('AddItemSucsessEvent',
                                            {'inventory_id':inventory_id,
                                            'item_id':item_id,
                                            'count':count})

                    else:
                        self.generate_event('InventoryHasNoFreeSpaceEvent',
                                            {'inventory_id':inventory_id,
                                            'item_id':item_id,
                                            'count':count})
                        break

    def remove_item(inventory_id, item_id, count=1):
        if self.inventory_exists(inventory_id) and self.item_exists(item_id):
            inventory = self.component_manager.component_types[self.comp_name][inventory_id]
            removed_items = [] # [inv_id1, inv_id2]

            for i, item in enumerate(inventory.items):
                if count == 0:
                    break

                if item[0] == item_id:
                    if count >= item[1]:
                        removed_items.append(i)
                        count -= item[1]

                    else: # count < item[1]
                        inventory.items[i] = (item_id, item[1] - count)
                        count = 0

            if count == 0:
                for item in removed_items:
                    inventory.items.pop(item)

                self.generate_event('RemoveItemSucsessEvent',
                                    {'inventory_id':inventory_id,
                                    'item_id':item_id,
                                    'count':count})

            else:
                self.generate_event('InventoryHasNoItemsEvent',
                                    {'inventory_id':inventory_id,
                                    'item_id':item_id,
                                    'count':count})

    def on_add_item_event(self, event):
        inventory_id, item_id, count = event.data

        self.add_item(inventory_id, item_id, count)

    def on_remove_item_event(self, event):
        inventory_id, item_id, count = event.data

        self.remove_item(inventory_id, item_id, count)

    def init(self):
        self.comp_name = self.type.replace('System', 'Component')

        self.subscribe(self.on_add_item_event, 'AddItemToInventoryEvent')
        self.subscribe(self.on_remove_item_event, 'RemoveItemFromInventoryEvent')
