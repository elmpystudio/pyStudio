import requests
import xml.etree.ElementTree as ET 

def url(endpoint):
    return "" + endpoint


def signin():
    u = url("api/3.4/auth/signin")
    user = "api-user"
    password = "Aa123456"
    site = "Research"

    msg = """<tsRequest>
    <credentials name="%s" password="%s">
            <site contentUrl="%s" />
    </credentials>
</tsRequest>""" % (user, password, site)

    print(msg)
    r = requests.post(u, data=msg)
    print(r.status_code)
    print(r.content)

    tree = ET.fromstring(r.content)
    print(tree)

    # get root element 
    for child in tree.iter('*'):
        print(child.tag, child.attrib)

    for child in tree.iter('{http://tableau.com/api}credentials'):
        token = child.attrib['token']

    for child in tree.iter('{http://tableau.com/api}site'):
        site_id = child.attrib['id']

    print("Token: " + token)
    print("site_id: " + site_id)

    s = requests.Session()
    s.headers.update({"X-Tableau-Auth": token})

    data = {
            "token": token,
            "site_id": site_id,
            "session": s
            }
    
    return data

def projects(data):
    u = url("api/3.4/sites/%s/projects" % data['site_id'])

    req = """
        <tsRequest>
                <project
                  name="new-project-name32424"
                  description="This is a new project" />
        </tsRequest>
        """

    r = data["session"].post(u, data=req)
    print(r.status_code)
    print(r.content)

data = signin()
projects(data)
