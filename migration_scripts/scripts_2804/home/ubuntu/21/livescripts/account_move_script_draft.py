

import xmlrpc.client as xmlrpclib
from datetime import datetime as dt, timedelta as td

# version 18
url_common18="http://localhost:8069/xmlrpc/2/common"
url_object18="http://localhost:8069/xmlrpc/2/object"

sock_common18 = xmlrpclib.ServerProxy(url_common18)
dbname18="alrahi_live_0401_15"
username18="sidmec"
pwd18="$idmectech@com"
uid18 = sock_common18.authenticate(dbname18, username18, pwd18, {})
sock18 = xmlrpclib.ServerProxy(url_object18)


#domain = [('date','>=','2024-01-01'),('company_id','=',26),('journal_id','in', [146,147,148,187])]
domain = [('date','>=','2024-01-01'),('company_id','=',26),('state','in',['posted','cancel'])]

account_move = sock18.execute_kw(dbname18, uid18, pwd18, 'account.move','search', [domain],{'order': 'id DESC'})
print("\n\n>>>>>Total length",len(account_move))

##############################
#account_move = account_move[:7000]
#account_move = account_move[70:]
#print("\nNew length>>>>>>>>",len(account_move))
###########################



sock18.execute_kw(dbname18, uid18, pwd18, 'account.move', 'button_draft', [account_move])
#sock18.execute_kw(dbname18, uid18, pwd18, 'account.move', 'unlink', [account_move])
print (f"\n >>>>>>COMPLETED >>>>>>?\n\n")
