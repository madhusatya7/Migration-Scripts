import xmlrpc.client as xmlrpclib

from Navire_Migration_Scripts.purchase_order import date_order18

# version 12
url_common="http://139.185.32.81:9020//xmlrpc/2/common" #Add Here Navire Ip Server
url_object="http://139.185.32.81:9020//xmlrpc/2/object"

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

def get_mapped_rec(model,ID):
	rec = sock18.execute_kw(dbname18, uid18, pwd18, model,'search_read', [[('old_id','=',ID)]], {'fields': ['id','old_id']})
	if rec:
		rst = rec[0]['id']
		return rst
	else:
		return False

def get_mapped_reccords(model,IDS):
	recds = []
	for ID in IDS:
		rec = sock18.execute_kw(dbname18, uid18, pwd18, model,'search_read', [[('old_id','=',ID)]], {'fields': ['id','old_id']})
		if rec:
			rst = rec[0]['id']
			recds.append(rst)
	return recds

#796,14213,18372,1038,14498,16892,19253,-Fully invoiced
# 19114 - To invoice
# domain = [('id','=',19102)]
domain=[('state','in',['draft']),('company_id','=',2)]
sale_order = sock.execute_kw(dbname, uid, pwd, 'sale.order', 'search', [domain])

# print(sale_order)
print("length",len(sale_order))

