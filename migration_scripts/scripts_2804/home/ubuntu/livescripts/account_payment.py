import xmlrpc.client as xmlrpclib
from datetime import datetime as dt, timedelta as td

# version 12
url_common="http://193.123.91.114:8069/xmlrpc/2/common"
url_object="http://193.123.91.114:8069/xmlrpc/2/object"

sock_common = xmlrpclib.ServerProxy(url_common,allow_none=True)
dbname="rahi_08"
username="sidmec3"
pwd="sankar123"
uid = sock_common.authenticate(dbname, username, pwd, {})
sock = xmlrpclib.ServerProxy(url_object,allow_none=True)

# version 18
url_common18="http://localhost:8069/xmlrpc/2/common"
url_object18="http://localhost:8069/xmlrpc/2/object"

sock_common18 = xmlrpclib.ServerProxy(url_common18,allow_none=True)
dbname18="alrahi_live_master"
username18="sidmec"
pwd18="RahiSm81o15M1R>"
uid18 = sock_common18.authenticate(dbname18, username18, pwd18, {})
sock18 = xmlrpclib.ServerProxy(url_object18,allow_none=True)

def get_mapped_rec(model,ID):
	rec = sock18.execute_kw(dbname18, uid18, pwd18, model,'search_read', [[('old_id','=',ID)]], {'fields': ['id','old_id']})
	if rec:
		rst = rec[0]['id']
		return rst
	else:
		return False

domain = [('id','=',3039105)]
#domain = [('journal_id','not in',[16,311,264,327]),('payment_date','>=','2025-01-01'),('payment_date','<=','2025-04-05'),('payment_type','!=','transfer'),('state','not in',['draft','cancelled']),('company_id','=',2)]
account_payment = sock.execute_kw(dbname, uid, pwd, 'account.payment', 'search', [domain])


def get_rec(payment_type,type,journal_id):
    method_rec = sock18.execute_kw(dbname18, uid18, pwd18, 'account.payment.method','search_read', [[('payment_type','=',payment_type),('code','=',type)]], {'fields': ['id']})
    print (method_rec,payment_type,type,journal_id)
    if method_rec:
        rst = method_rec[0]['id']
        method_line_rec = sock18.execute_kw(dbname18, uid18, pwd18, 'account.payment.method.line','search_read', [[('payment_method_id','=',rst),('journal_id','=',journal_id)]], {'fields': ['id']})
        if method_line_rec:
            rslt = method_line_rec[0]['id']
    return rst,rslt

# for account payment record
def get_querry(move_id,id):
    print ("\n\n\n\n\n>>?????????")
    if move_id:
        sql_account_pay = f"update account_payment set move_id={move_id} where id={id}"
        print(sql_account_pay)
        s = sock18.execute_kw(dbname18, uid18, pwd18, 'account.move', 'execute_raw_sql', [sql_account_pay])
    return s
    


#print(account_payment)
#account_payment = account_payment[910:]
#account_payment = account_payment[1020:]
#account_payment = account_payment[610:]
#account_payment = account_payment[10000:]
#account_payment = account_payment[650:]

print("length",len(account_payment))

