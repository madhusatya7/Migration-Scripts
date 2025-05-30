
import xmlrpc.client as xmlrpclib
from datetime import datetime as dt, timedelta as td

# version 12
url_common="http://193.123.91.114:8069/xmlrpc/2/common"
url_object="http://193.123.91.114:8069/xmlrpc/2/object"

sock_common = xmlrpclib.ServerProxy(url_common)
dbname="rahi_17"
username="sidmec1"
pwd="sankar123"
uid = sock_common.authenticate(dbname, username, pwd, {})
sock = xmlrpclib.ServerProxy(url_object)

# version 18
url_common18="http://localhost:8069/xmlrpc/2/common"
url_object18="http://localhost:8069/xmlrpc/2/object"

sock_common18 = xmlrpclib.ServerProxy(url_common18)
dbname18="alrahi_live_master"
username18="sidmec"
pwd18="RahiSm81o15M1R>"
uid18 = sock_common18.authenticate(dbname18, username18, pwd18, {})
sock18 = xmlrpclib.ServerProxy(url_object18)

def get_mapped_rec(model,ID):
	rec = sock18.execute_kw(dbname18, uid18, pwd18, model,'search_read', [[('old_id','=',ID)]], {'fields': ['id','old_id']})
	if rec:
		rst = rec[0]['id']
		return rst
	else:
		return False
def get_mapped_reccords(model,IDS):
	recds = []
	for ID in IDS:
		rec = sock18.execute_kw(dbname18, uid18, pwd18, model,'search_read', [[('old_id','=',ID)]], {'fields': ['id','old_id']})
		if rec:
			rst = rec[0]['id']
			recds.append(rst)
	return recds


def get_cogs_price_updates(v18_rec,v12_rec,acc_payble18,acc_payble12):
    # print("\n\n>>>>>>>>>>>>>??",p_id12,cogs_mapped_idv18,stock_outputv18,v18_rec)
    ac_payvabl8 = sock18.execute_kw(dbname18, uid18, pwd18, 'account.move.line','search_read', [[('move_id','=',v18_rec),('account_id', '=',53),('display_type','=','payment_term'),('product_id','=',False)]], {'fields': ['id','account_id','partner_id','product_id','name','debit','credit']})
    
    ac_payable12 = sock.execute_kw(dbname, uid, pwd, 'account.move.line','search_read', [[('move_id','=',v12_rec),('account_id', '=',acc_payble12),('product_id','=',False)]], {'fields': ['id','account_id','partner_id','product_id','name','debit','credit']})
    # print("ac_payvabl8 >>>>>>>ac_payable12>",ac_payvabl8,ac_payable12)
    
    if ac_payable12:
        pay_label = ac_payable12[0]['name']
        if pay_label == '':
            pay_label = "''"
        # for account payables
        for v18l4 in ac_payvabl8:
            aml_id4 = v18l4['id']
            sql_account_pay = f"update account_move_line set name={pay_label},account_id={acc_payble18} where id={aml_id4}"
            # print(sql_account_pay)
            sa4 = sock18.execute_kw(dbname18, uid18, pwd18, 'account.move', 'execute_raw_sql', [sql_account_pay])
    return True


