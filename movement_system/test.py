from edecs import (Entity, System, Engine)
from components import (LocationComponent, PositionComponent)
from systems import MovementSystem


class Hero(Entity):
    default_components = {
        'position': PositionComponent()
    }

class Location(Entity):
    default_components = {
        'location': LocationComponent()
    }

class LogSystem(System):

    def log(self, event):
        print(event)

    def init(self):
        self.subscribe(self.log, 'EntityDoesNotExistEvent')
        self.subscribe(self.log, 'EntityHasNoPositionComponentEvent')
        self.subscribe(self.log, 'EntityHasNoLocationComponentEvent')
        self.subscribe(self.log, 'EntityAlreadyInLocationEvent')
        self.subscribe(self.log, 'EntityNotInLocationEvent')
        self.subscribe(self.log, 'LocationAddEntitySucsessEvent')
        self.subscribe(self.log, 'LocationRemoveEntitySucsessEvent')
        self.subscribe(self.log, 'MoveEntitySucsessEvent')
        self.subscribe(self.log, 'LocationHasNoConnectionEvent')
        self.subscribe(self.log, 'TeleportEntitySucsessEvent')

class CreateSystem(System):

    def init(self):
        hero = Hero('Brave Knight') # id 0
        tavern = Location('Tavern') # id 1
        outside = Location('Outside') # id 2
        space = Location('Space') # id 3

        tavern.location.connections.append(2)
        outside.location.connections.append(1)

        self.create_entity(hero)
        self.create_entity(tavern)
        self.create_entity(outside)
        self.create_entity(space)


def main():
    engine = Engine()

    engine.create_system(LogSystem())
    engine.create_system(MovementSystem())
    engine.create_system(CreateSystem())

    hero = engine.entity_manager.entities[0]

    engine.generate_input('AddEntityToLocationEvent', {'entity_id': 0, 'location_id': 1})

    engine.update()
    print(hero.position)

    engine.generate_input('RemoveEntityFromLocationEvent', {'entity_id': 0, 'location_id': 1})

    engine.update()
    print(hero.position)

    engine.generate_input('AddEntityToLocationEvent', {'entity_id': 0, 'location_id': 1})
    engine.generate_input('MoveEntityEvent', {'entity_id': 0, 'location_id': 2})

    engine.update()
    print(hero.position)

    engine.generate_input('MoveEntityEvent', {'entity_id': 0, 'location_id': 2})
    engine.generate_input('MoveEntityEvent', {'entity_id': 0, 'location_id': 1})
    engine.generate_input('MoveEntityEvent', {'entity_id': 0, 'location_id': 3})

    engine.update()
    print(hero.position)

    engine.generate_input('TeleportEntityEvent', {'entity_id': 0, 'location_id': 3})

    engine.update()
    print(hero.position)


if __name__ == '__main__':
    main()
