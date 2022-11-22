import tableauserverclient as tab
# create a new instance of a TableauAuth object for authentication

tableau_auth = tab.TableauAuth('USERNAME', 'PASSWORD', site_id='CONTENTURL')

# create a server instance
# pass the "tableau_auth" object to the server.auth.sign_in() method
