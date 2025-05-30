
import xmlrpc.client as xmlrpclib
from datetime import datetime as dt, timedelta as td

# version 12
url_common="http://193.123.91.114:8069/xmlrpc/2/common"
url_object="http://193.123.91.114:8069/xmlrpc/2/object"

sock_common = xmlrpclib.ServerProxy(url_common)
dbname="rahidb"
username="sidmec1"
pwd="sankar123"
uid = sock_common.authenticate(dbname, username, pwd, {})
sock = xmlrpclib.ServerProxy(url_object)

# version 18
url_common18="http://localhost:8069/xmlrpc/2/common"
url_object18="http://localhost:8069/xmlrpc/2/object"

sock_common18 = xmlrpclib.ServerProxy(url_common18)
dbname18="alrahi_live_master"
username18="sidmec"
pwd18="$idmectech@com"
uid18 = sock_common18.authenticate(dbname18, username18, pwd18, {})
sock18 = xmlrpclib.ServerProxy(url_object18)

existing_records = []

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

e_jrnl = []
# eliminate vendor bills

#ej_31 = [31,27,99,139,316,123,91,107,115,131,163,35,67,147,302,43,83,51,11,19,59,75,171,274,155,26,98,138,315,122,90,106,114,130,162,34,66,146,301,42,82,50,10,18,58,74,170,273,154]
#ej_103 = [103,27,99,139,316,123,91,107,115,131,163,35,67,147,302,43,83,51,11,19,59,75,171,274,155,26,98,138,315,122,90,106,114,130,162,34,66,146,301,42,82,50,10,18,58,74,170,273,154]
#ej_143 =[143,27,99,139,316,123,91,107,115,131,163,35,67,147,302,43,83,51,11,19,59,75,171,274,155,26,98,138,315,122,90,106,114,130,162,34,66,146,301,42,82,50,10,18,58,74,170,273,154]
#ej_320 =[320,27,99,139,316,123,91,107,115,131,163,35,67,147,302,43,83,51,11,19,59,75,171,274,155,26,98,138,315,122,90,106,114,130,162,34,66,146,301,42,82,50,10,18,58,74,170,273,154]
#ej_127 =[127,27,99,139,316,123,91,107,115,131,163,35,67,147,302,43,83,51,11,19,59,75,171,274,155,26,98,138,315,122,90,106,114,130,162,34,66,146,301,42,82,50,10,18,58,74,170,273,154]
#ej_95 =[95,27,99,139,316,123,91,107,115,131,163,35,67,147,302,43,83,51,11,19,59,75,171,274,155,26,98,138,315,122,90,106,114,130,162,34,66,146,301,42,82,50,10,18,58,74,170,273,154]
#ej_111 =[111,27,99,139,316,123,91,107,115,131,163,35,67,147,302,43,83,51,11,19,59,75,171,274,155,26,98,138,315,122,90,106,114,130,162,34,66,146,301,42,82,50,10,18,58,74,170,273,154]
#ej_119 =[119,27,99,139,316,123,91,107,115,131,163,35,67,147,302,43,83,51,11,19,59,75,171,274,155,26,98,138,315,122,90,106,114,130,162,34,66,146,301,42,82,50,10,18,58,74,170,273,154]
#ej_135 =[135,27,99,139,316,123,91,107,115,131,163,35,67,147,302,43,83,51,11,19,59,75,171,274,155,26,98,138,315,122,90,106,114,130,162,34,66,146,301,42,82,50,10,18,58,74,170,273,154]
#ej_167 =[167,27,99,139,316,123,91,107,115,131,163,35,67,147,302,43,83,51,11,19,59,75,171,274,155,26,98,138,315,122,90,106,114,130,162,34,66,146,301,42,82,50,10,18,58,74,170,273,154]
#ej_39 =[39,27,99,139,316,123,91,107,115,131,163,35,67,147,302,43,83,51,11,19,59,75,171,274,155,26,98,138,315,122,90,106,114,130,162,34,66,146,301,42,82,50,10,18,58,74,170,273,154]
#ej_71 =[71,27,99,139,316,123,91,107,115,131,163,35,67,147,302,43,83,51,11,19,59,75,171,274,155,26,98,138,315,122,90,106,114,130,162,34,66,146,301,42,82,50,10,18,58,74,170,273,154]
### [,27,99,139,316,123,91,107,115,131,163,35,67,147,302,43,83,51,11,19,59,75,171,274,155,26,98,138,315,122,90,106,114,130,162,34,66,146,301,42,82,50,10,18,58,74,170,273,154]
### [,27,99,139,316,123,91,107,115,131,163,35,67,147,302,43,83,51,11,19,59,75,171,274,155,26,98,138,315,122,90,106,114,130,162,34,66,146,301,42,82,50,10,18,58,74,170,273,154]
#ej_151 =[151,27,99,139,316,123,91,107,115,131,163,35,67,147,302,43,83,51,11,19,59,75,171,274,155,26,98,138,315,122,90,106,114,130,162,34,66,146,301,42,82,50,10,18,58,74,170,273,154]
#ej_306 =[306,27,99,139,316,123,91,107,115,131,163,35,67,147,302,43,83,51,11,19,59,75,171,274,155,26,98,138,315,122,90,106,114,130,162,34,66,146,301,42,82,50,10,18,58,74,170,273,154]

