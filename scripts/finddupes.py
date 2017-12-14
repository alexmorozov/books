#--coding: utf8--


from li.models import Person
from li.utils import canonicalize

from survey.models import Result


def find_empty_forms(contacts):
    incomplete = filter(
        lambda c: bool(Result.objects
                       .filter(person=c)
                       .incomplete()
                       .exists()),
        contacts)
    return sorted(incomplete, key=lambda x: -x.pk)


def contact_info(contact):
    return u'{c.pk} {c.name} {c.profile_url}'.format(c=contact)


if __name__ == '__main__':
    dupes = {}
    for person in Person.objects.all():
        url = canonicalize(person.profile_url)
        dupes.setdefault(url, []).append(person)

    for url, contacts in dupes.items():
        if len(contacts) > 1:
            #incomplete = find_empty_forms(contacts)
            #if incomplete:
                #print incomplete[0].pk
            #print u'\n'.join([contact_info(contact)
                              #for contact in contacts])
            #print '\n'
            print contacts[-1].pk
