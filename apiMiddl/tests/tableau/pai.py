import tableauserverclient as tab
from utils import *

user = "api-user"
password = "Aa123456"
site = "Research"

url = "http://35.208.41.132:8999"
tableau_auth = tab.TableauAuth(user,password,site)
server = tab.Server(url)

with server.auth.sign_in(tableau_auth):
    all_datasources, pagination_item = server.datasources.get()
    print("\nThere are {} datasources on site: ".format(pagination_item.total_available))
    print([datasource.name for datasource in all_datasources])

    print("Adding new users")
    new_user_name = random_str(10)
    n_p = "q1q1q1Q!"
    new_user = tab.UserItem(new_user_name, "Publisher")
    n_u = server.users.add(new_user)
    server.users.update(n_u, password=n_p)

    #tableau_auth = tab.TableauAuth(new_user_name,n_p,site)
    #server.auth.sign_in(tableau_auth)

    #wb_item = TSC.WorkbookItem(name='Sample', project_id='1f2f3e4e-5d6d-7c8c-9b0b-1a2a3f4f5e6e')
    # call the publish method with the workbook item
    #wb_item = server.workbooks.publish(wb_item, 'SampleWB.twbx', 'Overwrite')