#ej_47 =[47,27,99,139,316,123,91,107,115,131,163,35,67,147,302,42,43,83,51,11,19,59,75,171,274,155,26,98,138,315,122,90,106,114,130,162,34,66,146,301,82,50,10,18,58,74,170,273,154]
#ej_87 =[87,27,99,139,316,123,91,107,115,131,163,35,67,147,302,43,83,51,11,19,59,75,171,274,155,26,98,138,315,122,90,106,114,130,162,34,66,146,301,42,82,50,10,18,58,74,170,273,154]
#ej_55 =[55,27,99,139,316,123,91,107,115,131,163,35,67,147,302,43,83,51,11,19,59,75,171,274,155,26,98,138,315,122,90,106,114,130,162,34,66,146,301,42,82,50,10,18,58,74,170,273,154]
ej_15 =[15,27,99,139,316,123,91,107,115,131,163,35,67,147,302,43,83,51,11,19,59,75,171,274,155,26,98,138,315,122,90,106,114,130,162,34,66,146,301,42,82,50,10,18,58,74,170,273,154,262,266]
#ej_8 =[8,27,99,139,316,123,91,107,115,131,163,35,67,147,302,43,83,51,11,19,59,75,171,274,155,26,98,138,315,122,90,106,114,130,162,34,66,146,301,42,82,50,10,18,58,74,170,273,154]
#ej_23 =[23,27,99,139,316,123,91,107,115,131,163,35,67,147,302,43,83,51,11,19,59,75,171,274,155,26,98,138,315,122,90,106,114,130,162,34,66,146,301,42,82,50,10,18,58,74,170,273,154]
#ej_63 =[63,27,99,139,316,123,91,107,115,131,163,35,67,147,302,43,83,51,11,19,59,75,171,274,155,26,98,138,315,122,90,106,114,130,162,34,66,146,301,42,82,50,10,18,58,74,170,273,154]
#ej_79 =[79,27,99,139,316,123,91,107,115,131,163,35,67,147,302,43,83,51,11,19,59,75,171,274,155,26,98,138,315,122,90,106,114,130,162,34,66,146,301,42,82,50,10,18,58,74,170,273,154]
#ej_175 =[175,27,99,139,316,123,91,107,115,131,163,35,67,147,302,43,83,51,11,19,59,75,171,274,155,26,98,138,315,122,90,106,114,130,162,34,66,146,301,42,82,50,10,18,58,74,170,273,154]
#ej_278 =[278,27,99,139,316,123,91,107,115,131,163,35,67,147,302,43,83,51,11,19,59,75,171,274,155,26,98,138,315,122,90,106,114,130,162,34,66,146,301,42,82,50,10,18,58,74,170,273,154]
#ej_159 =[159,27,99,139,316,123,91,107,115,131,163,35,67,147,302,43,83,51,11,19,59,75,171,274,155,26,98,138,315,122,90,106,114,130,162,34,66,146,301,42,82,50,10,18,58,74,170,273,154]

