import xmlrpc.client as xmlrpclib

# from Navire_Migration_Scripts.account_move_script import ref18

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

domain = [('id','=',323148)]

# domain = [('date','>=','2024-01-01'),('date','>=','2024-02-29')]
account_analytic_line = sock.execute_kw(dbname, uid, pwd, 'account.analytic.line', 'search', [domain], {'order': 'id DESC'})

# print(account_analytic_line)
print("\n\n\nlength??????", len(account_analytic_line))

if len(account_analytic_line) > 0:
    for rec in range(0, len(account_analytic_line)):
        res_rec = sock.execute_kw(dbname, uid, pwd, 'account.analytic.line', 'search_read',
                                  [[('id', '=', account_analytic_line[rec])]], {
                                      'fields': ['name', 'ref', 'date','amount','unit_amount','product_id','product_uom_id','partner_id',
                                                 'account_id','company_id','tag_ids','general_account_id','move_id']})

        print(">>>>>>>>>>>>>>>>>>v12 records>>>>>>>>>>>>>>>>>>>>>>", res_rec)
        print(f"first {rec} is :{res_rec}")

        name18 = res_rec[0]['name']
        ref18 = res_rec[0]['ref']
        date18 = res_rec[0]['date']
        amount18 = res_rec[0]['amount']
        unit_amount18 = res_rec[0]['unit_amount']

        #m2o fields
        product_id = res_rec[0]['product_id'][0] if res_rec[0]['product_id'] else False
        product_id18 = get_mapped_rec('product.product', ID=product_id) if product_id else False
        print(">>>>>>>>>>product_id18",product_id18)

        product_uom_id = res_rec[0]['product_uom_id'][0] if res_rec[0]['product_uom_id'] else False
        product_uom_id18 = get_mapped_rec('uom.uom', ID=product_uom_id) if product_uom_id else False

        partner_id = res_rec[0]['partner_id'][0]
        partner_id18 = get_mapped_rec('res.partner', ID=partner_id)

        account_id = res_rec[0]['account_id'][0]
        account_id18 = get_mapped_rec('account.analytic.account', ID=account_id)

        company_id = res_rec[0]['company_id'][0]
        company_id18 = get_mapped_rec('res.company', ID=company_id)

        general_account_id = res_rec[0]['general_account_id'][0]
        general_account_id18 = get_mapped_rec('account.account', ID=general_account_id)

        move_id = res_rec[0]['move_id'][0] if res_rec[0]['move_id'] else False
        move_id18 = get_mapped_rec('account.move.line', ID=move_id) if move_id else False

        print("\n\n\n\n\n",move_id18)


        record_ID = res_rec[0]['id']

        # 'product_id': product_id18,'tag_ids': [(6, 0, tag_ids18),'move_id': move_id
        create_vals = {'old_id': record_ID, 'name': name18,'ref': ref18, 'date': date18, 'amount': amount18,
                          'unit_amount': unit_amount18,'product_uom_id': product_uom_id18,'product_id': product_id18,
                            'partner_id': partner_id18,'account_id': account_id18,'company_id': company_id18,
                            'general_account_id': general_account_id18,'move_line_id':move_id18}

        print("\n\n>>>>>>>>>>>>>create_vals",create_vals)

        product_rec_is_exist = sock18.execute_kw(dbname18, uid18, pwd18, 'account.analytic.line', 'search_read',
                                                 [[('old_id', '=', record_ID)]],
                                                 {'fields': ['old_id']})
        if not product_rec_is_exist:
            result = sock18.execute_kw(dbname18, uid18, pwd18, 'account.analytic.line', 'create', [create_vals])
            print("\n\ncreated record>>>>", result)
        else:
            print(f"\n Record existed?\n")