# account_invoice = sock.execute_kw(dbname, uid, pwd, 'account.invoice', 'search', [[('date_invoice','>=','2024-01-01'),('company_id','=',5)]],{'order': 'id DESC'})
##############For not contain credir notes and valsale journal#####
# account_invoice = sock.execute_kw(dbname, uid, pwd, 'account.invoice', 'search', [[('type','!=','out_refund'),('journal_id','!=',266),('date_invoice','=','2024-01-01'),('company_id','=',2)]],{'order': 'id DESC'})
# domain = [106378,106333,106254,106241,106183,106154,106117,106111,106091,106082,106046,105848,105834,105829,105827,105824,105813,105810,105736,105687,105546,105531,105517,105507,105497,105491,105489,105482,105479,105467,105466,105424,105334,105314,105310,105303,105297,105286,105239,105218,105209,105198,105188,105175,105172,105163,105162,105003,104977,104973,104948,104946,104945,104943,104941,104930,104929,104927,104906,104901,104814,104807,104796,104692,104687,104677,104674,104671,104663,104655,104649,104642,104639,104637,104633,104622,104618,104617,104530,104529,104526,104424,104407,104399,104390,104387,104386,104385,104363,104343,104340,129934,104306,104297,104220,104120,104112,104110,104108,104087,104083,104079,104070,104052,104038,129629,104025,104020,104003,117613,103799,103792,103783,103781,129448,103775,103774,103767,103766,129417,103765,117442,103721,103720,117413,117406,129221,103608,103586,103568,103558,103555,103536,103535,103505,103488,103469,103464,103414,103413,103411,103395,103393,103392,103389,103388,103371,103326,103313,103302,103297,103289,103280]
# domain = [('id','in',[102108])]
domain = [('journal_id','=',274),('state','not in',['draft','cancel']),('company_id','=',23),('date_invoice','>=','2025-01-01'),('date_invoice','<=','2025-02-16')]
account_invoice = sock.execute_kw(dbname, uid, pwd, 'account.invoice', 'search', [domain],{'order': 'id DESC'})

print("length",len(account_invoice))

####################
#account_invoice = account_invoice[240:]
#print("\n\n> New length>>>>>>",len(account_invoice))
######################

