import xmlrpc.client as xmlrpclib

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

account_tax = sock.execute_kw(dbname, uid, pwd, 'account.tax', 'search', [[('company_id','=',2)]])

print("\n\n\nlength>>>>>",len(account_tax))

if len(account_tax)>0:
    for rec in range(0,len(account_tax)):
        res_rec = sock.execute_kw(dbname, uid, pwd, 'account.tax', 'search_read',[[('id', '=', account_tax[rec])]], {
												'fields': ['name','type_tax_use','amount_type','amount',
                       'account_id','refund_account_id','price_include','description',
                       'company_id','analytic','include_base_amount']})

        print(f"first {rec} is :{res_rec}")
        name18 = res_rec[0]['name']
        type_tax_use18 = res_rec[0]['type_tax_use']
        amount_type18 = res_rec[0]['amount_type']
        amount18 = res_rec[0]['amount']

        account_id = int(res_rec[0]['account_id'][0]) if res_rec[0]['account_id'] else False
        account_id18 = get_mapped_rec(model='account.account', ID=account_id) if account_id else False

        refund_account_id = int(res_rec[0]['refund_account_id'][0]) if res_rec[0]['refund_account_id'] else False
        refund_account_id18 = get_mapped_rec(model='account.account', ID=refund_account_id) if refund_account_id else False
        
        price_include18 = res_rec[0]['price_include']
        description18 = res_rec[0]['description']
        company_id = res_rec[0]['company_id'][0] if res_rec[0]['company_id'] else False
        company_id18 = get_mapped_rec(model='res.company', ID=company_id) if company_id else False

        # analytic18 = res_rec[0]['analytic']
        include_base_amount18 = res_rec[0]['include_base_amount']

        record_ID = res_rec[0]['id']
        price_include_override18 = 'tax_included' if price_include18 else 'tax_excluded'

        create_vals = {'old_id':record_ID,'name':name18,'type_tax_use':type_tax_use18, 'amount_type': amount_type18,'amount': amount18,
                       'price_include_override':price_include_override18,'description':description18,'company_id':company_id18,
                       'include_base_amount':include_base_amount18, 'invoice_repartition_line_ids':[(0,0,{'repartition_type':'tax','account_id':account_id18,'tax_id':[]}),(0,0,{'repartition_type':'base','account_id':False,'tax_id':[]})], 'refund_repartition_line_ids': [(0,0,{'repartition_type':'tax','account_id':refund_account_id18,'tax_id':[]}),(0,0,{'repartition_type':'base','account_id':False,'tax_id':[]})]}
        
        print(f"\n\ncreating records vals in {create_vals}")
            ###########a=tax name should be unique######
        # name wise unique
        ac_rec_is_exist = sock18.execute_kw(dbname18, uid18, pwd18, 'account.tax', 'search_read',[[('name','=',name18)]], {'fields': ['id','old_id','type_tax_use']})
        if not ac_rec_is_exist:
            result = sock18.execute_kw(dbname18, uid18, pwd18, 'account.tax', 'create', [create_vals])
            print("created record>>", result)
        # company wise unique
        ac_rec_cmp_is_exist = sock18.execute_kw(dbname18, uid18, pwd18, 'account.tax', 'search_read',[[('name','=',name18),('company_id','=',company_id18)]], {'fields': ['id','old_id','type_tax_use','company_id']})
        if not ac_rec_cmp_is_exist:
            create_vals['name'] = str(company_id18)+"-" + str(create_vals['name'])
            result = sock18.execute_kw(dbname18, uid18, pwd18, 'account.tax', 'create', [create_vals]) 
        else:
            # for type also
            duplicate_is_exist = sock18.execute_kw(dbname18, uid18, pwd18, 'account.tax', 'search_read',[[('type_tax_use','=',type_tax_use18),('name','=',name18),('company_id','=',company_id18)]], {'fields': ['id','old_id','type_tax_use']})
            if not duplicate_is_exist:
                create_vals['name'] = str(company_id18) +"-" +str(create_vals['name']) + "["+str(type_tax_use18)+"]" 
                result = sock18.execute_kw(dbname18, uid18, pwd18, 'account.tax', 'create', [create_vals])
            else:
                print(f"\n Record existed?\n")
        
print("<<<<<<<<<<<<<<<<<<<<<<<<TAX Creation completed >>>>>>>>>>>>>>>>>??")
