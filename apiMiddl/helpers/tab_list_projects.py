from utils.TableauWrapper import TableauWrapper
t = TableauWrapper()
for p in t.get_projects():
    print("%s:%s" % (p.name, p.id))
