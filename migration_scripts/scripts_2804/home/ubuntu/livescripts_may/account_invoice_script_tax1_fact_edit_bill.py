
import xmlrpc.client as xmlrpclib
from datetime import datetime as dt, timedelta as td

# version 12
url_common="http://161.97.148.133/xmlrpc/2/common"
url_object="http://161.97.148.133/xmlrpc/2/object"

sock_common = xmlrpclib.ServerProxy(url_common)
dbname="liverahi"
username="sidmec2"
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

def sanitise_line(pair,act,reslt):
    #print(f"Sanitising pair: {pair}")
    produc_id= pair[0]
    sql_delete = f"delete from account_move_line where account_id={act} and product_id={produc_id} and move_id={reslt} AND id NOT IN (SELECT MIN(id) FROM account_move_line where account_id={act} and product_id={produc_id} and move_id={reslt} GROUP BY product_id)"
    #print("dlete querry>>>>>>",sql_delete)
    san = sock18.execute_kw(dbname18, uid18, pwd18, 'account.move', 'execute_raw_sql', [sql_delete])
    return san


def get_cogs_price_updates(v18_rec,v12_rec,cogs_mapped_idv18,stock_outputv18,cogs_mapped_idv12,stock_outputv12,acc_recvbl18,acc_recbl12,acc_payble18,acc_payble12,p_id18,p_id12,amlv12):
    #print("\n\n>>>>>>>>>>>>>??",cogs_mapped_idv18,stock_outputv18,v18_rec)
    #print(">>>>>>>>",p_id12,p_id18)
    # already created as per current cogs and cost current DB main company
    rec18_cog = sock18.execute_kw(dbname18, uid18, pwd18, 'account.move.line','search_read', [[('move_id','=',v18_rec),('account_id', '=',75),('display_type','=','cogs'),('product_id','=',p_id18)]], {'fields': ['id','account_id','partner_id','product_id','name','debit','credit']})
    rec18_stock = sock18.execute_kw(dbname18, uid18, pwd18, 'account.move.line','search_read', [[('move_id','=',v18_rec),('account_id', '=',169),('display_type','=','cogs'),('product_id','=',p_id18)]], {'fields': ['id','account_id','partner_id','product_id','name','debit','credit']})
    ac_receivabl8 = sock18.execute_kw(dbname18, uid18, pwd18, 'account.move.line','search_read', [[('move_id','=',v18_rec),('account_id', '=',10),('display_type','=','payment_term'),('product_id','=',False)]], {'fields': ['id','account_id','partner_id','product_id','name','debit','credit']})
    ac_payvabl8 = sock18.execute_kw(dbname18, uid18, pwd18, 'account.move.line','search_read', [[('move_id','=',v18_rec),('account_id', '=',53),('display_type','=','payment_term'),('product_id','=',False)]], {'fields': ['id','account_id','partner_id','product_id','name','debit','credit']})
    
    #print(">>>>>>>>>>>>>>>>",cogs_mapped_idv12,stock_outputv12,v12_rec)
    # get the line from v12 
    ac_recv12_cogs = sock.execute_kw(dbname, uid, pwd, 'account.move.line','search_read', [[('move_id','=',v12_rec),('account_id', '=',cogs_mapped_idv12),('product_id','=',p_id12)]], {'fields': ['id','account_id','partner_id','product_id','name','debit','credit']})
    ac_recv12_stock = sock.execute_kw(dbname, uid, pwd, 'account.move.line','search_read', [[('move_id','=',v12_rec),('account_id', '=',stock_outputv12),('product_id','=',p_id12)]], {'fields': ['id','account_id','partner_id','product_id','name','debit','credit']})
    ac_receivable12 = sock.execute_kw(dbname, uid, pwd, 'account.move.line','search_read', [[('move_id','=',v12_rec),('account_id', '=',acc_recbl12),('product_id','=',False)]], {'fields': ['id','account_id','partner_id','product_id','name','debit','credit']})
    ac_payable12 = sock.execute_kw(dbname, uid, pwd, 'account.move.line','search_read', [[('move_id','=',v12_rec),('account_id', '=',acc_payble12),('product_id','=',False)]], {'fields': ['id','account_id','partner_id','product_id','name','debit','credit']})
    #print("ac_recv12_cogs >>>>>>>>",ac_recv12_cogs)
    counter = 0
    for v18l in rec18_cog:
        #print("counter >>>>>>>>>>>>>",counter,ac_recv12_cogs)
        aml_id = v18l['id']
        amt_d = ac_recv12_cogs[0]['debit']
        amt_c = ac_recv12_cogs[0]['credit']
        amount_currency18 = amt_d
        if amt_d:
            amount_currency18 = amt_d
        if amt_c:
            amount_currency18 = -amt_c
        counter += 1 
        sql_cogs = f"update account_move_line set debit={amt_d},balance={amount_currency18},account_id={cogs_mapped_idv18} where id={aml_id}"
        #print(sql_cogs)
        sa1 = sock18.execute_kw(dbname18, uid18, pwd18, 'account.move', 'execute_raw_sql', [sql_cogs])
        print(sa1)
    counter1 =0 
    for v18l2 in rec18_stock:
        aml_id2 = v18l2['id']
        amt2_c = ac_recv12_stock[0]['credit'] 
        amt2_d = ac_recv12_stock[0]['debit']
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
        counter3 =0 
        for v18l3 in ac_receivabl8:
            aml_id3 = v18l3['id']
            counter3 += 1
            sql_account_recb = f"update account_move_line set account_id={acc_recvbl18} where id={aml_id3}"
            sa3 = sock18.execute_kw(dbname18, uid18, pwd18, 'account.move', 'execute_raw_sql', [sql_account_recb])
    
    if ac_payable12:
        # for account payables
        counter4 =0 
        for v18l4 in ac_payvabl8:
            aml_id4 = v18l4['id']
            counter4 += 1
            sql_account_pay = f"update account_move_line set account_id={acc_payble18} where id={aml_id4}"
            sa4 = sock18.execute_kw(dbname18, uid18, pwd18, 'account.move', 'execute_raw_sql', [sql_account_pay])
    return True


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
##############For not contain credir notes and valsale journal#####
#account_invoice = sock.execute_kw(dbname, uid, pwd, 'account.invoice', 'search', [[('type','!=','out_refund'),('journal_id','!=',266),('state','not in',['draft','cancel']),('date_invoice','>=','2024-05-01'),('date_invoice','<=','2024-05-31'),('company_id','=',2)]],{'order': 'id DESC'})

