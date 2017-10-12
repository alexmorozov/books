from kupola.fabric_class import DjangoFabric,\
    add_class_methods_as_functions


class Fabric(DjangoFabric):
    host = 'localhost'
    app_name = 'career_books'
    repository = 'git@repo.kupo.la:kupola/career_books.git'
    remote_db_name = 'career_books'
    local_db_name = 'books'
    use_bower = True


__all__ = add_class_methods_as_functions(Fabric(), __name__)
