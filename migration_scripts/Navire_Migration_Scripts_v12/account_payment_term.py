import xmlrpc.client as xmlrpclib

from livescripts.account_invoice_script_tax1_credit_note_fact import line_obj

# version 12
url_common = "http://139.185.32.81:9020/xmlrpc/2/common"
url_object = "http://139.185.32.81:9020/xmlrpc/2/object"

sock_common = xmlrpclib.ServerProxy(url_common)
dbname = "navire_28"
username = "shaheen@navirelogistics.com"
pwd = "Alpha@2019"
uid = sock_common.authenticate(dbname, username, pwd, {})
sock = xmlrpclib.ServerProxy(url_object)

# version 18
url_common18 = "http://localhost:8017/xmlrpc/2/common"
url_object18 = "http://localhost:8017/xmlrpc/2/object"

sock_common18 = xmlrpclib.ServerProxy(url_common18)
dbname18 = "demo"
username18 = "admin"
pwd18 = "admin"
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


def get_mapped_reccords(model, IDS):
    recds = []
    for ID in IDS:
        rec = sock18.execute_kw(dbname18, uid18, pwd18, model, 'search_read', [[('old_id', '=', ID)]],
                                {'fields': ['id', 'old_id']})
        if rec:
            rst = rec[0]['id']
            recds.append(rst)
    return recds


# domain=[('id','in',[1406])]
account_payment_term = sock.execute_kw(dbname, uid, pwd, 'account.payment.term', 'search', [[]])

# print(res_partner)
print("\n\n\nlength>>>>>", len(account_payment_term))
main_obj = []

if len(account_payment_term) > 0:
    for rec in range(0, len(account_payment_term)):
        res_rec = sock.execute_kw(dbname, uid, pwd, 'account.payment.term', 'search_read',
                                  [[('id', '=', account_payment_term[rec])]], {
                                      'fields': ['name', 'note', 'active']})
        print(">>>>>>>>>>>>>>>>>>v12 records>>>>>>>>>>>>>>>>>>>>>>", res_rec)

        name18 = res_rec[0]['name']
        note18 = res_rec[0]['note']
        active18 = res_rec[0]['active']

        record_ID = res_rec[0]['id']
        create_vals = {'old_id': record_ID, 'name': name18, 'active': active18, 'note': note18}

        print(f"\n\ncreating records vals in {create_vals}")
        account_payment_term_line = sock.execute_kw(dbname, uid, pwd, 'account.payment.term.line', 'search_read',
                                                    [[('id', '=', record_ID)]], {
                                                        'fields': ['value', 'value_amount', 'days', 'option',
                                                                   'day_of_the_month']})

        print(account_payment_term_line)
        line_obj = []

        for vol in account_payment_term_line:
            value_amount18 = vol['value_amount']
            days18 = vol['days'][0]
            option18 = vol['option']

            obj = {'value_amount': value_amount18,
                   'nb_days': days18,
                   'option': option18,
                   }
            line_obj.append((0, 0, obj))

    print(f"lins obj >>>", line_obj)
    create_vals.update({'line_ids': line_obj})

    # print(f"Record {vo} >>>>", create_vals)
    # rp_rec_is_exist = sock18.execute_kw(dbname18, uid18, pwd18, 'account.payment.term', 'search_read',
# 												[[('old_id', '=', record_ID)]], {'fields': ['old_id']})
# if not rp_rec_is_exist:
# 	reslt = sock18.execute_kw(dbname18, uid18, pwd18, 'account.payment.term', 'create', [create_vals])
# else:
# 	print(f"\n\n Record existed?\n")
