import xmlrpc.client as xmlrpclib
from datetime import datetime as dt, timedelta as td

# version 12
url_common="http://193.123.91.114:8069/xmlrpc/2/common"
url_object="http://193.123.91.114:8069/xmlrpc/2/object"

sock_common = xmlrpclib.ServerProxy(url_common)
dbname="rahidb"
username="arif"
pwd="sankar123"
uid = sock_common.authenticate(dbname, username, pwd, {})
sock = xmlrpclib.ServerProxy(url_object)

# version 18
url_common18="http://localhost:8069/xmlrpc/2/common"
url_object18="http://localhost:8069/xmlrpc/2/object"

sock_common18 = xmlrpclib.ServerProxy(url_common18)
dbname18="alrahi_live_master"
username18="sidmec"
pwd18="$idmectech@com"
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

def get_cogs_price_updates(v18_rec,v12_rec,cogs_mapped_idv18,stock_outputv18,cogs_mapped_idv12,stock_outputv12,acc_recvbl18,acc_recbl12,acc_payble18,acc_payble12,p_id18,p_id12,amlv12,vansal_tax_act12,vansal_tax_act18,rpl_tax):
    #print("\n\n>>>>>>>>>>>>>??",cogs_mapped_idv18,stock_outputv18)
    # already created as per current cogs and cost current DB main company
    rec18_cog = sock18.execute_kw(dbname18, uid18, pwd18, 'account.move.line','search_read', [[('move_id','=',v18_rec),('account_id', '=',75),('display_type','=','cogs'),('product_id','=',p_id18)]], {'fields': ['id','account_id','partner_id','product_id','name','debit','credit']})
    rec18_stock = sock18.execute_kw(dbname18, uid18, pwd18, 'account.move.line','search_read', [[('move_id','=',v18_rec),('account_id', '=',169),('display_type','=','cogs'),('product_id','=',p_id18)]], {'fields': ['id','account_id','partner_id','product_id','name','debit','credit']})
    ac_receivabl8 = sock18.execute_kw(dbname18, uid18, pwd18, 'account.move.line','search_read', [[('move_id','=',v18_rec),('account_id', '=',10),('display_type','=','payment_term'),('product_id','=',False)]], {'fields': ['id','account_id','partner_id','product_id','name','debit','credit']})
    ac_payvabl8 = sock18.execute_kw(dbname18, uid18, pwd18, 'account.move.line','search_read', [[('move_id','=',v18_rec),('account_id', '=',53),('display_type','=','payment_term'),('product_id','=',False)]], {'fields': ['id','account_id','partner_id','product_id','name','debit','credit']})
    #ac_tax_line18 = sock18.execute_kw(dbname18, uid18, pwd18, 'account.move.line','search_read', [[('move_id','=',v18_rec),('account_id', '=',vansal_tax_act18),('display_type','=','tax'),('product_id','=',False)]], {'fields': ['id','account_id','partner_id','product_id','name','debit','credit']})
    
    #print(">>>>>>>>>>>>>>>>",cogs_mapped_idv12,stock_outputv12)
    # get the line from v12 
    ac_recv12_cogs = sock.execute_kw(dbname, uid, pwd, 'account.move.line','search_read', [[('move_id','=',v12_rec),('account_id', '=',cogs_mapped_idv12),('product_id','=',p_id12)]], {'fields': ['id','account_id','partner_id','product_id','name','debit','credit']})
    ac_recv12_stock = sock.execute_kw(dbname, uid, pwd, 'account.move.line','search_read', [[('move_id','=',v12_rec),('account_id', '=',stock_outputv12),('product_id','=',p_id12)]], {'fields': ['id','account_id','partner_id','product_id','name','debit','credit']})
    ac_receivable12 = sock.execute_kw(dbname, uid, pwd, 'account.move.line','search_read', [[('move_id','=',v12_rec),('account_id', '=',acc_recbl12),('product_id','=',False)]], {'fields': ['id','account_id','partner_id','product_id','name','debit','credit']})
    ac_payable12 = sock.execute_kw(dbname, uid, pwd, 'account.move.line','search_read', [[('move_id','=',v12_rec),('account_id', '=',acc_payble12),('product_id','=',False)]], {'fields': ['id','account_id','partner_id','product_id','name','debit','credit']})
    #ac_tax_line12 = sock.execute_kw(dbname, uid, pwd, 'account.move.line','search_read', [[('move_id','=',v12_rec),('account_id', '=',vansal_tax_act12),('product_id','=',False)]], {'fields': ['id','account_id','partner_id','product_id','name','debit','credit']})
    #print("ac_receivable12 >>>>>>>>",p_id12,v12_rec,acc_recbl12,ac_tax_line12)
    
    
    counter = 0
    for v18l in rec18_cog:
        #print("counter >>>>>>>>>>>>>",counter,ac_recv12_cogs)
        aml_id = v18l['id']
        amt_d = ac_recv12_cogs[counter]['debit']
        amt_c = ac_recv12_cogs[counter]['credit']
        amount_currency18 = amt_d
        if amt_d:
            amount_currency18 = amt_d
        if amt_c:
            amount_currency18 = -amt_c
        counter += 1 
        sql_cogs = f"update account_move_line set debit={amt_d},balance={amount_currency18},account_id={cogs_mapped_idv18} where id={aml_id}"
        sa1 = sock18.execute_kw(dbname18, uid18, pwd18, 'account.move', 'execute_raw_sql', [sql_cogs])
        print(sa1)
    counter1 =0 
    for v18l2 in rec18_stock:
        aml_id2 = v18l2['id']
        #print("counter >>>>>>>>>>>>>",counter,rec18_stock)
        amt2_c = ac_recv12_stock[counter1]['credit'] 
        amt2_d = ac_recv12_stock[counter1]['debit']
        amount_currency118 = -amt2_c
        if amt2_d:
            amount_currency118 = amt2_d
        if amt2_c:
            amount_currency118 = -amt2_c

        counter1 += 1
        sql_stck_op = f"update account_move_line set credit={amt2_c},balance={amount_currency118},account_id={stock_outputv18} where id={aml_id2}"
        #print("\n here querry::>>>>>>>>>",sql_stck_op)
        sa2 = sock18.execute_kw(dbname18, uid18, pwd18, 'account.move', 'execute_raw_sql', [sql_stck_op])
        print(sa2)
    # for account receivables
    if ac_receivable12:
        # counter3 =0 
        for v18l3 in ac_receivabl8:
            aml_id3 = v18l3['id']
            # counter3 += 1
            sql_account_recb = f"update account_move_line set account_id={acc_recvbl18} where id={aml_id3}"
            sa3 = sock18.execute_kw(dbname18, uid18, pwd18, 'account.move', 'execute_raw_sql', [sql_account_recb])
    
    if ac_payable12:
        # for account payables
        # counter4 =0 
        for v18l4 in ac_payvabl8:
            aml_id4 = v18l4['id']
            # counter4 += 1
            sql_account_pay = f"update account_move_line set account_id={acc_payble18} where id={aml_id4}"
            sa4 = sock18.execute_kw(dbname18, uid18, pwd18, 'account.move', 'execute_raw_sql', [sql_account_pay])
    # print("\n\nac_tax_line18>>>>>",ac_tax_line18,ac_tax_line12)
    ########################### for vansale tax replacemetn
    #if ac_tax_line12:
        # counter5 =0 
    #    for v18l5 in ac_tax_line18:
    #        aml_id5 = v18l5['id']
    #        # counter5 += 1
    #        sql_account_tax_rpl = f"update account_move_line set account_id={rpl_tax} where id={aml_id5}"
            # print(sql_account_tax_rpl)
    #        sa5 = sock18.execute_kw(dbname18, uid18, pwd18, 'account.move', 'execute_raw_sql', [sql_account_tax_rpl])
    #return True


