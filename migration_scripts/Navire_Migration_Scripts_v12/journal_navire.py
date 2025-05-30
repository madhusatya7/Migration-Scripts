import xmlrpc.client as xmlrpclib
import random
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
dbname18="navire_0905"
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

domain = ('id','not in',[51,77,72,70,71,116,144,159,140,115,114,42,165,167,174,275,186,185,53,119,122,18,32,138,163,100])
journal = sock.execute_kw(dbname, uid, pwd, 'account.journal', 'search', [[domain]], {'order': 'id DESC'})
print("\n\n\njournal length??????", len(journal))

if len(journal) > 0:
    for rec in range(0, len(journal)):
        res_rec = sock.execute_kw(dbname, uid, pwd, 'account.journal', 'search_read',
                                  [[('id', '=', journal[rec])]], {
                                      'fields': ['name', 'type', 'company_id', 'code', 'default_credit_account_id']})

        print(">>>>>>>>>>>>>>>>>>v12 records>>>>>>>>>>>>>>>>>>>>>>", res_rec)
        print(f"first {rec} is :{res_rec}")

        name18 = res_rec[0]['name']
        type18 = res_rec[0]['type']
        # company_id18 = res_rec[0]['company_id']
        code18 = res_rec[0]['code']
        # default_credit_account_id18 = res_rec[0]['default_credit_account_id']

        #m2o fields
        company_id = int(res_rec[0]['company_id'][0]) if res_rec[0]['company_id'] else False
        company_id18 = get_mapped_rec(model='res.company', ID=company_id) if company_id else False

        default_credit_account_id = int(res_rec[0]['default_credit_account_id'][0]) if res_rec[0]['default_credit_account_id'] else False
        default_credit_account_id18 = get_mapped_rec(model='account.account', ID=default_credit_account_id) if default_credit_account_id else False

        record_ID = res_rec[0]['id']
        
        create_vals = {'old_id': record_ID, 'name': name18,'company_id': company_id18,'default_account_id': default_credit_account_id18,
                        'type':type18,'code':code18,}
        # 'suspence_account_id': 436, 'profit_account_id': 437, 'loss_account_id': 438,

        journal_is_exist = sock18.execute_kw(dbname18, uid18, pwd18, 'account.journal', 'search_read',
                                                 [[('old_id', '=', record_ID)]],
                                                      {'fields': ['old_id']})
        if not journal_is_exist:
            try:
                ##################
                # random_number21 = random.randint(1, 100000)
                # create_vals['code'] = create_vals['code'] + '-' + str(random_number21) +'-' + str(random_number21)
                # ###################
                print("\n\n>>>>>>>>>>>>>create_vals", create_vals)
                result = sock18.execute_kw(dbname18, uid18, pwd18, 'account.journal', 'create', [create_vals])
                print("\n\ncreated record>>>>", result)
            except Exception as e:
                seq_exist = sock18.execute_kw(dbname18, uid18, pwd18, 'account.journal', 'search_read',
                                              [[('code', '=', create_vals['code'])]],
                                              {'fields': ['id']})
                if seq_exist:
                    inc = create_vals['code'].split('-')
                    num = 1
                    if len(inc)>=2:
                        num = int(inc[1])
                        num += 1
                    create_vals['code'] = create_vals['code'] + '-' + str(num)
                    result = sock18.execute_kw(dbname18, uid18, pwd18, 'account.journal', 'create', [create_vals])
                    print(">>>>>>>>>>>>>resequence ")
        else:
            id = journal_is_exist[0]['id']
            print(f"\n Record existed?\n")
            print("UPgrage is >>>>>>>>", id, record_ID)

            # result = sock18.execute_kw(dbname18, uid18, pwd18, 'account.journal', 'write', [[id], {'parent_id':parent_id18}])
            # print(">>>>>>", result)

