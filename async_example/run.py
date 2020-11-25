import sys
sys.path.append('..')
from edecs import Engine, System, Entity
from movement_system import (LocationComponent, PositionComponent, MovementSystem)


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
        pass

    def init(self):
        self.subscribe(self.log, 'AddEntityToLocationEvent')
        self.subscribe(self.log, 'RemoveEntityFromLocationEvent')
        self.subscribe(self.log, 'MoveEntityEvent')

        self.subscribe(self.log, 'EntityDoesNotExistEvent')
        self.subscribe(self.log, 'EntityHasNoPositionComponentEvent')
        self.subscribe(self.log, 'EntityHasNoLocationComponentEvent')
        self.subscribe(self.log, 'EntityAlreadyInLocationEvent')
        self.subscribe(self.log, 'EntityNotInLocationEvent')
        self.subscribe(self.log, 'LocationAddEntitySucsessEvent')
        self.subscribe(self.log, 'LocationRemoveEntitySucsessEvent')
        self.subscribe(self.log, 'MoveEntitySucsessEvent')
        self.subscribe(self.log, 'LocationHasNoConnectionEvent')

    async def update(self, dt):
        print('LogSystem')

class CreateSystem(System):

    def init(self):

        hero = Hero('Brave Knight') # id 0
        tavern = Location('Tavern') # id 1
        outside = Location('Outside') # id 2
        space = Location('Space') # id 3

        self.hero = hero

        tavern.location.connections.append(2)
        outside.location.connections.append(1)

        self.create_entity(hero)
        self.create_entity(tavern)
        self.create_entity(outside)
        self.create_entity(space)

    def update(self, dt):
        print('CreateSystem')
        print(self.hero.position)


def main():
    engine = Engine()

    engine.create_system(LogSystem())
    engine.create_system(MovementSystem())
    engine.create_system(CreateSystem())

    engine.generate_input('AddEntityToLocationEvent', {'entity_id': 0, 'location_id': 1})

    engine.generate_input('RemoveEntityFromLocationEvent', {'entity_id': 0, 'location_id': 1})

    engine.generate_input('AddEntityToLocationEvent', {'entity_id': 0, 'location_id': 1})
    engine.generate_input('MoveEntityEvent', {'entity_id': 0, 'location_id': 2})

    engine.generate_input('MoveEntityEvent', {'entity_id': 0, 'location_id': 2})
    engine.generate_input('MoveEntityEvent', {'entity_id': 0, 'location_id': 1})
    engine.generate_input('MoveEntityEvent', {'entity_id': 0, 'location_id': 3})

    engine.a_run()


if __name__ == '__main__':
    main()