# account_invoice = sock.execute_kw(dbname, uid, pwd, 'account.invoice', 'search', [[('date_invoice','>=','2024-01-01'),('company_id','=',14)]],{'order': 'id DESC'})
#account_invoice = sock.execute_kw(dbname, uid, pwd, 'account.invoice', 'search', [[('date_invoice','>=','2024-01-01'),('company_id','=',4)]],{'order': 'id DESC'})
#account_invoice = sock.execute_kw(dbname, uid, pwd, 'account.invoice', 'search', [[('date_invoice','>=','2024-01-01'),('company_id','=',13)]],{'order': 'id DESC'})
#account_invoice = sock.execute_kw(dbname, uid, pwd, 'account.invoice', 'search', [[('date_invoice','>=','2024-01-01'),('company_id','=',18)]],{'order': 'id DESC'})
# account_invoice = sock.execute_kw(dbname, uid, pwd, 'account.invoice', 'search', [[('date_invoice','>=','2024-01-01'),('company_id','=',26)]],{'order': 'id DESC'})
#account_invoice = sock.execute_kw(dbname, uid, pwd, 'account.invoice', 'search', [[('date_invoice','>=','2024-01-01'),('company_id','=',16)]],{'order': 'id DESC'})
# account_invoice = sock.execute_kw(dbname, uid, pwd, 'account.invoice', 'search', [[('date_invoice','>=','2024-01-01'),('company_id','=',12)]],{'order': 'id DESC'})
# account_invoice = sock.execute_kw(dbname, uid, pwd, 'account.invoice', 'search', [[('date_invoice','>=','2024-01-01'),('company_id','=',15)]],{'order': 'id DESC'})
# account_invoice = sock.execute_kw(dbname, uid, pwd, 'account.invoice', 'search', [[('date_invoice','>=','2024-01-01'),('company_id','=',17)]],{'order': 'id DESC'})

