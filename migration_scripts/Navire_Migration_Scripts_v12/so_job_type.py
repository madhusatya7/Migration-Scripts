import xmlrpc.client as xmlrpclib


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
dbname18="navire_prod"
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

# domain = [('id','=',1)]
so_job_type = sock.execute_kw(dbname, uid, pwd, 'so.job.type', 'search', [[]], {'order': 'id DESC'})

print(so_job_type)
print("\n\n\nlength??????", len(so_job_type))

if len(so_job_type) > 0:
    for rec in range(0, len(so_job_type)):
        res_rec = sock.execute_kw(dbname, uid, pwd, 'so.job.type', 'search_read',
                                  [[('id', '=', so_job_type[rec])]], {
                                      'fields': ['name', 'code']})

        print(">>>>>>>>>>>>>>>>>>v12 records>>>>>>>>>>>>>>>>>>>>>>", res_rec)
        print(f"first {rec} is :{res_rec}")

        name18 = res_rec[0]['name']
        code18 = res_rec[0]['code']

        record_ID = res_rec[0]['id']
        create_vals = {'old_id': record_ID, 'name': name18, 'code': code18,

                       }
        print("\n\n>>>>>>>>>>>>>create_vals",create_vals)
        so_job_rec_is_exist = sock18.execute_kw(dbname18, uid18, pwd18, 'so.job.type', 'search_read',
                                                 [[('old_id', '=', record_ID)]],
                                                 {'fields': ['old_id']})
        if not so_job_rec_is_exist:
            result = sock18.execute_kw(dbname18, uid18, pwd18, 'so.job.type', 'create', [create_vals])
            print("\n\ncreated record>>>>", result)
        else:
            print(f"\n Record existed?\n")

