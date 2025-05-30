import xmlrpc.client as xmlrpclib

# version 12
url_common = "http://161.97.148.133/xmlrpc/2/common"
url_object = "http://161.97.148.133/xmlrpc/2/object"

sock_common = xmlrpclib.ServerProxy(url_common)
dbname = "liverahi"
username = "sidmec3"
pwd = "sankar123"
uid = sock_common.authenticate(dbname, username, pwd, {})
sock = xmlrpclib.ServerProxy(url_object)

# version 18
url_common18 = "http://localhost:8069/xmlrpc/2/common"
url_object18 = "http://localhost:8069/xmlrpc/2/object"

sock_common18 = xmlrpclib.ServerProxy(url_common18)
dbname18 = "alrahi_live_master"
username18 = "sidmec"
pwd18 = "RahiSm81o15M1R>"
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
# domain = [('id','in',[39115,83,1754,1789])]
domain = [('create_date','>=','2025-03-20')]
vansale_order = sock.execute_kw(dbname, uid, pwd, 'van.sale.order', 'search', [domain],{'order': 'id DESC'})
#vansale_order = vansale_order[5500:]
#vansale_order = vansale_order[10500:]
print(">>>>>>>>>>>>>>>>>>>>>length>>>>>>",vansale_order)
if len(vansale_order) > 0:
    for vo in range(0, len(vansale_order)):
        print(vo)
        create_vals = {}
        vansale_order_rec = sock.execute_kw(dbname, uid, pwd, 'van.sale.order', 'search_read',
                                            [[('id', '=', vansale_order[vo])]], {
                                                'fields': ['name', 'partner_id', 'price_list', 'company_id', 'user_id',
                                                           'invoice_id', 'payment_journal_id', 'date_order', 'origin',
                                                           'payment_id', 'state', 'currency_id', 'old_id']})
        print("\nvansales v12 main>>>>>", vansale_order_rec)

        partner_id = int(vansale_order_rec[0]['partner_id'][0])
        company_id = int(vansale_order_rec[0]['company_id'][0])
        price_list = vansale_order_rec[0]['price_list']
        user_id = int(vansale_order_rec[0]['user_id'][0]) if vansale_order_rec[0]['user_id'] else False
        #invoice_id = int(vansale_order_rec[0]['invoice_id'][0])
        # currency_id = int(vansale_order_rec[0]['currency_id'][0])
        partner_id18 = get_mapped_rec(model='res.partner', ID=partner_id)
        company_id18 = get_mapped_rec(model='res.company', ID=company_id)
        user_id18 = get_mapped_rec(model='res.users', ID=user_id)
        # invoice_id18 = get_mapped_rec(model='account.move', ID=invoice_id)
        # currency_id18 = get_mapped_rec(model='res.currency', ID=currency_id)
        
        inv_id =  False
        if vansale_order_rec[0]['invoice_id']:
            invoice_id = int(vansale_order_rec[0]['invoice_id'][0])
            inv_rec = sock18.execute_kw(dbname18, uid18, pwd18, 'account.move', 'search_read', 
                                            [[('old_id', '=', invoice_id)]], {
                                                'fields': ['id', 'name', 'old_id']})
            inv_id = int(inv_rec[0]['id']) if inv_rec else False

        payment_journal_id18 = vansale_order_rec[0]['payment_journal_id']
        date_order18 = vansale_order_rec[0]['date_order']
        payment_id18 = vansale_order_rec[0]['payment_id']
        origin18 = vansale_order_rec[0]['origin']
        state18 = vansale_order_rec[0]['state']
        name18 = vansale_order_rec[0]['name']

        user_name18 = vansale_order_rec[0]['user_id'][1] if vansale_order_rec[0]['user_id'] else ''
        user_temp_id18 = vansale_order_rec[0]['user_id'][0] if vansale_order_rec[0]['user_id'] else False
 
        if price_list:
            price_list_id = int(vansale_order_rec[0]['price_list'][0])
            price_list18 = get_mapped_rec(model='product.pricelist', ID=price_list_id)
        else:
            price_list18 = False

        price_list_id = 403

        rec_ID = vansale_order_rec[0]['id']
        create_vals = {'old_id': rec_ID, 'partner_id': partner_id18, 'name': name18, 'price_list': price_list18,
                       'company_id': company_id18, 'user_id': user_id18, 'payment_journal_id': payment_journal_id18,
                       'date_order': date_order18, 'payment_id': payment_id18, 'origin': origin18, 'state': state18, \
                        'user_temp_id' : user_temp_id18, 'user_name':user_name18,'invoice_id':inv_id}

        # calculate lines
        vansale_orderline_rec = sock.execute_kw(dbname, uid, pwd, 'van.sale.order.line', 'search_read',
                                                [[('order_id', '=', rec_ID)]], {
                                                    'fields': ['name', 'product_id', 'product_qty', 'product_uom',
                                                               'price_unit', 'tax_ids', 'price_tax', 'price_subtotal']})


        line_obj = []
        for vol in vansale_orderline_rec:
            obj = {}
            # print(vol)
            lname18 = vol['name']
            product_id = vol['product_id'][0]
            product_id18 = get_mapped_rec(model='product.product', ID=product_id)
            product_qty18 = vol['product_qty']
            product_uom = vol['product_uom'][0]
            product_uom18 = get_mapped_rec(model='uom.uom', ID=product_uom)
            price_unit18 = vol['price_unit']
            tax_ids = vol['tax_ids']
            # tax_ids18 = get_mapped_reccords(model='account.tax', ID=tax_ids)
            price_tax18 = vol['price_tax']
            price_subtotal18 = vol['price_subtotal']

            # related fields
            lstate18 = state18
            # currency_id18 = currency_id18
            lpartner_id18 = partner_id18
            ldate_order18 = date_order18
            lcompany_id18 = company_id18

            #if 41 in tax_ids:
            tax_ids18 = [1203]

            obj = {'name': lname18,
                   'product_id': product_id18,
                   'product_qty': product_qty18,
                   'product_uom': product_uom18,
                   'price_unit': price_unit18,
                   'tax_ids':[(6,0,tax_ids18)],
                   'price_tax': price_tax18,
                   'price_subtotal': price_subtotal18,
                   'state': lstate18,
                   'partner_id': lpartner_id18,
                   'date_order': ldate_order18,
                   'company_id': lcompany_id18
                   }
            print(f"\n\n\nlines {vol} of line {vo} >>>>", obj)
            line_obj.append((0, 0, obj))

        # print(f"lins obj >>>", line_obj)
        create_vals.update({'order_line': line_obj})

        print(f"\n\n\nRecord {vo} >>>>", create_vals)

        vansale_order_rec_is_exitst = sock18.execute_kw(dbname18, uid18, pwd18, 'van.sale.order', 'search_read',
                                                        [[('old_id', '=', rec_ID)]], {'fields': ['old_id']})
        if not vansale_order_rec_is_exitst:
            if not create_vals['old_id'] in [37452,] :
                reslt = sock18.execute_kw(dbname18, uid18, pwd18, 'van.sale.order', 'create', [create_vals])
        else:
            print(f"\n\n Record existed?\n")
