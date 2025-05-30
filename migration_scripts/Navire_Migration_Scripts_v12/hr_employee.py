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
# 75 mapped with 82,11
# domain = [('id','=',11)]
hr_employee = sock.execute_kw(dbname, uid, pwd, 'hr.employee', 'search', [[]], {'order': 'id DESC'})

# print(hr_employee)
print("\n\n\nlength??????", len(hr_employee))

if len(hr_employee) > 0:
    for rec in range(0, len(hr_employee)):
        res_rec = sock.execute_kw(dbname, uid, pwd, 'hr.employee', 'search_read',
                                  [[('id', '=', hr_employee[rec])]], {
                                      'fields': ['name','work_location','work_email','mobile_phone','work_phone','job_title',
                                                 'manager','tz','gender','martial','image_128','children','parent_id','department_id',
                                                 'company_id','address_id','job_id','parent_id']})

        print(">>>>>>>>>>>>>>>>>>v12 records>>>>>>>>>>>>>>>>>>>>>>", res_rec)
        print(f"first {rec} is :{res_rec}")

        name18 = res_rec[0]['name']
        work_location18 = res_rec[0]['work_location']
        work_email18 = res_rec[0]['work_email']
        mobile_phone18 = res_rec[0]['mobile_phone']
        work_phone18 = res_rec[0]['work_phone']
        job_title18 = res_rec[0]['job_title']
        # manager18 = res_rec[0]['manager']
        tz18 = res_rec[0]['tz']
        gender18 = res_rec[0]['gender']
        # martial18 = res_rec[0]['martial'] if res_rec[0]['martial'] else False
        # children18 = res_rec[0]['children']



        #m2o fields
        parent_id = int(res_rec[0]['parent_id'][0]) if res_rec[0]['parent_id'] else False
        parent_id18 = get_mapped_rec(model='hr.employee', ID=parent_id) if parent_id else False

        job_id = int(res_rec[0]['job_id'][0]) if res_rec[0]['job_id'] else False
        job_id18 = get_mapped_rec(model='hr.job', ID=job_id) if job_id else False

        department_id = int(res_rec[0]['department_id'][0]) if res_rec[0]['department_id'] else False
        department_id18 = get_mapped_rec(model='hr.department', ID=department_id) if department_id else False

        company_id = int(res_rec[0]['company_id'][0]) if res_rec[0]['company_id'] else False
        company_id18 = get_mapped_rec(model='res.company', ID=company_id) if company_id else False

        address_id = int(res_rec[0]['address_id'][0]) if res_rec[0]['address_id'] else False
        address_id18 = get_mapped_rec(model='res.partner', ID=address_id) if address_id else False

        record_ID = res_rec[0]['id']
        create_vals = {'old_id': record_ID, 'name': name18,'work_location': work_location18,'work_email': work_email18,
                        'mobile_phone': mobile_phone18,'work_phone': work_phone18,'job_title': job_title18,
                        'tz':tz18,'gender':gender18,'job_id':job_id18,
                        'department_id':department_id18,'company_id':company_id18,'address_id':address_id18}

        # 'martial': martial18,'children':children18,'manager':manager18,'job_id':job_id,
        print("\n\n>>>>>>>>>>>>>create_vals",create_vals)
        hr_employee_is_exist = sock18.execute_kw(dbname18, uid18, pwd18, 'hr.employee', 'search_read',
                                                 [[('old_id', '=', record_ID)]],
                                                      {'fields': ['old_id']})
        if not hr_employee_is_exist:
            result = sock18.execute_kw(dbname18, uid18, pwd18, 'hr.employee', 'create', [create_vals])
            print("\n\ncreated record>>>>", result)
        else:
            id = hr_employee_is_exist[0]['id']
            print(f"\n Record existed?\n")
            # if not rp_rec_is_exist[0]['old_id']:
            print("UPgrage is >>>>>>>>", id, record_ID)
            result = sock18.execute_kw(dbname18, uid18, pwd18, 'hr.employee', 'write', [[id], {'parent_id':parent_id18}])
            print(">>>>>>", result)

