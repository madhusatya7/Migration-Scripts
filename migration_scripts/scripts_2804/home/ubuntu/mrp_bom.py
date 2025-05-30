import xmlrpc.client as xmlrpclib

# version 12
url_common="http://161.97.148.133/xmlrpc/2/common"
url_object="http://161.97.148.133/xmlrpc/2/object"

sock_common = xmlrpclib.ServerProxy(url_common)
dbname="liverahi"
username="sidmec3"
pwd="sankar123"
uid = sock_common.authenticate(dbname, username, pwd, {})
sock = xmlrpclib.ServerProxy(url_object)

# version 18
url_common18="http://84.235.243.208:8069/xmlrpc/2/common"
url_object18="http://84.235.243.208:8069/xmlrpc/2/object"

sock_common18 = xmlrpclib.ServerProxy(url_common18)
dbname18="alrahi_live_master"
username18="sidmec"
pwd18="RahiSm81o15M1R>"
uid18 = sock_common18.authenticate(dbname18, username18, pwd18, {})
sock18 = xmlrpclib.ServerProxy(url_object18)

def get_mapped_product_tmpls(model,ID):
    product_rec = sock.execute_kw(dbname, uid, pwd, 'product.product', 'search_read',
                              [[('product_tmpl_id', '=', ID)]],
                              {'fields': ['id', 'product_tmpl_id', 'name']})
    if product_rec:
        rst = product_rec[0]['id']
        rec1 = sock18.execute_kw(dbname18, uid18, pwd18, model,'search_read', [[('old_id','=',rst)]], {'fields': ['id','old_id','product_tmpl_id']})
        if rec1:
            rst1 = rec1[0]['product_tmpl_id'][0] if rec1[0]['product_tmpl_id'] else False
            return rst1
        else:
            return False

def get_mapped_rec(model,ID):
    rec = sock18.execute_kw(dbname18, uid18, pwd18, model,'search_read', [[('old_id','=',ID)]], {'fields': ['id','old_id']})
    if rec:
        rst = rec[0]['id']
        return rst
    else:
        return False


bom_rec_env = sock.execute_kw(dbname, uid, pwd, 'mrp.bom', 'search', [[]],{'order':'id DESC'})
print("\n\n\nlength>>>>>",len(bom_rec_env))

bom_rec_env = bom_rec_env[133:]
print("\nNew length>>>>>>>>",len(bom_rec_env))

if len(bom_rec_env)>0:
    for rec in range(0,len(bom_rec_env)):
        obj = {}
        bom_rec = sock.execute_kw(dbname, uid, pwd, 'mrp.bom', 'search_read',[[('id', '=', bom_rec_env[rec])]], {
                                                'fields': ['product_tmpl_id','company_id','product_id','product_qty','code','type','available_in_pos','ready_to_produce','bom_line_ids']})
        if rec not in [11,12,130,131,2,5,10,23]:
            print(f"\nfirst {rec} is :{bom_rec}")

            product_tmpl_id18 = int(bom_rec[0]['product_tmpl_id'][0]) if bom_rec[0]['product_tmpl_id'][0] else False
            pt_tmpl18 = get_mapped_product_tmpls(model='product.product', ID=product_tmpl_id18) if product_tmpl_id18 else False
            product_id18 = int(bom_rec[0]['product_id'][0]) if bom_rec[0]['product_id'] else False
            pr_18 = get_mapped_rec(model='product.product', ID=product_id18) if product_id18 else False
            product_qty18 = bom_rec[0]['product_qty']
            type18 = bom_rec[0]['type']
            company_id = int(bom_rec[0]['company_id'][0])
            company_id18 = get_mapped_rec(model='res.company', ID=company_id) if company_id else False

            if bom_rec and 'bom_line_ids' in bom_rec[0]:
                bom_line_ids18 = bom_rec[0]['bom_line_ids']
                bom_line_rec = sock.execute_kw(dbname, uid, pwd, 'mrp.bom.line', 'search_read',[[('id', 'in', bom_line_ids18)]], {'fields': ['product_id','product_qty','product_uom_id','sequence']})
                line_obj = []

                for b in bom_line_rec:
                    l_pr_18 = b['product_id'][0] if b['product_id'] else False
                    l_product_id18 = get_mapped_rec(model='product.product', ID=l_pr_18)
                    l_product_qty18 = b['product_qty']

                    uom_id = b['product_uom_id'][0] if b['product_uom_id'] else False
                    product_uom_id18 = get_mapped_rec(model='uom.uom', ID=uom_id) if uom_id else False
                    sequence18 = b['sequence']

                    line_obj.append((0, 0, {
                        'product_id':l_product_id18,
                        'product_qty': l_product_qty18,
                        'product_uom_id': product_uom_id18,
                        'sequence':sequence18
                    }))

            record_ID = bom_rec[0]['id']
            # {'old_id':record_ID}
            # 'available_in_pos':available_in_pos18, 'ready_to_produce':ready_to_produce18, 'code':code18,
            create_vals = {'old_id':record_ID,'company_id':company_id18,'product_tmpl_id': pt_tmpl18, 'product_id':pr_18, 'product_qty':product_qty18, 'type':type18, 'bom_line_ids':line_obj}

            print (f"\n\n\n Creation Record {rec} >>>>??????",create_vals)


            rec_is_exist = sock18.execute_kw(dbname18, uid18, pwd18, 'mrp.bom', 'search_read',
                                                                [[('old_id','=',record_ID)]], {'fields': ['id','old_id']})

            if not rec_is_exist:
                result = sock18.execute_kw(dbname18, uid18, pwd18, 'mrp.bom', 'create', [create_vals])
                print("created record>>", result)
            else:
                id = rec_is_exist[0]['id']
                print(f"\n Record existed?\n",id)