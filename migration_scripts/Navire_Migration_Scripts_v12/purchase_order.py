import xmlrpc.client as xmlrpclib



# version 12
url_common = "http://139.185.32.81:9020/xmlrpc/2/common"  # Add Here Navire Ip Server
url_object = "http://139.185.32.81:9020/xmlrpc/2/object"

sock_common = xmlrpclib.ServerProxy(url_common)
dbname = "navire_20"
username = "shaheen@navirelogistics.com"
pwd = "Alpha@2019"
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


def get_mapped_reccords(model, IDS):
    recds = []
    for ID in IDS:
        rec = sock18.execute_kw(dbname18, uid18, pwd18, model, 'search_read', [[('old_id', '=', ID)]],
                                {'fields': ['id', 'old_id']})
        if rec:
            rst = rec[0]['id']
            recds.append(rst)
    return recds
# 15640 fully billed
# 15566 waiting for bill
# 15572 nothing to bill
# domain = [('id','=',15378)]
domain = [('state','in',['draft']),('company_id','=',2)]
purchase_order = sock.execute_kw(dbname, uid, pwd, 'purchase.order', 'search', [domain])

# print(sale_order)
print("length", len(purchase_order))

if len(purchase_order) > 0:
    for rec in range(0, len(purchase_order)):
        res_rec = sock.execute_kw(dbname, uid, pwd, 'purchase.order', 'search_read',
                                  [[('id', '=', purchase_order[rec])]], {
                                      'fields': ['name', 'partner_ref', 'date_order', 'date_planned', 'invoice_status',
                                                 'date_approve', 'partner_id', 'payment_term_id', 'user_id',
                                                 'company_id', 'state','invoice_status']})

        print(f"first {rec} is :{res_rec}")

        name18 = res_rec[0]['name']
        partner_ref18 = res_rec[0]['partner_ref']
        date_order18 = res_rec[0]['date_order']
        date_planned18 = res_rec[0]['date_planned']
        invoice_status18 = res_rec[0]['invoice_status']
        date_approve18 = res_rec[0]['date_approve']
        state18 = res_rec[0]['state']


        # m2O fields
        partner_id = int(res_rec[0]['partner_id'][0])
        partner_id18 = get_mapped_rec(model='res.partner', ID=partner_id)

        user_id = int(res_rec[0]['user_id'][0])
        user_id18 = get_mapped_rec(model='res.users', ID=user_id)

        payment_term_id = int(res_rec[0]['payment_term_id'][0]) if res_rec[0]['payment_term_id'] else False
        payment_term_id18 = get_mapped_rec(model='account.payment.term', ID=payment_term_id) if payment_term_id else False

        company_id = int(res_rec[0]['company_id'][0])
        company_id18 = get_mapped_rec(model='res.company', ID=company_id)

        record_ID = res_rec[0]['id']
        create_vals = {'old_id': record_ID, 'name': name18, 'partner_ref': partner_ref18, 'date_order': date_order18,
                       'date_planned': date_planned18, 'date_approve': date_approve18, 'partner_id': partner_id18,
                       'payment_term_id': payment_term_id18,'user_id': user_id18, 'company_id': company_id18, 'state': state18}

        # print(f"records in {create_vals}")

        # calculate lines
        purchase_order_line = sock.execute_kw(dbname, uid, pwd, 'purchase.order.line', 'search_read',
                                              [[('order_id', '=', record_ID)]], {
                                                  'fields': ['name', 'date_planned', 'qty_invoiced', 'qty_received',
                                                             'product_qty', 'product_id',
                                                             'price_unit', 'company_id', 'account_analytic_id',
                                                             'taxes_id', 'price_subtotal', 'state']})

        line_obj = []
        # print(f"Record Main {rec} >>>>", create_vals)

        for line in purchase_order_line:
            name18 = line['name']
            date_planned18 = line['date_planned']
            qty_invoiced18 = line['qty_invoiced']
            qty_received18 = line['qty_received']
            product_qty18 = line['product_qty']
            price_unit18 = line['price_unit']
            price_subtotal18 = line['price_subtotal']
            state18 = line['state']

            # m2o fields
            product_id = line['product_id'][0]

            product_id18 = get_mapped_rec(model='product.product', ID=product_id)

            # company_id = int(line['company_id'][0])
            # company_id18 = get_mapped_rec(model='res.company', ID=company_id)
            #
            # account_analytic_id = line['account_analytic_id'][0]
            # account_analytic_id18 = get_mapped_rec(model='account.analytic.account', ID=account_analytic_id)

            account_analytic_id = line['account_analytic_id'][0] if line['account_analytic_id'] else False
            if account_analytic_id:
                account_analytic_id18 = get_mapped_rec(model='account.analytic.account', ID=account_analytic_id)
                if account_analytic_id18:
                    analytic_distribution = {
                        str(account_analytic_id18): 100.0
                    }
                else:
                    analytic_distribution = {}
            else:
                analytic_distribution = {}

            # m2m fields
            taxes_id = line['taxes_id']
            taxes_id18 = get_mapped_reccords(model='account.tax', IDS=taxes_id)

            obj = {'name': name18, 'date_planned': date_planned18, 'qty_invoiced': qty_invoiced18,
                   'qty_received': qty_received18, 'product_qty': product_qty18,'analytic_distribution': analytic_distribution,
                   'product_id': product_id18, 'price_unit': price_unit18,

                   'taxes_id': [(6, 0, taxes_id18)], 'price_subtotal': price_subtotal18, 'state': state18}
            # print(f"lines {line} of line {rec} >>>>", obj)
            line_obj.append((0, 0, obj))

        print("line_obj", line_obj)

        # 'account_analytic_id': account_analytic_id,

        create_vals.update({'order_line': line_obj})

        print(f"\n\n\n Creation Record {rec} >>>>??????", create_vals)


        purchase_rec_is_exist = sock18.execute_kw(dbname18, uid18, pwd18, 'purchase.order', 'search_read',
                                                 [[('old_id', '=', record_ID)]], {'fields': ['old_id']})

        if not purchase_rec_is_exist:
            result = sock18.execute_kw(dbname18, uid18, pwd18, 'purchase.order', 'create', [create_vals])
            sock18.execute_kw(dbname18, uid18, pwd18, 'purchase.order', 'write',[[result],{'invoice_status': invoice_status18}])

            print("created record", result)
        else:
            print(f"\n Record existed?\n")