# account_invoice = sock.execute_kw(dbname, uid, pwd, 'account.invoice', 'search', [[('date_invoice','>=','2024-01-01'),('company_id','=',5)]],{'order': 'id DESC'})

# account_invoice = sock.execute_kw(dbname, uid, pwd, 'account.invoice', 'search', [[('date_invoice','>=','2024-01-01'), ('date_invoice','<=','2024-01-15'),('company_id','=',2)]],{'order': 'id DESC'})
account_invoice = sock.execute_kw(dbname, uid, pwd, 'account.invoice', 'search', [[('type','!=','out_refund'),('state','not in',['draft','cancel']),('date_invoice','>=','2024-06-01'),('date_invoice','<=','2024-06-30'),('company_id','=',2),('journal_id','=',266)]],{'order': 'id DESC'})
# account_invoice = sock.execute_kw(dbname, uid, pwd, 'account.invoice', 'search', [[('date_invoice','=','2024-01-01'),('company_id','=',2),('journal_id','=',266)]],{'order': 'id DESC'})
# account_invoice = sock.execute_kw(dbname, uid, pwd, 'account.invoice', 'search', [[('date_invoice','>=','2024-01-01'),('company_id','=',5)]],{'order': 'id DESC'})
# account_invoice = sock.execute_kw(dbname, uid, pwd, 'account.invoice', 'search', [[('date_invoice','>=','2024-01-01'),('company_id','=',9)]],{'order': 'id DESC'})
# account_invoice = sock.execute_kw(dbname, uid, pwd, 'account.invoice', 'search', [[('date_invoice','>=','2024-01-01'),('company_id','=',24)]],{'order': 'id DESC'})
#account_invoice = sock.execute_kw(dbname, uid, pwd, 'account.invoice', 'search', [[('date_invoice','>=','2024-01-01'),('company_id','=',19)]],{'order': 'id DESC'})
#account_invoice = sock.execute_kw(dbname, uid, pwd, 'account.invoice', 'search', [[('date_invoice','>=','2024-01-01'),('company_id','=',25)]],{'order': 'id DESC'})
#account_invoice = sock.execute_kw(dbname, uid, pwd, 'account.invoice', 'search', [[('date_invoice','>=','2024-01-01'),('journal_id','=',42),('company_id','=',6)]],{'order': 'id DESC'})
# account_invoice = sock.execute_kw(dbname, uid, pwd, 'account.invoice', 'search', [[('date_invoice','>=','2024-01-01'),('company_id','=',11)]],{'order': 'id DESC'})
# account_invoice = sock.execute_kw(dbname, uid, pwd, 'account.invoice', 'search', [[('date_invoice','>=','2024-01-01'),('company_id','=',7)]],{'order': 'id DESC'})

#account_invoice = sock.execute_kw(dbname, uid, pwd, 'account.invoice', 'search', [[('date_invoice','>=','2024-01-01'),('company_id','=',2)]],{'order': 'id DESC'})

# account_invoice = sock.execute_kw(dbname, uid, pwd, 'account.invoice', 'search', [[('date_invoice','>=','2024-01-01'),('company_id','=',1)]],{'order': 'id DESC'})
# account_invoice = sock.execute_kw(dbname, uid, pwd, 'account.invoice', 'search', [[('date_invoice','>=','2024-01-01'),('company_id','=',3)]],{'order': 'id DESC'})
# account_invoice = sock.execute_kw(dbname, uid, pwd, 'account.invoice', 'search', [[('date_invoice','>=','2024-01-01'),('company_id','=',8)]],{'order': 'id DESC'})
# account_invoice = sock.execute_kw(dbname, uid, pwd, 'account.invoice', 'search', [[('date_invoice','>=','2024-01-01'),('company_id','=',10)]],{'order': 'id DESC'})
# account_invoice = sock.execute_kw(dbname, uid, pwd, 'account.invoice', 'search', [[('date_invoice','>=','2024-01-01'),('company_id','=',22)]],{'order': 'id DESC'})
# account_invoice = sock.execute_kw(dbname, uid, pwd, 'account.invoice', 'search', [[('date_invoice','>=','2024-01-01'),('company_id','=',23)]],{'order': 'id DESC'})
#account_invoice = sock.execute_kw(dbname, uid, pwd, 'account.invoice', 'search', [[('date_invoice','>=','2024-01-01'),('company_id','=',20)]],{'order': 'id DESC'})

