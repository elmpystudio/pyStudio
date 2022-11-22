import os
import sys

from utils.TableauWrapper import TableauWrapper as Tab

t = Tab()
t.publish_workbook_with_template("test_donw", "test_project", "/home/ohai/business.csv", "business")

sys.exit(0)

#--------------------------------------------------
import time

wb_name = "from_api_with_db_inside7"
t.create_workbook(wb_name, "root", "/tmp/db.twb")

while True:
    w = t.get_workbook_by_name(wb_name)
    if w == None:
        print("Waiting")
        time.sleep(1)
    else:
        break

t.populate_connections(w)
with t.server.auth.sign_in(t.auth):

    con = w.connections[0]
    con.username = "postgres"
    con.password = "dVre445Vsd"
    con.embed_password = True

    t.server.workbooks.update_connection(w, con)
    print(w.connections)

#--------------------------------------------------

wb_name = "from_api_with_db_inside6"
w = t.get_workbook_by_name(wb_name)
t.populate_connections(w)
with t.server.auth.sign_in(t.auth):

    con = w.connections[0]
    con.username = "postgres"
    con.password = "dVre445Vsd"
    con.embed_password = True

    t.server.workbooks.update_connection(w, con)
    print(w.connections)

#--------------------------------------------------

def final():

    def prepare_xml_template(template_path, ds_name, output_path = "/tmp/test.twb"):

        template = open(template_path, 'r').read()

        data = {
                'caption': ds_name,
                'name': ds_name,
                'id': ds_name,
                'dbname': ds_name
        }
        template = template.format(**data)
        f = open(output_path, "w+")
        f.write(template)
        f.close()


    from utils.TableauWrapper import TableauWrapper as Tab
    import tableaudocumentapi as tda
    from zipfile import ZipFile

    t = Tab()
    csv_path = "/home/ohai/business.csv"
    new_wb_name = "wb_copied_api_23_04_api"
    dest_project = "test_project"
    ds_name = "test_datasource_name"
    template_path = "/home/ohai/git/analytics-restapi/static/tableau/template_with_ds.twb"
    path_to_wb = "/tmp/test_with_db.twb"

    proj = t.get_project_by_name(dest_project)
    t.publish_datasource(proj.id, csv_path, ds_name)
    prepare_xml_template(template_path, ds_name, path_to_wb)

    t.create_workbook(new_wb_name, dest_project, path_to_wb)

    """

    print("Creating tableu connection")
    t = Tab()
    print("Getting workbook name: " + wb_name)
    w = t.get_workbook_by_name(wb_name)
    print("Workbook: " + str(w))
    """

    """
    print("Downloading workbook")
    path = "/tmp/%s.twb" % wb_name
    t.download_workbook(w.id, path)

    path_to_wb = "/tmp/" + new_wb_name + ".twbx"
    with ZipFile(path_to_wb, "w") as z:
        folder_to_zip = "/tmp/tab"
        for f in get_all_file_paths(folder_to_zip):
            rel = os.path.relpath(f, folder_to_zip)
            print("Zipping: " + f + ":" + rel)
            z.write(f, rel)

    print("Done zipping")

    print("Reading workbook " + path_to_wb)
    w = tda.Workbook(path_to_wb)
    print(w)
    print(w.datasources)

    print("Publishing ")
    t = Tab()
    t.create_workbook(new_wb_name, dest_project, path_to_wb)

    """

if "a" == "a":
    final()

#print("Getting project")
#p = t.get_project_by_name("root")
#print("Project"p)
#t.copy_workbook(w,p)

#t.create_workbook("copied123", "root", "/tmp/test/12345.twb")