domain = [('id','in',[149173,150977,151085,151086,152677,152712,152846,152894,152924,152984,153348,153564,154581,154753,155102,155105,155108,155112,155116,155164,155167,155170,155185,155402,155595,155662,155665,155803,155816,156068,156072,156096,156360,156668,156672,156673,156678,156681,156687,156702,157258,157262,157263,157266,157269,157276,157497,157571,157914,157992,157993,157998,158146,158459,158578,158633,158738,158743,158750,158756,158824,158852,158862,158888,158912,158935,158940,158945,158958,159307,159427,159543,159673,159770,159910,159921,160025,160101,160112,160150,160192,160333,160338,160340,160384,160395,160400,160570,160581,160764,160814,160839,160862,160870,160879,160881,160924,160925,160926,160927,160930,160936,161213,161305,161307,161347,161350,161353,161512,161682,161686,161689,161693,161905,161906,162127,162132,162138,162148,162150,162433,162460,162471,162475,162605,162831,162921,162949,162958,162968,162992,163002,163062,163096,163324,163330,163331,163333,163334,163474,163490,156676,163614,163721,163749,163798,163890,163911,164246,164309,164315,164331,164339,164347,164383,164412,164824,164823,165031,165129,165254,165266,165268,165559,165564,165798,165803,165813,165968,165985,165988,166047,166063,166082,166147,166188,166201,166209,166214,166219,166222,166228,166248,166266,166276,166281,166307,166367,166406,161821,166532,166538,166550,166570,166619,166635,166660,166666,166670,166674,166677,166695,166698,166722,166763,166825,166841,166845,166890,166901,166918,166932,166971,166985,166989,166996,167008,167012,167048,167283,167303,167313,167708,167913,167931,168061,168096,168182,168230,168233,168269,168324,168352,168565,168854,168872,168883,168899,168904,168909,168913,168930,168937,168943,168960,168965,168968,168992,168995,169022,169051,169055,169057,169061,169076,169084,169097,169123,169134,169137,169142,169149,169161,169165,169174,169190,169199,169212,169215,169216,169224,169230,169238,169240,169247,169259,169271,169282,169285,169298,169306,169314,169317,169321,169324,169327,169330,169348,169352,169353,169357,169361,169362,169366,169378,169384,169402,169421,169426,169439,169446,169459,169461,169473,169487,169513,169516,169518,169519,169521,169535,169559,169564,169567,169571,169572,169583,169604,169611,169614,169619,169621,169623,169628,169635,169641,169652,169686,169688,169695,169706,169720,169744,169747,169749,169778,169800,169878,169930,169967,169994,170023,170637,170707,171000,171116,171141,171237,171248,171252,171343,171348,156694,156697,158105,159176,163327,171472,171541,171591,171659,171679,171855,171993,171996,171998,171999,172007,172233,172517,168315,172708,172927,172938,172940,172944,173099,173106,173207,173384,173511,173634,173722,173893,174021,174210,174433,174434,174435,174436,174437,174438,174441,174442,174444,174445,174447,174448,174573,174579,174594,174762,174764,174767,174769,174835,175104,175114,175175,175180,174599,173171,175750,175753,175758,169226,175830,175850,175905,169082,175768])]
account_invoice = sock.execute_kw(dbname, uid, pwd, 'account.invoice', 'search', [domain])
# account_invoice = sock.execute_kw(dbname, uid, pwd, 'account.invoice', 'search', [[('id','=',102641)]],{'order': 'id DESC'})
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

