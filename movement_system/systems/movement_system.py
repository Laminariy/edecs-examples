from edecs import System


class MovementSystem(System):

    def position_exists(self, position_id):
        if not self.entity_manager.entity_exists(position_id):
            self.generate_event('EntityDoesNotExistEvent', {'entity_id': position_id})
            return False

        if not self.component_manager.component_exists('PositionComponent', position_id):
            self.generate_event('EntityHasNoPositionComponentEvent', {'entity_id': position_id})
            return False

        return True

    def location_exists(self, location_id):
        if not self.entity_manager.entity_exists(location_id):
            self.generate_event('EntityDoesNotExistEvent', {'entity_id': location_id})
            return False

        if not self.component_manager.component_exists('LocationComponent', location_id):
            self.generate_event('EntityHasNoLocationComponentEvent', {'entity_id': location_id})
            return False

        return True

    def add_entity_to_location(self, position_id, location_id):
        if self.position_exists(position_id) and self.location_exists(location_id):
            location = self.component_manager.component_types['LocationComponent'][location_id]
            position = self.component_manager.component_types['PositionComponent'][position_id]

            if position_id in location.entities:
                self.generate_event('EntityAlreadyInLocationEvent',
                                    {'entity_id':position_id,
                                    'location_id':location_id})
                return

            location.entities.append(position_id)
            position.position = location_id
            self.generate_event('LocationAddEntitySucsessEvent',
                                {'entity_id':position_id,
                                'location_id':location_id})

    def remove_entity_from_location(self, position_id, location_id):
        if self.position_exists(position_id) and self.location_exists(location_id):
            location = self.component_manager.component_types['LocationComponent'][location_id]
            position = self.component_manager.component_types['PositionComponent'][position_id]

            if position_id not in location.entities:
                self.generate_event('EntityNotInLocationEvent',
                                    {'entity_id':position_id,
                                    'location_id':location_id})
                return

            location.entities.remove(position_id)
            position.position = -1
            self.generate_event('LocationRemoveEntitySucsessEvent',
                                {'entity_id':position_id,
                                'location_id':location_id})

    def move_entity(self, position_id, location_id):
        if self.position_exists(position_id) and self.location_exists(location_id):
            location = self.component_manager.component_types['LocationComponent'][location_id]
            position = self.component_manager.component_types['PositionComponent'][position_id]

            if location_id in location.connections: # move
                self.remove_entity_from_location(position_id, position.position)
                self.add_entity_to_location(position_id, location_id)
                self.generate_event('MoveEntitySucsessEvent',
                                    {'entity_id':position_id,
                                    'location_id':location_id})

            else: # cannot move
                self.generate_event('LocationHasNoConnectionEvent',
                                    {'loc_from_id':position.position,
                                    'loc_to_id':location_id})
