Система перемещения между локациями.

Компоненты:
  LocationComponent - компонент локации
    connections - (list) - список локаций, в которые можно переместиться из данной
    entities - (lsit) - список сущностей в данной локации

  PositionComponent - компонент позиции, вешается на сущность, которая может находиться в локациях
    position (int) - айди локации, в которой находится сущность. -1, если не находится ни в одной


Системы:
  MovementSystem - система перемещения
    Принимаемые события:


    Генерируемые события:
      EntityDoesNotExistEvent - сущность не существует
        entity_id - айди сущности

      EntityHasNoPositionComponentEvent - сущность не имеет компонента позиции
        entity_id - айди сущности

      EntityHasNoLocationComponentEvent - сущность не имеет компонента локации
        entity_id - айди сущности

      EntityAlreadyInLocationEvent - сущность уже находится в локации
        entity_id - айди сущности
        location_id - айди локации

      EntityNotInLocationEvent - сущности нет в локации (при попытке удаления)
        entity_id - айди сущности
        location_id - айди локации

      LocationAddEntitySucsessEvent - сущность была успешно добавлена в локацию
        entity_id - айди сущности
        location_id - айди локации

      LocationRemoveEntitySucsessEvent - сущность была успешно удалена из локации
        entity_id - айди сущности
        location_id - айди локации

      MoveEntitySucsessEvent - перемещение сущности между локациями успешно
        entity_id - айди сущности
        location_id - айди локации

      LocationHasNoConnectionEvent - перемещение не удалось, отсутствует путь из текущей локации в заданную
        loc_from_id - из какой локации нет пути
        loc_to_id - в какую локацию нет пути
