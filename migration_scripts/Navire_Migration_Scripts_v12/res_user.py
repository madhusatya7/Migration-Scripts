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
url_common18="http://localhost:8018/xmlrpc/2/common"
url_object18="http://localhost:8018/xmlrpc/2/object"

sock_common18 = xmlrpclib.ServerProxy(url_common18)
dbname18="trail"
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


domain=[('id','in',[29])]
res_users = sock.execute_kw(dbname, uid, pwd, 'res.users', 'search', [domain])

print(res_users)
print("length>>>>>>>>>>>>>",len(res_users))

if len(res_users)>0:
    for rec in range(0,len(res_users)):
        res_rec = sock.execute_kw(dbname, uid, pwd, 'res.users', 'search_read',[[('id', '=', res_users[rec])]], {
												'fields': ['name','login','company_ids','lang','company_id','tz','signature','action_id','partner_id']})

        print(f"first {rec} is :{res_rec}")

        login18 = res_rec[0]['login']
        name18 = res_rec[0]['name'] #Doubt
        # image18 = res_rec[0]['image']
        lang18 = 'en_US'
        tz18 = res_rec[0]['tz']

       # m2O fields
       #  company_id = int(res_rec[0]['company_id'][0])
       #  company_id18 = get_mapped_rec(model='res.company',ID=company_id)

        partner_id = int(res_rec[0]['partner_id'][0])
        partner_id18 = get_mapped_rec(model='res.partner', ID=partner_id)

        # action_id= int(res_rec[0]['action_id'][0])
        # action_id18 = get_mapped_rec(model='ir.actions.actions',ID=action_id)

        # m2m fields
        # company_ids = res_rec[0]['company_ids']
        # company_ids18 =get_mapped_reccords(model='res.company',IDS=company_ids)

        # 'image_1920':image18,
        record_ID = res_rec[0]['id']
        create_vals = {'old_id':record_ID,'password':'1234','login':login18,'name':name18,'tz':tz18,'lang':lang18,
					   'partner_id':partner_id18}

        print(f"\n\n\ncreating records vals in {create_vals}")

        rec_is_exist = sock18.execute_kw(dbname18, uid18, pwd18, 'res.users', 'search_read',
                                                         [[('old_id', '=', record_ID)]], {'fields': ['old_id']})

        if not rec_is_exist:
            same_login_rec_exist = sock18.execute_kw(dbname18, uid18, pwd18, 'res.users','search_read', [[('login','=',create_vals['login'])]], {'fields': ['login']})
            if not same_login_rec_exist:
                result = sock18.execute_kw(dbname18, uid18, pwd18, 'res.users', 'create', [create_vals])
                print("created record", result)
            else:
                print(">>>>>>>>same  name record existed >>>>>>>>>>>>>>>>",create_vals)
                create_vals['login'] = str(create_vals['login']) + '_v12'
                result1 = sock18.execute_kw(dbname18, uid18, pwd18, 'res.users', 'create', [create_vals])
        else:
            print(f"\n Record existed?\n")
