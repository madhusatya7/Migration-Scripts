import xmlrpc.client as xmlrpclib

from odoo.osv.expression import is_false

# version 12
url_common="http://139.185.32.81:9020/xmlrpc/2/common"
url_object="http://139.185.32.81:9020/xmlrpc/2/object"

sock_common = xmlrpclib.ServerProxy(url_common)
dbname="navire_20"
username="shaheen@navirelogistics.com"
pwd="Alpha@2019"
uid = sock_common.authenticate(dbname, username, pwd, {})
sock = xmlrpclib.ServerProxy(url_object)

# version 18
url_common18="http://139.185.58.40:8069/xmlrpc/2/common"
url_object18="http://139.185.58.40:8069/xmlrpc/2/object"

sock_common18 = xmlrpclib.ServerProxy(url_common18)
dbname18="navire_prod2"
username18="admin"
pwd18="admin"
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

# domain=[('id','=',[7,301,304,301,311,295,702,532,1765,1261])]
domain=[('id','=',[1950])]
res_partner = sock.execute_kw(dbname, uid, pwd, 'res.partner', 'search', [domain])



#print(res_partner)
print("\n\n\nlength>>>>>",len(res_partner))
main_obj = []

if len(res_partner)>0:
    for rec in range(0,len(res_partner)):
        res_rec = sock.execute_kw(dbname, uid, pwd, 'res.partner', 'search_read',[[('id', '=', res_partner[rec])]], {
												'fields': ['company_type','name','street','street2','city','country_id','vat','function','phone','mobile',
                                                           'email','website','lang','company_id','property_account_receivable_id','property_account_payable_id','active',
                                                           'property_payment_term_id','property_supplier_payment_term_id','user_id','state_id','country_id']})
        print(">>>>>>>>>>>>>>>>>>v12 records>>>>>>>>>>>>>>>>>>>>>>",res_rec)

        print(f"first {rec} is :{res_rec}")
        company_type18 = res_rec[0]['company_type']
        print(".............",company_type18)
        name18 = res_rec[0]['name']
        street218 = res_rec[0]['street2']
        city18 = res_rec[0]['city']
        street18 = res_rec[0]['street']
        vat18 = res_rec[0]['vat']
        function18 = res_rec[0]['function']
        phone18 = res_rec[0]['phone']
        mobile18 = res_rec[0]['mobile']
        email18 = res_rec[0]['email']
        website18 = res_rec[0]['website']
        lang18 = res_rec[0]['lang']
        active18 = res_rec[0]['active']

        # m2O fields
        # title = int(res_rec[0]['title'][0])
        # title18 = get_mapped_rec(model='res.partner.title',ID=title)

        company_id = int(res_rec[0]['company_id'][0]) if res_rec[0]['company_id'] else False
        company_id18 = get_mapped_rec(model='res.company',ID=company_id) if company_id else False

        country_id = int(res_rec[0]['country_id'][0]) if res_rec[0]['country_id'] else False
        country_id18 = get_mapped_rec(model='res.country',ID=country_id) if country_id else False

        user_id= int(res_rec[0]['user_id'][0]) if res_rec[0]['user_id'] else False
        user_id18 = get_mapped_rec(model='res.users',ID=user_id) if user_id else False

        property_payment_term_id = int(res_rec[0]['property_payment_term_id'][0]) if res_rec[0]['property_payment_term_id'] else False
        property_payment_term_id18 = get_mapped_rec(model='account.payment.term',ID=property_payment_term_id) if property_payment_term_id else False


        state_id = int(res_rec[0]['state_id'][0]) if res_rec[0]['state_id'] else False
        state_id18 = get_mapped_rec(model='res.country.state',ID=state_id) if state_id else False


        # property_product_pricelist = int(res_rec[0]['property_product_pricelist'][0])
        # property_product_pricelist18 = get_mapped_rec(model='product.pricelist', ID=property_product_pricelist)


        # property_stock_customer = int(res_rec[0]['property_stock_customer'][0])
        # property_stock_customer18 = get_mapped_rec(model='stock.location', ID=property_stock_customer)

        # property_stock_supplier = int(res_rec[0]['property_stock_supplier'][0])
        # property_stock_supplier18 = get_mapped_rec(model='stock.location', ID=property_stock_supplier)

        # property_account_position_id = int(res_rec[0]['property_account_position_id'][0])
        # property_account_position_id18 = get_mapped_rec(model='account.fiscal.position', ID=property_account_position_id)

        property_supplier_payment_term_id = int(res_rec[0]['property_supplier_payment_term_id'][0]) if res_rec[0]['property_supplier_payment_term_id'] else False
        property_supplier_payment_term_id18 = get_mapped_rec(model='account.payment.term', ID=property_supplier_payment_term_id) if property_supplier_payment_term_id else False




        # property_purchase_currency_id = int(res_rec[0]['property_purchase_currency_id'][0])
        # property_purchase_currency_id18 = get_mapped_rec(model='res.currency', ID=property_purchase_currency_id)

        property_account_receivable_id = int(res_rec[0]['property_account_receivable_id'][0])
        property_account_receivable_id18 = get_mapped_rec(model='account.account', ID=property_account_receivable_id)

        property_account_payable_id = int(res_rec[0]['property_account_payable_id'][0])
        property_account_payable_id18 = get_mapped_rec(model='account.account', ID=property_account_payable_id)

		# 'property_stock_customer18':property_stock_customer18 ,'property_stock_supplier':property_stock_supplier18 ,'property_supplier_payment_id':property_supplier_payment_id18,
		# 'property_purchase_currency_id18':property_supplier_payment_id18,'message_bounce':message_bounce18,'bank_id':bank_id18,'category_id':category_id18,'property_account_position_id':property_purchase_currency_id,
        record_ID = res_rec[0]['id']
		# # 'image_1920':image18,'company_id':company_id18 ,
        create_vals = {'old_id': record_ID, 'name': name18, 'company_type': company_type18, 'vat': vat18,
                       'function': function18, 'phone': phone18,'user_id':user_id18,
                       'mobile': mobile18, 'email': email18, 'website': website18, 'lang': lang18, 'street': street18,
                       'property_account_receivable_id': property_account_receivable_id18,
                       'property_account_payable_id': property_account_payable_id18,'company_id':company_id18,
                       'property_payment_term_id':property_payment_term_id18,'property_supplier_payment_term_id':property_supplier_payment_term_id18,'active':active18,
                       'city':city18,'street2':street218,'country_id':country_id18,'state_id':state_id18}


        print(f"\n\ncreating records vals in {create_vals}")

        rp_rec_is_exist = sock18.execute_kw(dbname18, uid18, pwd18, 'res.partner', 'search_read',
                                                            [[('old_id', '=', record_ID), ('name', '=', name18)]],
                                                            {'fields': ['old_id']})

        if not rp_rec_is_exist:
            result = sock18.execute_kw(dbname18, uid18, pwd18, 'res.partner', 'create', [create_vals])
            print("created record>>", result)
        else:
            id = rp_rec_is_exist[0]['id']
            print(f"\n Record existed?\n")
            #if not rp_rec_is_exist[0]['old_id']:
            print ("UPgrage is >>>>>>>>",id,record_ID)
            result = sock18.execute_kw(dbname18, uid18, pwd18, 'res.partner', 'write', [[id],{'old_id':record_ID}])
            print(">>>>>>",result)

