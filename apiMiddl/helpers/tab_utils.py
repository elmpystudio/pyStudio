import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from utils.TableauWrapper import TableauWrapper

def tab_utils():
    t = TableauWrapper()
    cmd = sys.argv[1]

    if cmd == "tab_list_users":
        users = t.get_users()
        for user in users:
            print("%s Role: %s" % (user.name, user.site_role))

    if cmd == "tab_delete_test_users":

        users = t.get_users()
        for user in users:
            if user.name.startswith("t3st"):
                print("Deleting user: %s" % user.name)
                t.delete_user(user.name)

    if cmd == "tab_list_projects":
        for p in t.get_projects():
            print(p.name)

    if cmd == "tab_list_datasources":
        print(t.get_datasources()[0][0].name)
        return
        for d in t.get_datasources()[0]:
            print(d[0])

    if cmd == "tab_list_workbooks":
        for d in t.get_workbooks()[0]:
            print("%s: %s" % (d.name, d.id))

    if cmd == "test":
        t.test()


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rest.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc


if __name__ == '__main__':
    main()
    tab_utils()
