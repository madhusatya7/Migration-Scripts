import xmlrpc.client as xmlrpclib
import random

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

account_type_mapping = {
    1: 'asset_receivable',
    3: 'asset_cash',
    5: 'asset_current',
    6: 'asset_non_current',
    7: 'asset_prepayments',
    8: 'asset_fixed',
    2: 'liability_payable',
    4: 'liability_credit_card',
    9: 'liability_current',
    10: 'liability_non_current',
    11: 'equity',
    12: 'equity_unaffected',
    14: 'income',
    13: 'income_other',
    16: 'expense',
    15: 'expense_depreciation',
    17: 'expense_direct_cost',
}

domain = ('id','in',[417,418,419,420,421,423,424,425,966,968,969,970,971,972,973,974,975])
account = sock.execute_kw(dbname, uid, pwd, 'account.account', 'search', [[domain]], {'order': 'id DESC'})
print("\n\n\naccount length??????", len(account))

if len(account) > 0:
    for rec in range(0, len(account)):
        res_rec = sock.execute_kw(dbname, uid, pwd, 'account.account', 'search_read',
                                  [[('id', '=', account[rec])]], {
                                      'fields': ['name', 'code', 'company_id', 'user_type_id', 'reconcile']})

        print(">>>>>>>>>>>>>>>>>>v12 records>>>>>>>>>>>>>>>>>>>>>>", res_rec)
        print(f"first {rec} is :{res_rec}")

        name18 = res_rec[0]['name']
        # type18 = res_rec[0]['type']
        code18 = res_rec[0]['code']
        user_type_id18 = account_type_mapping[res_rec[0]['user_type_id'][0]]
        reconcile18 = res_rec[0]['reconcile']

        #m2o fields
        company_id = int(res_rec[0]['company_id'][0]) if res_rec[0]['company_id'] else False
        company_id18 = get_mapped_rec(model='res.company', ID=company_id) if company_id else False

        record_ID = res_rec[0]['id']

        create_vals = {'old_id': record_ID, 'name': name18,'company_ids': [(6, 0, [company_id18])],
                       'reconcile': reconcile18,'account_type':user_type_id18,'code':code18}

        account_is_exist = sock18.execute_kw(dbname18, uid18, pwd18, 'account.account', 'search_read',
                                                 [[('old_id', '=',record_ID )]],
                                                      {'fields': ['old_id']})
        if create_vals['code'] not in ['100001','101001','105001','999999']:
            if not account_is_exist:
                try:
                    print("\n\n>>>>>>>>>>>>>create_vals", create_vals)
                    result = sock18.execute_kw(dbname18, uid18, pwd18, 'account.account', 'create', [create_vals])
                    print("\n\ncreated record>>>>", result)
                except Exception as e:
                    print(f"Error creating account: {e}")
            else:
                id = account_is_exist[0]['id']
                print(f"\n Record existed?\n")
                print("UPgrage is >>>>>>>>", id, record_ID)
                write_vals = {'old_id': record_ID, 'name': name18, 'company_ids': [(6, 0, [company_id18])],
                               'reconcile': reconcile18, 'account_type': user_type_id18,
                               'code': code18}
                del write_vals["code"]
                print(write_vals)
                print(">>>>>>", write_vals)
                result = sock18.execute_kw(dbname18, uid18, pwd18, 'account.account', 'write', [[id], write_vals])


