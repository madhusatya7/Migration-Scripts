import xmlrpc.client as xmlrpclib

from Navire_Migration_Scripts.account_invoice_script_tax1_credit_note_fact import state18
from odoo.osv.expression import is_false

# version 12
url_common="http://139.185.32.81:9020//xmlrpc/2/common" #Add Here Navire Ip Server
url_object="http://139.185.32.81:9020//xmlrpc/2/object"

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
dbname18="navire"
username18="sidmec"
pwd18="$idmectech@com"
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

#796
domain=[('id','=',18370)]
hr_payslip = sock.execute_kw(dbname, uid, pwd, 'hr.payslip', 'search', [domain])

print("length",len(hr_payslip))

if len(hr_payslip)>0:
    for rec in range(0,len(hr_payslip)):
        res_rec = sock.execute_kw(dbname, uid, pwd, 'hr.payslip', 'search_read',[[('id', '=', hr_payslip[rec])]], {
												'fields': ['employee_id','date_from','number','name','contract_id','struct_id'
                                                           ,'credit_note','company_id','payslip_run_id','date','journal_id','move_id','state']})

        print(f"first {rec} is :{res_rec}")

        name18 = res_rec[0]['name']
        date_from18 = res_rec[0]['date_from']
        date18 = res_rec[0]['date']
        number18 = res_rec[0]['number']
        credit_note18 = res_rec[0]['credit_note']
        state18 = res_rec[0]['state']




        # m2O fields
        employee_id = int(res_rec[0]['employee_id'][0])
        employee_id18 = get_mapped_rec(model='hr.employee',ID=employee_id)

        company_id = int(res_rec[0]['company_id'][0]) if res_rec[0]['company_id'] else False
        company_id18 = get_mapped_rec(model='res.company', ID=company_id) if company_id else False

        contract_id = int(res_rec[0]['contract_id'][0]) if res_rec[0]['contract_id'] else False
        contract_id18 = get_mapped_rec(model='hr.contract', ID=contract_id) if contract_id else False

        struct_id = int(res_rec[0]['struct_id'][0]) if res_rec[0]['struct_id'] else False
        struct_id18 = get_mapped_rec(model='hr.salary.structure', ID=struct_id) if struct_id else False

        journal_id = int(res_rec[0]['journal_id'][0]) if res_rec[0]['journal_id'] else False
        journal_id18 = get_mapped_rec(model='account.journal', ID=journal_id) if journal_id else False

        payslip_run_id = int(res_rec[0]['payslip_run_id'][0]) if res_rec[0]['payslip_run_id'] else False
        payslip_run_id18 = get_mapped_rec(model='hr.payslip.run', ID=payslip_run_id) if payslip_run_id else False

        move_id = int(res_rec[0]['move_id'][0]) if res_rec[0]['move_id'] else False
        move_id18 = get_mapped_rec(model='account.move', ID=move_id) if move_id else False



        record_ID = res_rec[0]['id']

        create_vals = {'old_id':record_ID,'name':name18,'date_from':date_from18,'date':date18,'number':number18,
                       'credit_note':credit_note18,'state':state18,'employee_id':employee_id18,'company_id':company_id18,
                       'contract_id':contract_id18,'struct_id':struct_id18,'journal_id':journal_id18,'payslip_run_id':payslip_run_id18,
                       'move_id':move_id18}



        print(f"records in {create_vals}")

        # calculate lines
        hr_payslip_line = sock.execute_kw(dbname, uid, pwd, 'hr.payslip.line', 'search_read',
                                                   [[('slip_id', '=', record_ID)]], {
                                                       'fields': ['name', 'code', 'category_id','quantity', 'amount', 'total',
                                                                  'rate', 'salary_rule_id']})


        line_obj = []
        print(f"Record Main {rec} >>>>", create_vals)

        for line in hr_payslip_line:
            name18 = line['name']
            code18 = line['code']

            category_id = int(line['category_id'][0]) if line['category_id'] else False
            category_id18 = get_mapped_rec(model='hr.salary.rule.category', ID=category_id) if category_id else False

            quantity18 = line['quantity']
            amount18 = line['amount']
            total18 = line['total']
            rate18 = line['rate']

            salary_rule_id = int(line['salary_rule_id'][0]) if line['salary_rule_id'] else False
            salary_rule_id18 = get_mapped_rec(model='hr.salary.rule', ID=salary_rule_id) if salary_rule_id else False

            obj = {'name': name18,'code': code18,'category_id': category_id18,'quantity': quantity18,
                   'amount': amount18,'total': total18,'rate': rate18,'salary_rule_id': salary_rule_id18}


            print(f"lines {line} of line {rec} >>>>", obj)
            line_obj.append((0, 0, obj))


        create_vals.update({'order_line': line_obj})


        account_rec_is_exist = sock18.execute_kw(dbname18, uid18, pwd18, 'hr.payslip', 'search_read',
                                                         [[('old_id', '=', record_ID)]], {'fields': ['old_id']})


        if not account_rec_is_exist:
            result = sock18.execute_kw(dbname18, uid18, pwd18, 'hr.payslip', 'create', [create_vals])
            print("created record", result)
        else:
            print(f"\n Record existed?\n")
