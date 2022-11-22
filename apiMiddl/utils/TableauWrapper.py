# import tableauserverclient as tab
# import requests
# from django.conf import settings
# from tableaudocumentapi import *
# from tableauhyperapi import TableName
# from utils.random_utils import *
# import pandas as pd
# import pantab
# import time
#
# class TableauWrapper:
#
#     def create_group(self, name):
#         with self.server.auth.sign_in(self.auth):
#             group = tab.GroupItem(name=name)
#             print("[+] Tableau: creating group " + name)
#             return self.server.groups.create(group)
#
#     def add_user_to_group(self, group_item, user_item):
#         with self.server.auth.sign_in(self.auth):
#             return self.server.groups.add_user(group_item, user_item.id)
#
#     @staticmethod
#     def get_trusted_ticket(username):
#
#         data = {
#                 "username": username,
#                 "target_site": settings.TABLEAU_SERVER['DEFAULT_SITE']
#         }
#
#         r = requests.post(settings.TABLEAU_SERVER['URL']+"/trusted", data)
#         return r.content
#
#     def __init__(
#             self, user = settings.TABLEAU_SERVER['ADMIN_LOGIN'],
#             password = settings.TABLEAU_SERVER['ADMIN_PASS'],
#             site = settings.TABLEAU_SERVER['DEFAULT_SITE'],
#             url = settings.TABLEAU_SERVER['URL']
#         ):
#         self.site = site
#         self.url = url
#         self.user = user
#         self.password = password
#         self._connect()
#
#     def prepare_xml_template(self, ds_name, template_path="static/tableau/template_with_ds.twb", output_path = "/tmp/test.twb"):
#
#         template = open(template_path, 'r').read()
#
#         data = {
#                 'caption': ds_name,
#                 'name': ds_name,
#                 'id': ds_name,
#                 'dbname': ds_name
#         }
#
#         template = template.format(**data)
#         f = open(output_path, "w+")
#         f.write(template)
#         f.close()
#
#     def prepare_xml_template_with_db(self, table_name, template_path="static/tableau/template_with_db.twb", output_path = "/tmp/test.twb"):
#
#         with open(template_path, 'r') as f:
#             template = f.read()
#
#         data = {
#                 'table': table_name,
#                 'db_host': "analytics-platform.ml",
#                 'db_pass': "dVre445Vsd",
#                 "db_db": "public"
#         }
#
#         template = template.format(**data)
#         f = open(output_path, "w+")
#         f.write(template)
#         f.close()
#
#     def publish_workbook_with_template(self, wb_name, dest_project_name, csv_path, ds_name):
#
#         path_to_wb = "/tmp/%s.twb" % wb_name
#
#         print("Publishing to project name: " + dest_project_name)
#         proj = self.get_project_by_name(dest_project_name)
#         print("Got project: " + proj)
#         self.publish_datasource(proj.id, csv_path, ds_name)
#         self.prepare_xml_template(ds_name, output_path=path_to_wb)
#         return self.create_workbook(wb_name, dest_project_name, path_to_wb)
#
#
#     def publish_workbook_with_template_for_db(self, wb_name, dest_project_name, dataset, table_name):
#
#         if type(dataset) == int:
#             from items.models import Dataset
#             dataset = Dataset.objects.get(id=dataset)
#
#         if dataset == None:
#             print("No dataset provided or none found")
#             return None
#
#         # sql table creation
#         print("Building and executing sql with name " + table_name)
#         print("Ds: ")
#         print(dataset)
#
#         pre_sql = "drop table if exists %s;" % table_name
#         exec_in_pg(pre_sql)
#         sql = build_sql_for_dataset(table_name, dataset)
#         exec_in_pg(sql)
#
#         path_to_wb = "/tmp/%s.twb" % wb_name
#
#         proj = self.get_project_by_name(dest_project_name)
#
#         self.prepare_xml_template_with_db(table_name, output_path = path_to_wb)
#
#         self.create_workbook(wb_name, dest_project_name, path_to_wb)
#
#         # waiting till tableau creates a workbook
#         while True:
#             w = self.get_workbook_by_name(wb_name)
#             if w == None:
#                 time.sleep(1)
#             else:
#                 break
#
#         self.populate_connections(w)
#
#         with self.server.auth.sign_in(self.auth):
#             con = w.connections[0]
#             con.username = "postgres"
#             con.password = "dVre445Vsd"
#             con.embed_password = True
#
#             self.server.workbooks.update_connection(w, con)
#             print(w.connections)
#
#             return w
#
#     def _connect(self):
#         self.auth = tab.TableauAuth(self.user,self.password,self.site)
#         self.server = tab.Server(self.url, use_server_version=True)
#         self.server.auth.sign_in(self.auth)
#
#     def get_workbook_by_id(self, wb_id):
#         with self.server.auth.sign_in(self.auth):
#             wbs = self.server.workbooks.get()
#             for wb in wbs[0]:
#                 if wb.id == wb_id:
#                     return wb
#             return None
#
#     def copy_workbook(self, wb_name, new_wb_name, dest_project):
#
#         #new_wb_name += "1"
#
#         print("Creating tableu connection")
#         t = Tab()
#         #wb_name = "wb_with_ds"
#         print("Getting workbook name: ")
#         w = t.get_workbook_by_name(wb_name)
#         print("Workbook: " + str(w))
#
#         """
#         t.populate_connections(w)
#         with t.server.auth.sign_in(t.auth):
#             print("Wb connections: " + str(w.connections))
#         """
#
#         print("Downloading workbook")
#         path = "/tmp/%s.twb" % wb_name
#         t.download_workbook(w.id, path)
#
#         #path = "/tmp/wb.twb"
#         print("Reading workbook " + path)
#         w = tda.Workbook(path)
#         print(w)
#         print(w.datasources)
#
#         print("Publishing ")
#         return t.create_workbook(new_wb_name, dest_project, path)
#
#     def get_sites(self):
#         with self.server.auth.sign_in(self.auth):
#             return self.server.sites.get()
#
#     def get_token(self):
#         with self.server.auth.sign_in(self.auth):
#             return self.server.auth_token
#
#
#     ######################################
#     ## DATASOURCES
#     ######################################
#     def get_datasources(self):
#         with self.server.auth.sign_in(self.auth):
#             return self.server.datasources.get()
#
#     def download_datasource(self, datasource_id, path):
#         with self.server.auth.sign_in(self.auth):
#             return self.server.datasources.download(datasource_id, path)
#
#
#
#     def publish_datasource(self, project_id, path, name):
#         filename = "{}.hyper".format(name)
#         df = pd.read_csv(open(path, 'r'))
#         table = TableName("Extract", "Extract")
#         pantab.frame_to_hyper(df, filename, table=table)
#
#         with self.server.auth.sign_in(self.auth):
#             file_path = filename
#             new_datasource = tab.DatasourceItem(project_id)
#             new_datasource = self.server.datasources.publish(
#                 new_datasource, file_path, 'Overwrite')
#
#             return new_datasource
#
#
#     ######################################
#     ## PROJECTS
#     ######################################
#
#     def create_project(self, name, desc=None):
#         print("Tableau: creating new project name: " + name)
#         with self.server.auth.sign_in(self.auth):
#             new_project_item = tab.ProjectItem(name, description=desc)
#             return self.server.projects.create(new_project_item)
#
#     def get_project_by_name(self, name=None):
#         for proj in self.get_projects():
#             if proj.name == name:
#                 return proj
#         return None
#
#     def get_project_by_id(self, wb_id=None):
#         for proj in self.get_projects():
#             if proj.id == wb_id:
#                 return proj
#         return None
#
#     def get_projects(self):
#         with self.server.auth.sign_in(self.auth):
#             all_project_items, pagination_item = self.server.projects.get()
#             return all_project_items
#
#     ######################################
#     ## WORKBOOKS
#     ######################################
#
#     def get_user_workbooks(self, usename):
#         with self.server.auth.sign_in(self.auth):
#             user = self.get_user_by_name(username)
#
#     def get_workbooks(self):
#         with self.server.auth.sign_in(self.auth):
#             return self.server.workbooks.get()
#
#     def download_workbook(self, workbook_id, path = "/tmp/test_workbook"):
#         with self.server.auth.sign_in(self.auth):
#             return self.server.workbooks.download(workbook_id, path)
#
#     def get_workbooks_by_project(self, project):
#         with self.server.auth.sign_in(self.auth):
#             for wb in self.server.workbooks.get()[0]:
#                 if wb.project_id == project.id:
#                     yield wb
#
#     def get_workbook_by_name(self, name):
#         with self.server.auth.sign_in(self.auth):
#             wbs = self.server.workbooks.get()
#
#             for wb in wbs[0]:
#                 if wb.name == name:
#                     return wb
#             return None
#
#     def populate_connections(self, workbook):
#         with self.server.auth.sign_in(self.auth):
#             self.server.workbooks.populate_connections(workbook)
#
#
#     def populate_preview_image(self, workbook):
#         with self.server.auth.sign_in(self.auth):
#             self.server.workbooks.populate_preview_image(workbook)
#             return workbook.preview_image
#
#     def create_workbook(self, name, project_name="Default", file_path = "static/tableau_workbook_template.twb"):
#         with self.server.auth.sign_in(self.auth):
#             project_id = self.get_project_by_name(project_name).id
#
#         with self.server.auth.sign_in(self.auth):
#             new_workbook = tab.WorkbookItem(project_id, name, show_tabs=True)
#             return self.server.workbooks.publish(new_workbook, file_path, 'Overwrite')
#
#     ######################################
#     ## USERS
#     ######################################
#
#     def get_users(self):
#         with self.server.auth.sign_in(self.auth):
#             return self.server.users.get()[0]
#
#     def delete_user(self, name):
#         user = self.get_user_by_name(name)
#         with self.server.auth.sign_in(self.auth):
#             return self.server.users.remove(user.id)
#
#     def create_user(self, new_user, new_password, role):
#         with self.server.auth.sign_in(self.auth):
#             new_user_object = tab.UserItem(new_user, role)
#             new_user_object = self.server.users.add(new_user_object)
#             self.server.users.update(new_user_object, password=new_password)
#
#         return new_user_object
#
#
#     def get_user_by_name(self, name):
#
#         with self.server.auth.sign_in(self.auth):
#             all_users, pagination_item = self.server.users.get()
#             for user in all_users:
#                 if user.name == name:
#                     #print([user for user in all_users])
#                     return user
#
#         return None
#
#     # not done
#     def add_datasource(self, aaaaaaaaaaaaaaaaaaaaaaaa):
#         project_id = self.get_project_by_name("Default").id
#         ds = tab.DatasourceItem(project_id)
#
#     def list(self):
#
#         with self.server.auth.sign_in(self.auth):
#             print(dir(self.auth))
#             print(dir(self.server))
#
#             print(self.auth.password)
#             print(self.auth.credentials)
#             print(self.auth.site)
#             print(self.auth.username)
#             print(self.server._auth_token)
#             print(self.server.auth)
#             print(self.server.auth_token)
#             print(self.server.site_id)
#
#     def test(self):
#
#         w = t.get_workbooks()[0][0]
#         p = t.get_project_by_name("Default")
#
#
# if __name__ == "__main__":
#     t = TableauWrapper()
#     t.test()
