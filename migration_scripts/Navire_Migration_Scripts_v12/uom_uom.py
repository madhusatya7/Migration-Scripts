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
dbname18="navire_prod"
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

# domain = [('id','=',20)]
uom_uom = sock.execute_kw(dbname, uid, pwd, 'uom.uom', 'search', [[]],{'order': 'id DESC'})

print(uom_uom)
print("\n\n\nlength??????",len(uom_uom))

if len(uom_uom)>0:
    for rec in range(0,len(uom_uom)):
        res_rec = sock.execute_kw(dbname, uid, pwd, 'uom.uom', 'search_read',[[('id', '=', uom_uom[rec])]], {
												'fields': ['name','category_id','uom_type','active','rounding']})

        print(f"first {rec} is :{res_rec}")


        name18 = res_rec[0]['name']
        uom_type18 = res_rec[0]['uom_type']
        rounding18 = res_rec[0]['rounding']
        active18 = res_rec[0]['active']

        # # m2O fields
        category_id = int(res_rec[0]['category_id'][0])
        category_id18 = get_mapped_rec(model='uom.category',ID=category_id) if category_id else False

        record_ID = res_rec[0]['id']
        create_vals = {'old_id':record_ID, 'name':name18, 'uom_type':uom_type18, 'rounding':rounding18, 'active':active18,'category_id':category_id18}

        # existing_reference = sock18.execute_kw(
        #     dbname18, uid18, pwd18, 'uom.uom', 'search_read',
        #     [[('category_id', '=', category_id18), ('uom_type', '=', 'reference')]],
        #     {'fields': ['id']}
        # )
        # print(">>>>>>>>>>>>>>>>", existing_reference)

        product_rec_is_exist = sock18.execute_kw(dbname18, uid18, pwd18, 'uom.uom', 'search_read',[[('old_id', '=', record_ID)]], {'fields': ['old_id']})
        if not product_rec_is_exist:
            result = sock18.execute_kw(dbname18, uid18, pwd18, 'uom.uom', 'create', [create_vals])
            print("\n\ncreated record>>>>", result)
        else:
            print(f"\n Record existed?\n")

