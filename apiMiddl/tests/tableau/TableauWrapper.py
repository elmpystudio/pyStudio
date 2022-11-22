import tableauserverclient as tab

class TableauWrapper:

    def __init__(self, url, user, password, site):
        self.site = site
        self.url = url
        self.user = user
        self.password = password
        self._connect()

    def _connect(self):
        self.auth = tab.TableauAuth(self.user,self.password,self.site)
        self.server = tab.Server(self.url)

    def create_user(self, new_user, new_password):
        with self.server.auth.sign_in(self.auth):
            new_user_object = tab.UserItem(new_user, "Publisher")
            new_user_object = self.server.users.add(new_user_object)
            self.server.users.update(new_user_object, password=new_password)

        return new_user_object

    def get_user_by_name(self, name):

        with self.server.auth.sign_in(self.auth):
            all_users, pagination_item = self.server.users.get()
            for user in all_users:
                if user.name == name:
                    print([user for user in all_users])
                    return user
        return None

if __name__ == "__main__":
    user = "api-user"
    password = "Aa123456"
    site = "Research"
    url = "http://35.208.41.132:8999"
    t = TableauWrapper(url, user, password, site)
    
    #t.create_user("user", "q1q1q1Q!")
    t.get_user_by_name("user")
