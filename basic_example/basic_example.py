from random import random
from edecs import (Entity, Component, System, Engine)


class HealthComponent(Component):
    # стандартные значения данных компонента:
    defaults = {
        'max_hp': 10,
        'hp': 10
    }

class AttackComponent(Component):
    defaults = {
        'damage': 1,
        'crit_damage': 3,
        'crit_chance': 0.3,
        'target': -1 # id цели, которую существо атакует
    }

    # функция рассчета урона
    def get_damage(self):
        if random() <= self.crit_chance:
            return self.crit_damage

        return self.damage


class Skeleton(Entity):
    # стандартные компоненты сущности:
    default_components = {
        'health': HealthComponent(max_hp=5, hp=5),
        'attack': AttackComponent()
    }

class Hero(Entity):
    default_components = {
        'health': HealthComponent(max_hp=20, hp=20),
        'attack': AttackComponent(damage=3, crit_damage=5, crit_chance=0.45)
    }


class CombatSystem(System):
    # init() вызывается при создании системы
    def init(self):
        # создаем объекты сущностей
        hero = Hero('Brave Knight')
        skeleton = Skeleton('Archer Skeleton')

        # добавляем их в "мир"
        self.create_entity(hero)
        self.create_entity(skeleton)

        # "натравливаем" друг на друга - добавляем айди в компонент атаки
        hero.attack.target = skeleton.id
        skeleton.attack.target = hero.id

        # подписываем функцию на событие смерти
        self.subscribe(self.on_death, 'DeathEvent')

    # событие о смерти персонажа
    def on_death(self, event):
        id = event.id

        # удаляем мертвую сущность
        death_entity = self.entity_manager.entities[id]
        self.destroy_entity(death_entity)

    # update() вызывается каждый проход игрового цикла
    def update(self, dt):
        # находим все компоненты атаки и здоровья
        attack_components = self.component_manager.component_types['AttackComponent']
        health_components = self.component_manager.component_types['HealthComponent']

        # пробегаем все компоненты атаки
        for id, atk in attack_components.items():
            target_id = atk.target

            if target_id == -1:
                break # если существо никого не атакует - ничего не делаем, выходим из цикла

            # рассчитываем урон и вычитаем здоровье
            damage = atk.get_damage()
            health_components[target_id].hp -= damage

            # отправляем событие, что один персонаж атаковал другого
            self.generate_event('AttackEvent', {'attacker_id':id, 'target_id':target_id, 'damage':damage})

            # если цель умерла после атаки
            if health_components[target_id].hp <= 0:
                # отправляем событие о смерти персонажа
                name = self.entity_manager.entities[target_id].name
                self.generate_event('DeathEvent', {'id':target_id,'name':name})

                # убираем цель атакующему
                atk.target = -1

                # так как умершее существо еще не удалено системой, уберем и у него цель тоже
                attack_components[target_id].target = -1

class LogSystem(System):
    # log() вызовется когда случится событие, на которое подписана эта функция
    def log(self, event):
        # если пришло событие об атаке, то выводим сообщение в консоль
        if event.type == 'AttackEvent':
            attacker_id = event.attacker_id
            target_id = event.target_id
            damage = event.damage

            attacker_name = self.entity_manager.entities[attacker_id].name
            target_name = self.entity_manager.entities[target_id].name

            print("%s наносит %s урона персонажу %s!" % (attacker_name, damage, target_name))

        # если кто-то умер
        elif event.type == 'DeathEvent':
            print("Персонаж %s умер!" % event.name)

    # здесь в init() мы подписываем функцию log() на события
    def init(self):
        self.subscribe(self.log, 'AttackEvent')
        self.subscribe(self.log, 'DeathEvent')


def main():
    # создаем объект движка
    engine = Engine()

    # создаем системы
    engine.create_system(CombatSystem())
    engine.create_system(LogSystem())

    # игровой цикл
    while True:
        engine.update()


if __name__ == '__main__':
    main()
