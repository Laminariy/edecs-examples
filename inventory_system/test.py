from edecs import (Entity, System, Engine)
from components import (ItemComponent, InventoryComponent)
from systems import (InventorySystem)


class CreateSystem(System):
    def init(self):
        hero = Entity(entity_type='Hero', name='Brave Knight')
        hero.inventory = InventoryComponent()

        sword = Entity(entity_type='Sword', name='FireSword')
        sword.item = ItemComponent(stack_size=1)

        health_potion = Entity(entity_type='HealthPotion', name='Health Potion')
        health_potion.item = ItemComponent(stack_size=10)

        self.create_entity(hero) # hero id = 0
        self.create_entity(sword) # sword id = 1
        self.create_entity(health_potion) # health potion id = 2

class LogSystem(System):
    def log(self, event):
        print(event)

        inventory = self.component_manager.component_types['InventoryComponent'][event.inventory_id]
        print(inventory.items)

    def init(self):
        self.subscribe(self.log, 'EntityDoesNotExistEvent')
        self.subscribe(self.log, 'EntityHasNoInventoryComponentEvent')
        self.subscribe(self.log, 'EntityHasNoItemComponentEvent')
        self.subscribe(self.log, 'AddItemSucsessEvent')
        self.subscribe(self.log, 'InventoryHasNoFreeSpaceEvent')
        self.subscribe(self.log, 'RemoveItemSucsessEvent')
        self.subscribe(self.log, 'InventoryHasNoItemsEvent')


def main():
    engine = Engine()

    engine.create_system(CreateSystem())
    engine.create_system(LogSystem())
    engine.create_system(InventorySystem())

    engine.generate_input('AddItemToInventoryEvent', {'inventory_id':0, 'item_id':1, 'count':2})
    engine.generate_input('AddItemToInventoryEvent', {'inventory_id':0, 'item_id':2, 'count':15})

    engine.update()

    engine.generate_input('RemoveItemFromInventoryEvent', {'inventory_id':0, 'item_id':2, 'count':4})
    engine.generate_input('RemoveItemFromInventoryEvent', {'inventory_id':0, 'item_id':1, 'count':5})

    engine.update()

    engine.generate_input('RemoveItemFromInventoryEvent', {'inventory_id':0, 'item_id':2, 'count':11})
    engine.generate_input('RemoveItemFromInventoryEvent', {'inventory_id':0, 'item_id':1, 'count':1})

    engine.update()

    engine.generate_input('AddItemToInventoryEvent', {'inventory_id':0, 'item_id':2, 'count':15})
    engine.generate_input('AddItemToInventoryEvent', {'inventory_id':0, 'item_id':2, 'count':7})

    engine.update()

    engine.generate_input('RemoveItemFromInventoryEvent', {'inventory_id':0, 'item_id':2, 'count':10})

    engine.update()

    engine.generate_input('RemoveItemFromInventoryEvent', {'inventory_id':0, 'item_id':2, 'count':3})

    engine.update()

if __name__ == '__main__':
    main()