if len(sale_order)>0:
    for rec in range(0,len(sale_order)):
        res_rec = sock.execute_kw(dbname, uid, pwd, 'sale.order', 'search_read',[[('id', '=', sale_order[rec])]], {
												'fields': ['name','partner_id','payment_term_id','confirmation_date','job_type','job_created_by','picking_policy','user_id','tag_ids','team_id','invoice_status','invoice_ids',
                                                           'pricelist_id','client_order_ref','bl_no','company_id','analytic_account_id','origin','opportunity_id','campaign_id','medium_id','source_id','state','note','validity_date',
                                                           'create_date']})

        print(f"first {rec} is :{res_rec}")
        # print("res_rec",res_rec)

        name18 = res_rec[0]['name']
        date_order18 = res_rec[0]['create_date']
        # print("date_order18",date_order18)
        # name_desc = name18.replace("\n", " ")

        validity_date18 = res_rec[0]['validity_date'] if res_rec[0]['validity_date'] else False
        confirmation_date18 = res_rec[0]['confirmation_date']
        picking_policy18 = res_rec[0]['picking_policy']
        client_order_ref18 = res_rec[0]['client_order_ref']
        bl_no18 = res_rec[0]['bl_no']
        origin18 = res_rec[0]['origin']
        state18 = res_rec[0]['state']
        invoice_status18 = res_rec[0]['invoice_status']

        # print("invoice_status>>>>>>>>>>>>",invoice_status18)

        note18 = res_rec[0]['note'] if res_rec[0]['note'] else False
        # print(">>>>>>>>>>note",note18)

        # m2O fields
        partner_id = int(res_rec[0]['partner_id'][0])
        partner_id18 = get_mapped_rec(model='res.partner',ID=partner_id)

        user_id= int(res_rec[0]['user_id'][0]) if res_rec[0]['user_id'] else False
        user_id18 = get_mapped_rec(model='res.users',ID=user_id) if user_id else False

        payment_term_id = int(res_rec[0]['payment_term_id'][0]) if res_rec[0]['payment_term_id'] else False
        payment_term_id18 = get_mapped_rec(model='account.payment.term',ID=payment_term_id) if payment_term_id else False

        job_type = int(res_rec[0]['job_type'][0]) if res_rec[0]['job_type'] else False
        job_type18 = get_mapped_rec(model='so.job.type', ID=job_type) if job_type else False

        company_id = int(res_rec[0]['company_id'][0]) if res_rec[0]['company_id'] else False
        company_id18 = get_mapped_rec(model='res.company', ID=company_id) if company_id else False

        job_created_by = int(res_rec[0]['job_created_by'][0]) if res_rec[0]['job_created_by'] else False
        job_created_by18 = get_mapped_rec(model='hr.employee', ID=job_created_by) if job_created_by else False


        # job_created_by =1

        pricelist_id = int(res_rec[0]['pricelist_id'][0]) if res_rec[0]['pricelist_id'] else False
        pricelist_id18 = get_mapped_rec(model='product.pricelist', ID=pricelist_id) if pricelist_id else False


        # team_id = int(res_rec[0]['team_id'][0])
        # team_id18 = get_mapped_rec(model='crm.team', ID=team_id)

        analytic_account_id = int(res_rec[0]['analytic_account_id'][0]) if res_rec[0]['analytic_account_id'] else False
        analytic_account_id18 = get_mapped_rec(model='account.analytic.account', ID=analytic_account_id) if analytic_account_id else False
        # get invoice ids
        # invoice_ids = res_rec[0]['invoice_ids'] if res_rec[0]['invoice_ids'] else False
        # invoice_ids18 = get_mapped_reccords(model='account.move', IDS=invoice_ids)

        record_ID = res_rec[0]['id']

        create_vals = {'old_id':record_ID,'name':name18,'date_order':confirmation_date18 or date_order18 ,'picking_policy':picking_policy18,'client_order_ref':client_order_ref18,'bl_no':bl_no18,
                       'origin':origin18,'partner_id':partner_id18,'user_id':user_id18,'company_id':company_id18,
                       'job_type':job_type18,'payment_term_id':payment_term_id18,'state':state18,'analytic_account_id':analytic_account_id18,
                       'job_created_by':job_created_by18,'note':note18,'validity_date':validity_date18,}

        # 'campaign_id': campaign_id18, 'medium_id': medium_id18,'analytic_account_id':analytic_account_id18,pricelist_id':pricelist_id18,
        # 'source_id': source_id18, 'team_id': team_id18, 'opportunity_id': opportunity_id18,'company_id':company_id18,

        print(f"records in {create_vals}")

        # calculate lines
        sale_order_line = sock.execute_kw(dbname, uid, pwd, 'sale.order.line', 'search_read',
                                                   [[('order_id', '=', record_ID)]], {
                                                       'fields': ['product_id','name', 'product_uom_qty','qty_delivered','product_uom'
                                                                  'qty_invoiced', 'price_unit', 'tax_id','price_total','display_type']})


        line_obj = []
        print(f"Record Main {rec} >>>>", create_vals)

        # print(">>>>>>>>>>>>>>",create_vals)

        for line in sale_order_line:
            # display_type18 = line.get('display_type', False)
            #
            # if display_type18 == 'line_note':
            #     name18 = line['name']
            #     obj = {
            #         'name': name18,
            #         'display_type': 'line_note'
            #     }
            #     print("Line Note OBJ >>>>", obj)

            name18 = line['name']
            product_id = line['product_id'][0] if line['product_id'] else False

            if not product_id:
                obj = {
                    'name': name18,
                    'display_type': 'line_note',  # or 'line_section' if it's a section header
                }

            else:
                product_id18 = get_mapped_rec(model='product.product', ID=product_id) if product_id else False
                name18 = line.get('name','')
                product_uom_qty18 = line.get('product_uom_qty', 0.0)
                qty_delivered18 = line['qty_delivered']
                price_unit18 = line.get('price_unit', 0.0)
                tax_id = line['tax_id']
                tax_id18 = get_mapped_reccords(model='account.tax', IDS=tax_id)

                product_uom = line.get('product_uom', False)
                product_uom18 = get_mapped_rec(model='uom.uom', ID=product_uom[0]) if product_uom else False

                price_total18 = line['price_total']



                obj = {'product_id': product_id18,'name': name18,'product_uom_qty':product_uom_qty18,'price_unit': price_unit18,
                   'product_uom':product_uom18,'qty_delivered': qty_delivered18,'tax_id': tax_id18}
            # 'product_uom_qty': product_uom_qty18,'qty_invoiced':qty_invoiced18,'tax_ids': tax_id18,
            # print(f"lines {line} of line {rec} >>>>", obj)
            line_obj.append((0, 0, obj))


        create_vals.update({'order_line': line_obj})

        print (f"\n\n\n Creation Record {rec} >>>>??????",create_vals)


        sale_rec_is_exist = sock18.execute_kw(dbname18, uid18, pwd18, 'sale.order', 'search_read',
                                                         [[('old_id', '=', record_ID)]], {'fields': ['old_id']})


        if not sale_rec_is_exist:
            result = sock18.execute_kw(dbname18, uid18, pwd18, 'sale.order', 'create', [create_vals])
            sock18.execute_kw(dbname18, uid18, pwd18, 'sale.order', 'write',
                              [[result], {'invoice_status': invoice_status18}])
            print("created record", result)
        else:

            print(f"\n Record existed?\n")