if len(account_payment)>0:
    for rec in range(0,len(account_payment)):
        account_payment_rec = sock.execute_kw(dbname, uid, pwd, 'account.payment', 'search_read',[[('id', '=', account_payment[rec])]], {
												'fields': ['name','payment_type','partner_type','partner_id','amount','company_id','journal_id','communication','payment_transaction_id','cheque_num','state','payment_date','due_date']})

        print(f"first {rec} is :{account_payment_rec}")
        name18 = account_payment_rec[0]['name']
        payment_type18 = account_payment_rec[0]['payment_type'] if account_payment_rec[0]['payment_type'] else ''
        partner_type18 = account_payment_rec[0]['partner_type'] if account_payment_rec[0]['partner_type'] else ''
        amount18 = float(account_payment_rec[0]['amount'])
        communication18 = account_payment_rec[0]['communication'] if account_payment_rec[0]['communication'] else ''
        state18 = account_payment_rec[0]['state']

        payment_date18 = account_payment_rec[0]['payment_date'] if account_payment_rec[0]['payment_date'] else False
        cheque_num18 = account_payment_rec[0]['cheque_num'] if account_payment_rec[0]['cheque_num'] else ''
        
        # M2O fields
        partner_id = account_payment_rec[0]['partner_id']
        if partner_id:
            partner_id = int(account_payment_rec[0]['partner_id'][0])
            partner_id18 = get_mapped_rec(model='res.partner', ID=partner_id)
        else:
            partner_id18 = False
        # partner_id = int(account_payment_rec[0]['partner_id'][0])
        # partner_id18 = get_mapped_rec(model='res.partner', ID=partner_id)
        
        company_id = account_payment_rec[0]['company_id']
        if company_id:
            company_id = int(account_payment_rec[0]['company_id'][0])
            company_id18 = get_mapped_rec(model='res.company',ID=company_id)
        else:
            company_id18 = False

        journal_id = account_payment_rec[0]['journal_id'][0]
        if journal_id:
            journal_id = int(account_payment_rec[0]['journal_id'][0])
            journal_id18 = get_mapped_rec(model='account.journal', ID=journal_id)
        else:
            journal_id = False
        
        payment_method_line_id = get_rec(payment_type18,'manual',journal_id18)

        payment_method_line_id18 = payment_method_line_id[1]
        payment_method_id18 = payment_method_line_id[0]

        # payment_transaction_id = int(account_payment_rec[0]['payment_transaction_id'][0])
        # payment_transaction_id18 = get_mapped_rec(model='payment.transaction', ID=payment_transaction_id)
        currency_id18 = 128
        record_ID = account_payment_rec[0]['id']
        # get the relavant account move id 
        mv_rec = sock18.execute_kw(dbname18, uid18, pwd18, 'account.move','search_read', [[('ref','=',communication18)]], {'fields': ['id']})
        if mv_rec:
            mv_id = mv_rec[0]['id']
        else:
             mv_id = False
        
        

        values = {'old_id':record_ID, 'name':name18, 'payment_type':payment_type18,'partner_type':partner_type18, 'cheque_num' : cheque_num18, 'payment_method_id':payment_method_id18 ,'payment_method_line_id':payment_method_line_id18,'currency_id':currency_id18, 'partner_id':partner_id18, 'amount':amount18, 'memo':communication18, 'date':payment_date18, 'company_id':company_id18,'journal_id':journal_id18 }
        print(f"\ncreate values >>>: {values}")
        ap_rec_is_exist = sock18.execute_kw(dbname18, uid18, pwd18, 'account.payment', 'search_read',
                                                     [[('old_id', '=', record_ID)]], {'fields': ['old_id']})

        # print(">>>>>>>>>>>>>>>",mv_id)
        if not ap_rec_is_exist:
            result = sock18.execute_kw(dbname18, uid18, pwd18, 'account.payment', 'create', [values])
            print("\ncreated record>>>>",result)
            # print(">>>>>>>>>>>>>>>",mv_id)
            
            try:
                if state18 == 'posted':
                    sock18.execute_kw(dbname18, uid18, pwd18, 'account.payment', 'action_post', [[result]])
                    
            # if state18 == 'cancelled':
            #     n= sock18.execute_kw(dbname18, uid18, pwd18, 'account.payment', 'action_cancel', [[result]])
            # print("\n\nPayment posted for record>>", n)
                # payment connecting 
                
            except Exception as e:
                print(f">>>>>>>>>Error processing record  {e}>>>>>>>>>>>>>>>>\n\n")
            if mv_id:
                n = get_querry(mv_id,result)
                print("\n\n\n>>>>>>>>>update link record",n,mv_id)
        else:
            print(f"\n Record existed?\n")
