import xmlrpc.client as xmlrpclib


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


def get_mapped_rec(model, ID):
    rec = sock18.execute_kw(dbname18, uid18, pwd18, model, 'search_read', [[('old_id', '=', ID)]],
                            {'fields': ['id', 'old_id']})
    if rec:
        rst = rec[0]['id']
        return rst
    else:
        return False


def get_mapped_records(model, IDS):
    recds = []
    for ID in IDS:
        rec = sock18.execute_kw(dbname18, uid18, pwd18, model, 'search_read', [[('old_id', '=', ID)]],
                                {'fields': ['id', 'old_id']})
        if rec:
            rst = rec[0]['id']
            recds.append(rst)
    return recds
# domain = [('id', '=', [3902])]
# domain = [('create_date','>=','2025-03-25 00:00:00')]
account_analytic_account = sock.execute_kw(dbname, uid, pwd, 'account.analytic.account', 'search', [[]], {'order': 'id DESC'})

# print(account_analytic_account)
print("\n\n\nlength??????", len(account_analytic_account))

if len(account_analytic_account) > 0:
    for rec in range(0, len(account_analytic_account)):
        res_rec = sock.execute_kw(dbname, uid, pwd, 'account.analytic.account', 'search_read',
                                  [[('id', '=', account_analytic_account[rec])]], {
                                      'fields': ['name', 'code', 'partner_id','group_id','company_id']})

        print(">>>>>>>>>>>>>>>>>>v12 records>>>>>>>>>>>>>>>>>>>>>>", res_rec)
        print(f"first {rec} is :{res_rec}")

        name18 = res_rec[0]['name']
        code18 = res_rec[0]['code']
        partner_id = res_rec[0]['partner_id'][0] if res_rec[0]['partner_id'] else False
        partner_id18= get_mapped_rec('res.partner', ID=partner_id) if partner_id else False
        # group_id = res_rec[0]['group_id'][0] if res_rec[0]['group_id'] else False
        # group_id18 = get_mapped_rec('account.analytic.group', ID=group_id)

        # if group_id18.start_date or group_id.end_date:
        #     start_date18 = group_id18.start_date
        #     end_date18 = group_id18.end_date
        # else:
        #     start_date18 = False
        #     end_date18 = False

        group_id = res_rec[0]['group_id'][0] if res_rec[0]['group_id'] else False
        start_date18 = False
        end_date18 = False

        if group_id:
            group_rec = sock.execute_kw(dbname, uid, pwd, 'account.analytic.group', 'read', [group_id],
                                        {'fields': ['start_date', 'end_date']})
            if group_rec:
                start_date18 = group_rec[0].get('start_date', False)
                end_date18 = group_rec[0].get('end_date', False)
        plan_id     = 1

        company_id = res_rec[0]['company_id'][0]
        company_id18 = get_mapped_rec('res.company', ID=company_id)


        record_ID = res_rec[0]['id']
        create_vals = {'old_id': record_ID, 'name': name18, 'code': code18,
                       'partner_id': partner_id18,'name': name18,'company_id': company_id18,
                       'start_date': start_date18,'end_date': end_date18,'plan_id': plan_id,
                       }
        print("\n\n>>>>>>>>>>>>>create_vals",create_vals)
        product_rec_is_exist = sock18.execute_kw(dbname18, uid18, pwd18, 'account.analytic.account', 'search_read',
                                                 [[('old_id', '=', record_ID)]],
                                                 {'fields': ['old_id']})
        if not product_rec_is_exist:
            result = sock18.execute_kw(dbname18, uid18, pwd18, 'account.analytic.account', 'create', [create_vals])
            print("\n\ncreated record>>>>", result)
        else:
            print(f"\n Record existed?\n")

