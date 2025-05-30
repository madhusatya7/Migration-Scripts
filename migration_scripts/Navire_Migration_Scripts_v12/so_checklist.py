import xmlrpc.client as xmlrpclib


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

domain = [('id','=',519),('state','in',['validate'])]
so_checklist = sock.execute_kw(dbname, uid, pwd, 'so.checklist', 'search', [domain], {'order': 'id DESC'})

# print(so_checklist)
print("\n\n\nlength??????", len(so_checklist))

if len(so_checklist) > 0:
    for rec in range(0, len(so_checklist)):
        res_rec = sock.execute_kw(dbname, uid, pwd, 'so.checklist', 'search_read',
                                  [[('id', '=', so_checklist[rec])]], {
                                      'fields': ['sale_order_id','so_date','so_partner','eta','free_time',
                                                 'bl_status','do','demmurage','job_type','bl_number','container_no',
                                                 'invoice_doc','pack_list_doc','certificate_origin_doc','bl_awb_doc',
                                                 'phyto_certificate_doc','health_certificate_doc','state']})

        # print(">>>>>>>>>>>>>>>>>>v12 records>>>>>>>>>>>>>>>>>>>>>>", res_rec)
        print(f"first {rec} is :{res_rec}")

        so_date18 = res_rec[0]['so_date']
        eta18 = res_rec[0]['eta']
        free_time18 = res_rec[0]['free_time']
        bl_status18 = res_rec[0]['bl_status']
        do18 = res_rec[0]['do']
        demmurage18 = res_rec[0]['demmurage']
        bl_number18 = res_rec[0]['bl_number']
        container_no18 = res_rec[0]['container_no']
        invoice_doc18 = res_rec[0]['invoice_doc']
        pack_list_doc18 = res_rec[0]['pack_list_doc']
        certificate_origin_doc18 = res_rec[0]['certificate_origin_doc']
        bl_awb_doc18 = res_rec[0]['bl_awb_doc']
        phyto_certificate_doc18 = res_rec[0]['phyto_certificate_doc']
        health_certificate_doc18 = res_rec[0]['health_certificate_doc']
        state18 = res_rec[0]['state']

        sale_order_id = int(res_rec[0]['sale_order_id'][0]) if res_rec[0]['sale_order_id'] else False
        sale_order_id18 = get_mapped_rec(model='sale.order', ID=sale_order_id) if sale_order_id else False

        so_partner = int(res_rec[0]['so_partner'][0]) if res_rec[0]['so_partner'] else False
        so_partner18 = get_mapped_rec(model='res.partner', ID=so_partner) if so_partner else False

        job_type = int(res_rec[0]['job_type'][0]) if res_rec[0]['job_type'] else False
        job_type18 = get_mapped_rec(model='so.job.type', ID=job_type) if job_type else False

        record_ID = res_rec[0]['id']
        create_vals = {'old_id': record_ID, 'so_date': so_date18, 'eta': eta18, 'free_time': free_time18,
                          'bl_status': bl_status18, 'do': do18, 'demmurage': demmurage18, 'bl_number': bl_number18,
                            'container_no': container_no18, 'invoice_doc': invoice_doc18, 'pack_list_doc': pack_list_doc18,
                            'certificate_origin_doc': certificate_origin_doc18, 'bl_awb_doc': bl_awb_doc18,
                            'phyto_certificate_doc': phyto_certificate_doc18, 'health_certificate_doc': health_certificate_doc18,
                            'sale_order_id': sale_order_id18, 'so_partner': so_partner18, 'job_type': job_type18, 'state': state18}


        print("\n\n>>>>>>>>>>>>>create_vals",create_vals)
        so_job_rec_is_exist = sock18.execute_kw(dbname18, uid18, pwd18, 'so.checklist', 'search_read',
                                                 [[('old_id', '=', record_ID)]],
                                                 {'fields': ['old_id']})
        if not so_job_rec_is_exist:
            result = sock18.execute_kw(dbname18, uid18, pwd18, 'so.checklist', 'create', [create_vals])
            print("\n\ncreated record>>>>", result)
        else:
            print(f"\n Record existed?\n")

    print("\n\n\n<<<<<<<<<<<Existed records >>>>>>>>>>>>")