#domain = [('date','>=','2024-01-01'),('company_id','=',4),('journal_id','not in', ej_31)]
#domain = [('date','>=','2024-01-01'),('company_id','=',13),('journal_id','not in', ej_103)]
#domain = [('date','>=','2024-01-01'),('company_id','=',18),('journal_id','not in', ej_143)]
# domain = [('date','>=','2024-01-01'),('company_id','=',26),('journal_id','not in', ej_320)]
# domain = [('date','>=','2024-01-01'),('company_id','=',16),('journal_id','not in', ej_127)]
# domain = [('date','>=','2024-01-01'),('company_id','=',12),('journal_id','not in', ej_95)]
#domain = [('date','>=','2024-01-01'),('company_id','=',6),('journal_id','not in', ej_47)]
# domain = [('date','>=','2024-01-01'),('company_id','=',15),('journal_id','not in', ej_119)]
# domain = [('date','>=','2024-01-01'),('company_id','=',17),('journal_id','not in', ej_135)]

domain = [('journal_id','=',178),('date','>=','2024-01-01'),('date','<=','2024-12-31'),('state','in',['posted']),('company_id','=',2),('journal_id','not in', ej_15)]

# domain = [('date','>=','2024-01-01'),('company_id','=',5),('journal_id','not in', ej_39)]
# domain = [('date','>=','2024-01-01'),('company_id','=',9),('journal_id','not in', ej_71)]
# domain = [('date','>=','2024-01-01'),('company_id','=',19),('journal_id','not in', ej_151)]
#domain = [('date','>=','2024-01-01'),('company_id','=',25),('journal_id','not in', ej_306)]
# domain = [('date','>=','2024-01-01'),('company_id','=',6),('journal_id','not in', ej_47)]
# domain = [('date','>=','2024-01-01'),('company_id','=',11),('journal_id','not in', ej_87)]
# domain = [('date','>=','2024-01-01'),('company_id','=',7),('journal_id','not in', ej_55)]
#domain = [('date','>=','2024-01-01'),('company_id','=',2),('journal_id','not in', ej_15)]

# domain = [('date','>=','2024-01-01'),('company_id','=',3),('journal_id','not in', ej_23)]
# domain = [('date','>=','2024-01-01'),('company_id','=',8),('journal_id','not in', ej_63)]
# domain = [('date','>=','2024-01-01'),('company_id','=',10),('journal_id','not in', ej_79)]
# domain = [('date','>=','2024-01-01'),('company_id','=',22),('journal_id','not in', ej_175)]
# domain = [('date','>=','2024-01-01'),('company_id','=',23),('journal_id','not in', ej_278)]
# domain = [('date','>=','2024-01-01'),('company_id','=',20),('journal_id','not in', ej_159)]
#domain = ('date','>=','2024-01-01'),('company_id','=',14),('journal_id','not in', ej_111)

account_move = sock.execute_kw(dbname, uid, pwd, 'account.move', 'search', [domain],{'order': 'id DESC'})
# print(account_move)
print("\n\n>>>>>Total length",len(account_move))

##############################
#account_move = account_move[7900:]
#account_move = account_move[7000:]
#account_move = account_move[9290:]
#account_move = account_move[130:]
#account_move = account_move[910:]
#print("\nNew length>>>>>>>>",len(account_move))
###########################

