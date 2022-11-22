from utils.TableauWrapper import TableauWrapper

t = TableauWrapper()
users = t.get_users()
for user in users:
    if user.name.startswith("t3st"):
        print("Deleting user: %s" % user.name)
        t.delete_user(user.name)
