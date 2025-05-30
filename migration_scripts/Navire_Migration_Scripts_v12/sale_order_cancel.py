import xmlrpc.client as xmlrpclib
from datetime import datetime as dt, timedelta as td


# version 18
url_common18="http://139.185.58.40:8069/xmlrpc/2/common"
url_object18="http://139.185.58.40:8069/xmlrpc/2/object"

sock_common18 = xmlrpclib.ServerProxy(url_common18)
dbname18="navire"
username18="sidmec"
pwd18="$idmectech@com"
uid18 = sock_common18.authenticate(dbname18, username18, pwd18, {})
sock18 = xmlrpclib.ServerProxy(url_object18)


#domain = [('date','>=','2024-01-01'),('company_id','=',26),('journal_id','in', [146,147,148,187])]
domain = [('id','=',314),('date_order','>=','2024-02-01'),('date_order','<=','2024-02-29'),('state','in',['sale'])]


sale_order = sock18.execute_kw(dbname18, uid18, pwd18, 'sale.order','search', [domain],{'order': 'id DESC'})
print("\n\n>>>>>Total length",len(sale_order))
print(">>>>>>>>>>>>>>>>",sale_order)

##############################
#sale_order = sale_order[:7000]
#account_move = account_move[70:]
#print("\nNew length>>>>>>>>",len(account_move))
###########################


for order_id in sale_order:
    try:
        sock18.execute_kw(dbname18, uid18, pwd18, 'sale.order', 'action_cancel', [[order_id]])
        sock18.execute_kw(dbname18, uid18, pwd18, 'sale.order', 'unlink', [[order_id]])
        print(f"✅ Cancelled and deleted sale order {order_id}")
    except Exception as e:
        print(f"❌ Failed to cancel/delete sale order {order_id}: {e}")

# # sock18.execute_kw(dbname18, uid18, pwd18, 'sale.order', 'action_cancel', [sale_order])
# sock18.execute_kw(dbname18, uid18, pwd18, 'sale.order', 'unlink', [sale_order])
# print (f"\n >>>>>>COMPLETED >>>>>>?\n\n")

