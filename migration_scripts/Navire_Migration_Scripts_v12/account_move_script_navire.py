import xmlrpc.client as xmlrpclib

# import dt

# version 12
url_common = "http://139.185.32.81:9020/xmlrpc/2/common"
url_object = "http://139.185.32.81:9020/xmlrpc/2/object"

sock_common = xmlrpclib.ServerProxy(url_common)
dbname = "navire_20"
username = "shaheen@navirelogistics.com"
pwd = "Alpha@2019"
uid = sock_common.authenticate(dbname, username, pwd, {})
sock = xmlrpclib.ServerProxy(url_object)

# version 18
url_common18 = "http://139.185.58.40:8069/xmlrpc/2/common"
url_object18 = "http://139.185.58.40:8069/xmlrpc/2/object"

sock_common18 = xmlrpclib.ServerProxy(url_common18)
dbname18 = "navire_prod2"
username18 = "admin"
pwd18 = "admin"
uid18 = sock_common18.authenticate(dbname18, username18, pwd18, {})
sock18 = xmlrpclib.ServerProxy(url_object18)

existing_records = []


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


e_jrnl = []
# eliminate vendor bills


ej_14 = [14,10,9]

# domain = [('company_id','=',2),('journal_id','not in', ej_14),('state','not in',['draft'])]
#Direct entries 1188,1189,5767,86728,86724,86729,86844,86665,86704,89167,89165,89156,89133,89125
#89124,89164,89163,89132,110045,128055,139293,139295,139294,139495,139514,139296,115204
domain = [('id', 'in', [86731])]
account_move = sock.execute_kw(dbname, uid, pwd, 'account.move', 'search', [domain], {'order': 'id DESC'})
# print(account_move)
print("\n\n>>>>>Total length", len(account_move))

##############################
# account_move = account_move[7900:]
# print("\nNew length>>>>>>>>",len(account_move))
###########################

if len(account_move) > 0:
    for rec in range(0, len(account_move)):
        account_move_rec = sock.execute_kw(dbname, uid, pwd, 'account.move', 'search_read',
                                           [[('id', '=', account_move[rec])]], {
                                               'fields': ['name', 'ref', 'date', 'state', 'journal_id', 'company_id',
                                                          'currency_id', 'narration']})

        print("\nCurrent record>>>>>>>", account_move[rec], account_move_rec)
        name18 = account_move_rec[0]['name']
        ref18 = account_move_rec[0]['ref']
        date18 = account_move_rec[0]['date']
        state18 = account_move_rec[0]['state']
        # m2o field
        journal_id = int(account_move_rec[0]['journal_id'][0] if account_move_rec[0]['journal_id'] else False)
        journal_id18 = get_mapped_rec(model='account.journal', ID=journal_id) if journal_id else False

        currency_id18 = 128
        company_id = int(account_move_rec[0]['company_id'][0])
        company_id18 = get_mapped_rec(model='res.company', ID=company_id) if company_id else False
        narration18 = account_move_rec[0]['narration'] or ''

        record_ID = account_move_rec[0]['id']

        create_vals = {'old_id1': record_ID, 'auto_post': 'no', 'date': date18, 'move_type': 'entry', 'name': name18,
                       'ref': ref18, 'date': date18, 'currency_id': currency_id18, 'journal_id': journal_id18,
                       'company_id': company_id18, 'narration': narration18}

        # calculate lines
        account_move_rec_line = sock.execute_kw(dbname, uid, pwd, 'account.move.line', 'search_read',
                                                [[('move_id', '=', record_ID)]], {
                                                    'fields': ['name', 'partner_id', 'account_id', 'debit', 'credit',
                                                               'amount_currency', 'currency_id', 'tax_ids']})

        line_obj = []
        for line in account_move_rec_line:
            lid = line['id']
            lname18 = line['name']
            debit18 = line['debit']
            credit18 = line['credit']
            amount_currency18 = line['amount_currency']
            partner_id = line['partner_id'][0] if line['partner_id'] else False
            partner_id18 = get_mapped_rec(model='res.partner', ID=partner_id) if partner_id else False

            # currency_id = line['currency_id'][0]
            # lcurrency_id18 = get_mapped_rec(model='res.currency', ID=currency_id)
            lcurrency_id18 = 128

            if debit18:
                amount_currency18 = debit18
            if credit18:
                amount_currency18 = -credit18

            # eliminate current year earnings
            account_id = line['account_id'][0]
            if account_id in [370]:
                account_id18 = 595
            else:
                account_id18 = get_mapped_rec(model='account.account', ID=account_id) if account_id else False
            # 625
            # 'tax_ids':tax_ids18
            obj = {'old_id1': lid, 'name': lname18, 'debit': debit18, 'credit': credit18,
                   'amount_currency': amount_currency18, 'partner_id': partner_id18, 'account_id': account_id18,
                   'currency_id': lcurrency_id18}
            line_obj.append((0, 0, obj))

        create_vals.update({'line_ids': line_obj})

        print("\n\n\nCreating Record in v18 {} $$$$$$$$>>>>??", rec)
        try:
            account_move_rec_exist = sock18.execute_kw(dbname18, uid18, pwd18, 'account.move', 'search_read',
                                                       [[('old_id1', '=', record_ID)]], {'fields': ['old_id1', 'name']})
            if not account_move_rec_exist:
                # same_name_rec_exist = sock18.execute_kw(dbname18, uid18, pwd18, 'account.move','search_read', [[('name','=',create_vals['name'])]], {'fields': ['name']})
                # if not same_name_rec_exist:
                result = sock18.execute_kw(dbname18, uid18, pwd18, 'account.move', 'create', [create_vals])
                print("\n\n>> created record", result)
                if state18 == 'posted' and create_vals['line_ids'] != []:
                    sock18.execute_kw(dbname18, uid18, pwd18, 'account.move', 'action_post', [result], {})
                # commented because multiples came
                # else:
                #     print(">>>>>>>>same  name record existed >>>>>>>>>>>>>>>>",create_vals)
                #     create_vals['name'] = str(create_vals['name']) + 'append v18'
                #     existing_records.append(create_vals)
                #     result1 =sock18.execute_kw(dbname18, uid18, pwd18, 'account.move','create', [create_vals])
                #     if state18 == 'posted' and create_vals['line_ids']!= []:
                #         sock18.execute_kw(dbname18, uid18, pwd18, 'account.move', 'action_post', [result1],{})
            else:
                print(f"\n Record existed?\n\n")
        except Exception as e:
            print(f">>>>>>>>>Error processing record {account_move_rec[0]['name']}: {e}>>>>>>>>>>>>>>>>")

    print("<<<??Exisitng records>>>>>", existing_records)
