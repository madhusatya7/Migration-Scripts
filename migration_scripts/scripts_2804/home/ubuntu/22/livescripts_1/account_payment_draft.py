import xmlrpc.client as xmlrpclib
from datetime import datetime as dt, timedelta as td

# version 18
url_common18="http://localhost:8069/xmlrpc/2/common"
url_object18="http://localhost:8069/xmlrpc/2/object"

sock_common18 = xmlrpclib.ServerProxy(url_common18)
dbname18="alrahi_live_1201_1"
username18="sidmec"
pwd18="$idmectech@com"
uid18 = sock_common18.authenticate(dbname18, username18, pwd18, {})
sock18 = xmlrpclib.ServerProxy(url_object18)


#domain = [('old_id','!=',0),('date','>=','2024-01-01'),('date','<=','2024-01-31'),('company_id','=',26)]
domain = [('old_id','!=',0),('date','>=','2024-01-01'),('date','<=','2024-01-31'),('company_id','=',26),('state','=','in_process')]
#domain = [('id','=',749)]
account_pay = sock18.execute_kw(dbname18, uid18, pwd18, 'account.payment','search', [domain],{'order': 'id DESC'})
print("\n\n>>>>>Total length",len(account_pay))
print("\n\n>>>>>Total length",account_pay)
##############################
account_pay = account_pay[:700]
#account_move = account_move[70:]
print("\nNew length>>>>>>>>",len(account_pay))
###########################


#for p in account_pay:
sock18.execute_kw(dbname18, uid18, pwd18, 'account.payment', 'action_draft', [account_pay])
#sock18.execute_kw(dbname18, uid18, pwd18, 'account.payment', 'unlink', [account_move])
print (f"\n >>>>>>COMPLETED >>>>>>?\n\n")
