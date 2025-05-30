# -*- coding: utf-8 -*-

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
pwd18="$idmectech@com"
uid18 = sock_common18.authenticate(dbname18, username18, pwd18, {})
sock18 = xmlrpclib.ServerProxy(url_object18)


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

def get_mapping(model):
    records = sock18.execute_kw(dbname18, uid18, pwd18, model, 'search_read', [
                                [('old_id', '>', 0)]],
                                {'fields': ['old_id'],
                                 'context': {'active_test': False}})
    rec_dict = {rec['old_id']: rec['id'] for rec in records}
    return rec_dict

account_mapping = get_mapping('account.account')
journal_mapping = get_mapping('account.journal')

def create_accounts(v12_company, v18_company, limit):
    model = 'account.account'
    new_records = sock18.execute_kw(
        dbname18, uid18, pwd18, model, 'search_read',
        [[('old_id', '!=', 0), ('company_ids', 'in', v18_company)]],
        {
            'fields': ['old_id'],
            'context': {'active_test': False},
        }
    )
    exist_records = [item['old_id'] for item in new_records if item['old_id']]

    old_records, while_round, offset = True, 0, 0
    while old_records:
        old_records = sock.execute_kw(
            dbname, uid, pwd, model, 'search_read',
            [[('company_id', '=', v12_company)]],
            {
                'fields': ['name', 'code', 'company_id', 'user_type_id', 'reconcile'],
                'context': {'active_test': False},
                'offset': offset,
                'limit': limit,
            }
        )
        vals_list, count = [], 0
        for old_rec in old_records:
            if old_rec['id'] in exist_records:
                continue
            vals = {
                'name': old_rec['name'],
                # 'code': f'{v18_company}{old_rec['code'][2:]}',
                'code': old_rec['code'],
                # 'code': str("23 -"+old_rec['code']),
                'company_ids': [(6, 0, [1])],
                # 'company_ids': [(6, 0, [v18_company])],
                'reconcile': old_rec['reconcile'],
                'account_type': account_type_mapping[old_rec['user_type_id'][0]],
                'old_id': old_rec['id'] 
            }
            count += 1
            # eleiminate the current year earnings
            if old_rec['id'] in [740,2405,3330,6508,2960,2220,2590,2775,3145,3885,925,1665,3515,6240,1110,2035,1295,370,185,555,1480,1850,4070,5507,3700]:
                pass
            else:
                vals_list.append(vals)
            exist_records.append(old_rec['id'])
        print("=============Cureent list=================", count,vals_list)
        if vals_list:
            sock18.execute_kw(
                dbname18, uid18, pwd18, model, 'create',
                [vals_list]
            )
        offset += limit
        while_round += 1
    print("<<<<Done account >>>>>>>>>>>>>")

def create_journals(v12_company, v18_company, limit):
    model = 'account.journal'
    new_records = sock18.execute_kw(
        dbname18, uid18, pwd18, model, 'search_read',
        [[('old_id', '!=', 0), ('company_id', '=', v18_company)]],
        {
            'fields': ['old_id'],
            'context': {'active_test': False},
        }
    )
    exist_records = [item['old_id'] for item in new_records if item['old_id']]
    account_mapping = get_mapping('account.account')

    old_records, while_round, offset = True, 0, 0
    while old_records:
        old_records = sock.execute_kw(
            dbname, uid, pwd, model, 'search_read',
            [[('company_id', '=', v12_company)]],
            {
                'fields': ['name', 'type', 'company_id', 'code', 'default_credit_account_id'],
                'context': {'active_test': False},
                'offset': offset,
                'limit': limit,
            }
        )
        vals_list, count = [], 0
        for old_rec in old_records:
            if old_rec['id'] in exist_records:
                continue
            account_id = old_rec.get('default_credit_account_id') and old_rec.get('default_credit_account_id')[0]
            vals = {
                'name': old_rec['name'] or '',
                # 'name': str("23-"+old_rec['name']) or '',
                'company_id': v18_company,
                'default_account_id': account_mapping.get(account_id, False),
                'type': old_rec['type'],
                'code': old_rec['code'],
                'old_id': old_rec.get('id')
            }
            count += 1
            vals_list.append(vals)
            exist_records.append(old_rec['id'])
        if vals_list:
            sock18.execute_kw(
                dbname18, uid18, pwd18, model, 'create',
                [vals_list]
            )
        offset += limit
        while_round += 1
    print("<<<<<<<<<<<<<journal >>>>>>>>>>>>>> completed.")

def migrate_account_data(v12_company, v18_company):
    limit = 1000
    create_accounts(v12_company, v18_company, limit)
    create_journals(v12_company, v18_company, limit)


#migrate_account_data(14, 12)
#migrate_account_data(4, 3)
#migrate_account_data(13, 11)
# migrate_account_data(18, 16)
# migrate_account_data(26, 23) # No branch code  23 - ALRAHI ROASTERY LLC (AL AIN)
# migrate_account_data(16, 14)
#migrate_account_data(12, 10)
# migrate_account_data(15, 13)
# migrate_account_data(17, 15)
#migrate_account_data(21, 19)

# migrate_account_data(5, 4) # not done 
# migrate_account_data(9, 7)

# migrate_account_data(24, 28)  # need to conform
# migrate_account_data(19, 17)
#migrate_account_data(25, 22)
#migrate_account_data(6, 5)
# migrate_account_data(11, 9)
# migrate_account_data(7, 25)

migrate_account_data(2, 26)

#migrate_account_data(1, 24)
# migrate_account_data(3, 2)
# migrate_account_data(8, 6)
# migrate_account_data(10, 8)
# migrate_account_data(22, 20)
# migrate_account_data(23, 21)
#migrate_account_data(20, 18)