print("\n\n\n\n>>>>>>>>>>>>>>>>>>>>length",len(account_invoice))

####################
account_invoice = account_invoice[625:]
#account_invoice = account_invoice[1340:]
print("\n\n> New length>>>>>>",len(account_invoice))
######################

count = 0
if len(account_invoice)>0:
    for rec in range(0,len(account_invoice)):
        account_invoice_rec = sock.execute_kw(dbname, uid, pwd, 'account.invoice', 'search_read',[[('id', '=', account_invoice[rec])]], {
												'fields': ['name','number','date_invoice','date','date_due','reference','partner_id','partner_shipping_id','payment_term_id','user_id','currency_id','journal_id','company_id','type','state']})


        # print(f"first {rec} is :{account_invoice_rec}")

        number18 = account_invoice_rec[0]['number'] if account_invoice_rec[0] else '' 
        mname18 = account_invoice_rec[0]['name'] if account_invoice_rec[0] else ''
        date_invoice18 = account_invoice_rec[0]['date_invoice']
        date_due18 = account_invoice_rec[0]['date_due'] if account_invoice_rec[0]['date_due'] else dt.now().date().strftime("%Y-%m-%d")
        date18 = account_invoice_rec[0]['date'] 
        reference18 = account_invoice_rec[0]['reference']
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
        create_vals = {'old_id':record_ID,'name':number18,'invoice_date':date_invoice18,'date': date18 or dt.now().date().strftime("%Y-%m-%d") ,'invoice_date_due':date_due18,'payment_date': date_invoice18 or dt.now().date(),'payment_reference':reference18,'partner_id':partner_id18,'currency_id':currency_id18,'journal_id':journal_id18,'company_id':company_id18,'move_type':move_type18}

        account_invoice_rec_line = sock.execute_kw(dbname, uid, pwd, 'account.invoice.line', 'search_read',
                                              [[('invoice_id', '=', record_ID)]], {
                                                  'fields': ['name', 'product_id','account_id', 'quantity', 'uom_id','price_unit', 'invoice_line_tax_ids', 'discount', 'price_subtotal']})

        print (account_invoice_rec_line)
        line_obj = []
        # prod_id = {}
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
                cogs_mapped_idv18 = 789 #v18
                stock_outputv18 = 728 #v18
                acc_recvbl18 = 581
                acc_payble18 = 516 
                vansal_tax_act18 = 742 # taxreceivable

                cogs_mapped_idv12 = 293 #direct v12
                stock_outputv12 = 5859 # direct v12
                acc_recbl12 = 193 #direct v12
                acc_payble12 = 243
                vansal_tax_act12 = 259
 
                rpl_tax = 742 # Tota sale account to chaged because details chaged,Modification applied
                rec12 = sock.execute_kw(dbname, uid, pwd, 'account.move','search_read', [[('name','=',number18)]], {'fields': ['id']})
                rec12_id = rec12[0]['id'] if rec12[0] else False
                # prd =list(prod_id.keys())
                print("product lisr",prod_list)
                for p in prod_list:
                # for p in prd:
                    p_id18 = p[0]
                    p_id12 = p[1]
                    amlv12 = p[2]
                    rn = get_cogs_price_updates(reslt,rec12_id,cogs_mapped_idv18,stock_outputv18,cogs_mapped_idv12,stock_outputv12,acc_recvbl18,acc_recbl12,acc_payble18,acc_payble12,p_id18,p_id12,amlv12,vansal_tax_act12,vansal_tax_act18,rpl_tax)
                    
            #if state18 == 'cancel':
            #    sock18.execute_kw(dbname18, uid18, pwd18, 'account.move', 'action_invoice_cancel', [reslt],{})
        else:
            print (f"\n\n Record existed?\n")
            count +=1


    print ("\n\n\n<<<<<<<<<<<EXisted records >>>>>>>>>>>>",count)