print("length",len(account_invoice))

####################
#account_invoice = account_invoice[1000:]
#print("\n\n> New length>>>>>>",len(account_invoice))
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
                cogs_mapped_idv18 = 789 #v18
                stock_outputv18 = 728 #v18
                acc_recvbl18 = 581
                acc_payble18 = 516

                cogs_mapped_idv12 = 293 #direct v12
                stock_outputv12 = 5859 # direct v12
                acc_recbl12 = 193 #direct v12
                acc_payble12 = 243
                rec12 = sock.execute_kw(dbname, uid, pwd, 'account.move','search_read', [[('name','=',number18)]], {'fields': ['id']})
                rec12_id = rec12[0]['id'] if rec12[0] else False
                prd =list(prod_id.keys())
                print("product lisr",prod_list)
                # for p in prd:
                #     p_id18 = p
                #     p_id12 = prod_id[p_id18][0]
                #     amlv12 = prod_id[p_id18][1]
                #     rn = get_cogs_price_updates(reslt,rec12_id,cogs_mapped_idv18,stock_outputv18,cogs_mapped_idv12,stock_outputv12,acc_recvbl18,acc_recbl12,acc_payble18,acc_payble12,p_id18,p_id12,amlv12)
                for p in prod_list:
                    p_id18 = p[0]
                    p_id12 = p[1]
                    amlv12 = p[2]
                    #print("product list item>>>>>",p)
                    rn = get_cogs_price_updates(reslt,rec12_id,cogs_mapped_idv18,stock_outputv18,cogs_mapped_idv12,stock_outputv12,acc_recvbl18,acc_recbl12,acc_payble18,acc_payble12,p_id18,p_id12,amlv12)
                # sanitise the records
                data = prod_list
                pair_count = {}
                for item in data:
                    pair = item[:2]  # Extract the first two elements as a tuple
                    if pair in pair_count:
                        pair_count[pair] += 1
                    else:
                        pair_count[pair] = 1
                #print (">>>>>>>>>",pair_count)
                for pair, count in pair_count.items():
                    if count >= 2:
                        # print("\n\n\n\n>>>santise>>",pair,cogs_mapped_idv18,stock_outputv18,reslt),
                        sanitise_line(pair,cogs_mapped_idv18,reslt)
                        sanitise_line(pair,stock_outputv18,reslt)

            #if state18 == 'cancel':
            #    sock18.execute_kw(dbname18, uid18, pwd18, 'account.move', 'action_invoice_cancel', [reslt],{})
        else:
            print (f"\n\n Record existed?\n")
            count +=1


    print ("\n\n\n<<<<<<<<<<<EXisted records >>>>>>>>>>>>",count)

