#--coding: utf8--


from survey.models import Book


def print_results(count):
    books = Book.objects.by_votes()[:count]
    for book in books:
        print '{b.title} by {b.author} {b.image}'.format(
            b=book)

if __name__ == '__main__':
    print_results(20)