if len(account_move)>0:
    for rec in range(0,len(account_move)):
        account_move_rec = sock.execute_kw(dbname, uid, pwd, 'account.move', 'search_read',[[('id', '=', account_move[rec])]], {
												'fields': ['name','ref','date','state','journal_id','company_id','currency_id','narration']})

        print("\nCurrent record>>>>>>>",account_move[rec],account_move_rec) 
        name18 = account_move_rec[0]['name']
        ref18 = account_move_rec[0]['ref']
        date18 = account_move_rec[0]['date']
        state18 = account_move_rec[0]['state']
        #m2o field
        journal_id = int(account_move_rec[0]['journal_id'][0] if account_move_rec[0]['journal_id'] else False)
        journal_id18 = get_mapped_rec(model='account.journal', ID=journal_id) if journal_id else False
        # currency_id = int(account_move_rec[0]['currency_id'][0])
        # currency_id18 = get_mapped_rec(model='res.currency', ID=currency_id)
        currency_id18 = 128
        company_id = int(account_move_rec[0]['company_id'][0])
        company_id18 = get_mapped_rec(model='res.company', ID=company_id) if company_id else False
        narration18 =account_move_rec[0]['narration'] or ''
        
        record_ID = account_move_rec[0]['id']

        create_vals = {'old_id1':record_ID,'auto_post': 'no','payment_date': date18 or dt.now().date(),'move_type':'entry','name':name18,'ref':ref18,'date':date18,'currency_id':currency_id18,'journal_id':journal_id18,'company_id':company_id18,'narration':narration18}

        # calculate lines
        account_move_rec_line = sock.execute_kw(dbname, uid, pwd, 'account.move.line', 'search_read',
                                              [[('move_id', '=', record_ID)]], {
                                                  'fields': ['name', 'partner_id','account_id','debit','credit','amount_currency','currency_id','tax_ids']})

        line_obj = []
        for line in account_move_rec_line:
            lid = line['id']
            lname18 = line['name']
            debit18 = line['debit']
            credit18 = line['credit']
            amount_currency18 = line['amount_currency']
            partner_id = line['partner_id'][0] if line['partner_id'] else False
            partner_id18 = get_mapped_rec(model='res.partner', ID=partner_id) if partner_id else False
            
            # currency_id = line['currency_id'][0]
            # lcurrency_id18 = get_mapped_rec(model='res.currency', ID=currency_id)
            lcurrency_id18 = 128

            if debit18:
                amount_currency18 = debit18
            if credit18:
                amount_currency18 = -credit18
            
            # eliminate current yeat earnings
            account_id = line['account_id'][0]
            if account_id in [740,2405,3330,6508,2960,2220,2590,2775,3145,3885,925,1665,3515,6240,1110,2035,1295,370,185,555,1480,1850,4070,5507,3700]:
                account_id18 = 160
            else:
                 account_id18 = get_mapped_rec(model='account.account',ID=account_id) if account_id else False

            # 'tax_ids':tax_ids18
            obj = {'old_id1':lid,'name':lname18,'debit':debit18,'credit':credit18,'amount_currency':amount_currency18,'partner_id':partner_id18,'account_id':account_id18,'currency_id':lcurrency_id18}
            line_obj.append((0, 0, obj))

        create_vals.update({'line_ids': line_obj})

        print ("\n\n\nCreating Record in v18 {} $$$$$$$$>>>>??",rec)
        try:
            account_move_rec_exist = sock18.execute_kw(dbname18, uid18, pwd18, 'account.move','search_read', [[('old_id1','=',record_ID)]], {'fields': ['old_id1','name']})
            if not account_move_rec_exist:
                # same_name_rec_exist = sock18.execute_kw(dbname18, uid18, pwd18, 'account.move','search_read', [[('name','=',create_vals['name'])]], {'fields': ['name']})
                # if not same_name_rec_exist:
                result =sock18.execute_kw(dbname18, uid18, pwd18, 'account.move','create', [create_vals])
                print("\n\n>> created record",result)
                if state18 == 'posted' and create_vals['line_ids']!= []:
                    sock18.execute_kw(dbname18, uid18, pwd18, 'account.move', 'action_post', [result],{})
                # commented because multiples came
                # else:
                #     print(">>>>>>>>same  name record existed >>>>>>>>>>>>>>>>",create_vals)
                #     create_vals['name'] = str(create_vals['name']) + 'append v18'
                #     existing_records.append(create_vals)
                #     result1 =sock18.execute_kw(dbname18, uid18, pwd18, 'account.move','create', [create_vals])
                #     if state18 == 'posted' and create_vals['line_ids']!= []:
                #         sock18.execute_kw(dbname18, uid18, pwd18, 'account.move', 'action_post', [result1],{})
            else:
                print (f"\n Record existed?\n\n")
        except Exception as e:
            print(f">>>>>>>>>Error processing record {account_move_rec[0]['name']}: {e}>>>>>>>>>>>>>>>>")

    print("<<<??Exisitng records>>>>>",existing_records)
