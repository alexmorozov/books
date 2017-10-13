from kupola.fabric_class import DjangoFabric,\
    add_class_methods_as_functions


class Fabric(DjangoFabric):
    host = 'vm4'
    remote_base_path = '/home/inductor/.virtualenvs/'
    remote_project_path = '/home/inductor/.virtualenvs/books/'
    user = 'inductor'
    app_name = 'career_books'
    repository = 'git@github.com:alexmorozov/books.git'
    remote_db_name = 'books'
    local_db_name = 'books'
    use_bower = False


__all__ = add_class_methods_as_functions(Fabric(), __name__)
