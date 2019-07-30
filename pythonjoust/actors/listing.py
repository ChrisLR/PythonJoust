actors_by_name = {}


def register(actor_class):
    actors_by_name[actor_class.name] = actor_class

    return actor_class


def get(name):
    return actors_by_name.get(name)
