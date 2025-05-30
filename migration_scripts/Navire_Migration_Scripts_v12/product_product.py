import xmlrpc.client as xmlrpclib

# version 12
url_common="http://139.185.32.81:9020/xmlrpc/2/common"
url_object="http://139.185.32.81:9020/xmlrpc/2/object"

sock_common = xmlrpclib.ServerProxy(url_common)
dbname="navire_28"
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

def get_mapped_records(model,IDS):
	recds = []
	for ID in IDS:
		rec = sock18.execute_kw(dbname18, uid18, pwd18, model,'search_read', [[('old_id','=',ID)]], {'fields': ['id','old_id']})
		if rec:
			rst = rec[0]['id']
			recds.append(rst)
	return recds
# domain = [('id','=',482)]

domain = [('id','in',[349,162,212])]
product_product = sock.execute_kw(dbname, uid, pwd, 'product.product', 'search', [domain],{'order': 'id DESC'})

# print(product_product)
print("\n\n\nlength??????",len(product_product))

if len(product_product)>0:
    for rec in range(0,len(product_product)):
        res_rec = sock.execute_kw(dbname, uid, pwd, 'product.product', 'search_read',[[('id', '=', product_product[rec])]], {
												'fields': ['name','type','default_code','barcode','lst_price','standard_price'
                                                          ,'invoice_policy','purchase_method','taxes_id','categ_id','company_id',
                                                           'uom_id','uom_po_id','sale_ok','purchase_ok']})

        print(f"first {rec} is :{res_rec}")

        create_vals= {}
        name18 = res_rec[0]['name']
        type18 = res_rec[0]['type'] if res_rec[0]['type'] else False



        default_code18 = res_rec[0]['default_code'] if res_rec[0]['default_code'] else ''
        barcode18=res_rec[0]['barcode'] if res_rec[0]['barcode'] else ''
        lst_price18 = res_rec[0]['lst_price'] if res_rec[0]['lst_price'] else 0
        standard_price18 = res_rec[0]['standard_price'] if res_rec[0]['standard_price'] else 0
        invoice_policy18 = res_rec[0]['invoice_policy']

        purchase_method18 = res_rec[0]['purchase_method'] if res_rec[0]['purchase_method'] else False
        sale_ok18 = res_rec[0]['sale_ok'] if res_rec[0]['sale_ok'] else False
        purchase_ok18 = res_rec[0]['purchase_ok'] if res_rec[0]['purchase_ok'] else False
        # available_in_pos18 = res_rec[0]['available_in_pos'] if res_rec[0]['available_in_pos'] else False



        # # m2O fields
        categ_id = int(res_rec[0]['categ_id'][0])
        categ_id18 = get_mapped_rec(model='product.category',ID=categ_id) if categ_id else False

        company_id= int(res_rec[0]['company_id'][0])
        company_id18 = get_mapped_rec(model='res.company',ID=company_id)

        uom_id = int(res_rec[0]['uom_id'][0])
        uom_id18 = get_mapped_rec(model='uom.uom',ID=uom_id) if uom_id else False
        uom_po_id = int(res_rec[0]['uom_po_id'][0])
        uom_po_id18 = get_mapped_rec(model='uom.uom', ID=uom_po_id) if uom_po_id else False

        #m2m
        taxes_id = res_rec[0]['taxes_id'] if res_rec[0]['taxes_id'] else []
        taxes_id18 = get_mapped_records(model='account.tax', IDS=taxes_id) if taxes_id else False
        # ,'company_id':company_id18
        if type18 == 'consu':
            is_storable = False
            pro_type = 'consu'
            # create_vals.update({'invoice_policy': invoice_policy18})
        if type18 == 'product':
            pro_type = 'consu'
            is_storable = True
            # create_vals.update({'invoice_policy': invoice_policy18})
        if type18 == 'service':
            pro_type = 'service'
            # service_policy = 'delivered_manual'
            # create_vals.update({'service_policy': service_policy})
        # print(">>>>>>>>>>>>",create_vals)

        record_ID = res_rec[0]['id']
        # create_vals.update(
        create_vals = {'old_id':record_ID,'purchase_method' : purchase_method18, 'sale_ok':sale_ok18, 'purchase_ok':purchase_ok18,
                       'name':name18,'type':pro_type,'default_code':default_code18,'barcode':barcode18,
                       'lst_price':lst_price18,'standard_price':standard_price18,'categ_id':categ_id18,'uom_id':uom_id18,
                       'uom_po_id':uom_po_id18 ,'taxes_id':taxes_id18,'company_id':company_id18}
        print("\n\n>>>>>>>>>>>>>.createvasl",create_vals)
        product_rec_is_exist = sock18.execute_kw(dbname18, uid18, pwd18, 'product.product', 'search_read',[[('old_id', '=', record_ID),('barcode','=',barcode18)]], {'fields': ['old_id']})
        if not product_rec_is_exist:
            result = sock18.execute_kw(dbname18, uid18, pwd18, 'product.product', 'create', [create_vals])
            print("\n\ncreated record>>>>", result)
        # else:
        #     print(f"\n Record existed?\n")

        else:
            id = product_rec_is_exist[0]['id']

            print(f"\n Record existed?\n")
            # if not rp_rec_is_exist[0]['old_id']:
            print("UPgrage is >>>>>>>>", id, record_ID)
            result = sock18.execute_kw(dbname18, uid18, pwd18, 'product.product', 'write', [[id], {'taxes_id':taxes_id18}])
            print(">>>>>>", result)

