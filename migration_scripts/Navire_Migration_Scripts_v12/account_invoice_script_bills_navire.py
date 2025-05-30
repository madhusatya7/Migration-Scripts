import xmlrpc.client as xmlrpclib
from datetime import datetime as dt, timedelta as td




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

# main
# domain = [('journal_id', '=', 10), ('company_id', '=', 2),('date_invoice', '>=', '2024-01-01'),('date_invoice', '<=', '2024-02-29'),('state','not in',['draft','cancel'])]
# domain = [('id','=',48101)]
domain = [('id','=',63124)]
account_invoice = sock.execute_kw(dbname, uid, pwd, 'account.invoice', 'search', [domain], {'order': 'id DESC'})

print("length", len(account_invoice))

####################
# account_invoice = account_invoice[29:]
# print("\n\n> New length>>>>>>",len(account_invoice))
######################

count = 0
if len(account_invoice) > 0:
    for rec in range(0, len(account_invoice)):
        account_invoice_rec = sock.execute_kw(dbname, uid, pwd, 'account.invoice', 'search_read',
                                              [[('id', '=', account_invoice[rec])]], {
                                                  'fields': ['name', 'number', 'date_invoice', 'date', 'date_due','partner_bank_id',
                                                             'reference', 'partner_id', 'partner_shipping_id',
                                                             'payment_term_id', 'user_id', 'currency_id', 'journal_id',
                                                             'company_id','bl_number','container_no','type', 'state','comment','job_number']})
        # print(">>>>>>>>>>>>>>>>",account_invoice_rec[0].get('number'))
        print(f"first {rec} is :{account_invoice_rec}")

        number18 = account_invoice_rec[0]['number'] if account_invoice_rec[0] else ''
        mname18 = account_invoice_rec[0]['name'] if account_invoice_rec[0] else ''
        date_invoice18 = account_invoice_rec[0]['date_invoice']
        date_due18 = account_invoice_rec[0]['date_due'] if account_invoice_rec[0]['date_due'] else dt.now().date().strftime("%Y-%m-%d")
        date18 = account_invoice_rec[0]['date']
        reference18 = account_invoice_rec[0]['reference']
        # ref18 = account_invoice_rec[0]['ref']
        state18 = account_invoice_rec[0]['state']
        comment18 = account_invoice_rec[0]['comment'] if account_invoice_rec[0]['comment'] else False
        bl_number18 = account_invoice_rec[0]['bl_number']
        container_no18 = account_invoice_rec[0]['container_no']

        # m2o field

        job_number = int(account_invoice_rec[0]['job_number'][0]) if account_invoice_rec[0]['job_number'] else False
        job_number18 = get_mapped_rec(model='sale.order', ID=job_number) if job_number else False

        partner_bank_id = int(account_invoice_rec[0]['partner_bank_id'][0] if account_invoice_rec[0]['partner_bank_id'] else False)
        partner_bank_id18 = get_mapped_rec(model='res.partner.bank', ID=partner_bank_id) if partner_bank_id else False

        partner_id = int(account_invoice_rec[0]['partner_id'][0])
        partner_id18 = get_mapped_rec(model='res.partner', ID=partner_id) if partner_id else False

        partner_shipping_id = int(account_invoice_rec[0]['partner_shipping_id'][0] if account_invoice_rec[0][
            'partner_shipping_id'] else False)
        partner_shipping_id18 = get_mapped_rec(model='res.partner',
                                               ID=partner_shipping_id) if partner_shipping_id else False

        payment_term_id = int(account_invoice_rec[0]['payment_term_id'][0]) if account_invoice_rec[0]['payment_term_id'] else False
        invoice_payment_term_id18 = get_mapped_rec(model='account.payment.term', ID=payment_term_id) if payment_term_id else False

        user_id = int(account_invoice_rec[0]['user_id'][0] if account_invoice_rec[0]['user_id'] else 2)
        user_id18 = get_mapped_rec(model='res.users', ID=user_id) if user_id else False

        currency_id18 = 128

        journal_id = int(account_invoice_rec[0]['journal_id'])
        journal_id18 = get_mapped_rec(model='account.journal', ID=journal_id) if journal_id else False

        company_id = int(account_invoice_rec[0]['company_id'][0])
        company_id18 = get_mapped_rec(model='res.company', ID=company_id) if company_id else False

        move_type18 = account_invoice_rec[0]['type'] if account_invoice_rec[0] else 'entry'

        record_ID = account_invoice_rec[0]['id']


        create_vals = {'old_id': record_ID, 'name': number18, 'invoice_date': date_invoice18,'invoice_user_id':user_id18,
                       'date': date18 or dt.now().date().strftime("%Y-%m-%d"), 'invoice_date_due': date_due18,'job_number':job_number18,
                       'ref': reference18,'invoice_payment_term_id':invoice_payment_term_id18,'partner_id': partner_id18,
                       'currency_id': currency_id18, 'journal_id': journal_id18,'partner_bank_id':partner_bank_id18,
                       'company_id': company_id18, 'move_type': move_type18,'narration':comment18,'container_no':container_no18,'bl_number':bl_number18}

        account_invoice_rec_line = sock.execute_kw(dbname, uid, pwd, 'account.invoice.line', 'search_read',
                                                   [[('invoice_id', '=', record_ID)]], {
                                                       'fields': ['name', 'product_id', 'account_id', 'quantity',
                                                                  'uom_id', 'price_unit', 'invoice_line_tax_ids',
                                                                  'discount', 'price_subtotal','account_analytic_id']})

        # print (account_invoice_rec_line)
        line_obj = []

        for line in account_invoice_rec_line:
            name18 = line['name']
            product_id = line['product_id'][0] if line['product_id'] else False

            if not product_id:
                # This is a note line
                obj = {
                    'name': name18,
                    'display_type': 'line_section',  # or 'line_section' if it's a section header
                }
            else:
                product_id18 = get_mapped_rec(model='product.product', ID=product_id) if product_id else False
                account_id = line['account_id'][0]
                account_id18 = get_mapped_rec(model='account.account', ID=account_id) if account_id else False
                quantity18 = line['quantity']
                uom_id = line['uom_id'][0] if line['uom_id'] else False
                uom_id18 = get_mapped_rec(model='uom.uom', ID=uom_id) if uom_id else False
                price_unit18 = line['price_unit']
                invoice_line_tax_ids = line['invoice_line_tax_ids']
                invoice_line_tax_ids18 = get_mapped_reccords(model='account.tax', IDS=invoice_line_tax_ids)
                # invoice_line_tax_ids18 = get_mapped_taxes(IDS=invoice_line_tax_ids)
                discount18 = line['discount']
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


                obj = {'name': name18, 'display_type': 'product', 'product_id': product_id18,
                       'account_id': account_id18, 'quantity': quantity18, 'product_uom_id': uom_id18,
                       'price_unit': price_unit18, 'tax_ids': invoice_line_tax_ids18, 'discount': discount18,
                       'analytic_distribution': analytic_distribution}
            line_obj.append((0, 0, obj))

        create_vals.update({'invoice_line_ids': line_obj})

        print(f"\n\n\n Creation Record {rec} >>>>??????", create_vals)

        rec_is_exitst = sock18.execute_kw(dbname18, uid18, pwd18, 'account.move', 'search_read',
                                          [[('old_id', '=', record_ID)]], {'fields': ['old_id', 'name']})

        if not rec_is_exitst:
            reslt = sock18.execute_kw(dbname18, uid18, pwd18, 'account.move', 'create', [create_vals])
            print('\n created Record in v18>>>>>>>>>', reslt)
            if state18 in ['open', 'in_payment', 'paid']:
                r = sock18.execute_kw(dbname18, uid18, pwd18, 'account.move', 'action_post', [reslt], {})
                print("created record>>>>>>>>>>>", r)
        else:
            print(f"\n\n Record existed?\n")
            count += 1

    print("\n\n\n<<<<<<<<<<<Existed records >>>>>>>>>>>>", count)