count = 0
if len(account_invoice)>0:
    for rec in range(0,len(account_invoice)):
        account_invoice_rec = sock.execute_kw(dbname, uid, pwd, 'account.invoice', 'search_read',[[('id', '=', account_invoice[rec])]], {
												'fields': ['name','number','date_invoice','date','date_due','reference','partner_id','partner_shipping_id','payment_term_id','user_id','currency_id','journal_id','company_id','type','state']})


        number18 = account_invoice_rec[0]['number'] if account_invoice_rec[0] else '' 
        mname18 = account_invoice_rec[0]['name'] if account_invoice_rec[0] else ''
        date_invoice18 = account_invoice_rec[0]['date_invoice']
        date_due18 = account_invoice_rec[0]['date_due'] if account_invoice_rec[0]['date_due'] else dt.now().date().strftime("%Y-%m-%d")
        date18 = account_invoice_rec[0]['date'] 
        reference18 = account_invoice_rec[0]['reference']
        # ref18 = account_invoice_rec[0]['ref']
        state18 = account_invoice_rec[0]['state']
        #m2o field
        partner_id = int(account_invoice_rec[0]['partner_id'][0])
        partner_id18 = get_mapped_rec(model='res.partner',ID=partner_id) if partner_id else False
        partner_shipping_id = int(account_invoice_rec[0]['partner_shipping_id'][0] if account_invoice_rec[0]['partner_shipping_id'] else False)
        partner_shipping_id18 = get_mapped_rec(model='res.partner', ID=partner_shipping_id) if partner_shipping_id else False

        # payment_term_id = int(account_invoice_rec[0]['payment_term_id'][0])
        # invoice_payment_term_id18 = get_mapped_rec(model='account.payment.term', ID=payment_term_id)
        invoice_payment_term_id18 = 1
        user_id = int(account_invoice_rec[0]['user_id'][0] if account_invoice_rec[0]['user_id'] else 2)
        user_id18 = get_mapped_rec(model='res.users', ID=user_id) if user_id else False

        # team_id = int(account_invoice_rec[0]['team_id'][0])
        # team_id18 = get_mapped_rec(model='crm.team', ID=team_id)

        # currency_id = int(account_invoice_rec[0]['currency_id'][0])
        # currency_id18 = get_mapped_rec(model='res.currency', ID=currency_id)
        currency_id18 = 128

        journal_id = int(account_invoice_rec[0]['journal_id'][0])
        journal_id18 = get_mapped_rec(model='account.journal', ID=journal_id) if journal_id else False
        company_id = int(account_invoice_rec[0]['company_id'][0])
        company_id18 = get_mapped_rec(model='res.company', ID=company_id) if company_id else False

        move_type18 =  account_invoice_rec[0]['type'] if account_invoice_rec[0] else 'entry'

        record_ID = account_invoice_rec[0]['id']

        # 'invoice_payment_term_id':invoice_payment_term_id18, 'invoice_user_id':user_id18,
        create_vals = {'old_id':record_ID,'name':number18,'invoice_date':date_invoice18,'date': date18 or dt.now().date().strftime("%Y-%m-%d") ,'invoice_date_due':date_due18,'payment_date': date_invoice18 or dt.now().date(),'ref':reference18,'partner_id':partner_id18,'currency_id':currency_id18,'journal_id':journal_id18,'company_id':company_id18,'move_type':move_type18}

        account_invoice_rec_line = sock.execute_kw(dbname, uid, pwd, 'account.invoice.line', 'search_read',
                                              [[('invoice_id', '=', record_ID)]], {
                                                  'fields': ['name', 'product_id','account_id', 'quantity', 'uom_id','price_unit', 'invoice_line_tax_ids', 'discount', 'price_subtotal']})

        # print (account_invoice_rec_line)
        line_obj = []
        prod_id = {}
        prod_list = []
        for line in account_invoice_rec_line:
            aml_id = line['id']
            name18 = line['name']
            product_id = line['product_id'][0]
            product_id18 = get_mapped_rec(model='product.product', ID=product_id) if product_id else False
            account_id = line['account_id'][0]
            account_id18 = get_mapped_rec(model='account.account',ID=account_id) if account_id else False
            quantity18 = line['quantity']
            uom_id = line['uom_id'][0] if line['uom_id'] else False
            uom_id18 = get_mapped_rec(model='uom.uom', ID=uom_id) if uom_id else False
            price_unit18 = line['price_unit']
            invoice_line_tax_ids = line['invoice_line_tax_ids']
            invoice_line_tax_ids18 = get_mapped_reccords(model='account.tax', IDS=invoice_line_tax_ids)
            #invoice_line_tax_ids18 = get_mapped_taxes(IDS=invoice_line_tax_ids)
            discount18 = line['discount']
            price_subtotal18 = line['price_subtotal']

            obj = {'old_id':aml_id,'name':name18, 'display_type': 'product','product_id':product_id18, 'account_id':account_id18,'quantity':quantity18, 'product_uom_id':uom_id18,'price_unit':price_unit18, 'tax_ids':invoice_line_tax_ids18, 'discount':discount18, 'price_subtotal':price_subtotal18}
            # prod_id.update({product_id18 : [product_id,aml_id]})
            prod_list.append((product_id18,product_id,aml_id))
            line_obj.append((0, 0, obj))
        

        create_vals.update({'invoice_line_ids': line_obj})

        print (f"\n\n\n Creation Record {rec} >>>>??????",create_vals)
        
        rec_is_exitst = sock18.execute_kw(dbname18, uid18, pwd18, 'account.move','search_read', [[('old_id','=',record_ID)]], {'fields': ['old_id','name']})
        
        if not rec_is_exitst:
            reslt =sock18.execute_kw(dbname18, uid18, pwd18, 'account.move','create', [create_vals])
            print('\n created Record in v18>>>>>>>>>',reslt)
            if state18 in ['open','in_payment','paid']:
                r = sock18.execute_kw(dbname18, uid18, pwd18, 'account.move', 'action_post', [reslt],{})
                # acc_payble18 = 3757
                # acc_payble12 = 983

                acc_payble18 = 5226
                acc_payble12 = 5379

                rec12 = sock.execute_kw(dbname, uid, pwd, 'account.move','search_read', [[('name','=',number18)]], {'fields': ['id']})
                rec12_id = rec12[0]['id'] if rec12[0] else False
                prd =list(prod_id.keys())

                rn = get_cogs_price_updates(reslt,rec12_id,acc_payble18,acc_payble12)
                
        else:
            print (f"\n\n Record existed?\n")
            count +=1


    print ("\n\n\n<<<<<<<<<<<EXisted records >>>>>>>>>>>>",count)

