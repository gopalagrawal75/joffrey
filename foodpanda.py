from bson.json_util import dumps
from django.views.decorators.csrf import csrf_exempt
from . import db, get_json, basic_success, basic_error

failure = dumps({"Failed"})
@csrf_exempt
def check_email(request):
	try:
		email = request.GET['email']
	except:
		return basic_error("invalid parameters")
	try:
		creds = db.operation_heads
		check_email = creds.find_one({"email":email} , {"_id":False , "type":True})
		if check_email:
			return basic_success({"email":email , "level":check_email['type']})
		else:
			return basic_error("EmailID doesn't exist")
	except:
		return basic_error("Something Went Wrong")
def showVendorData(request):
	try:
		code = request.GET['vendor_code']
	except:
		return basic_error("invalid parameters")
		
	try:
		data={}
		restaurant = db.restaurant_data
		data['info']=restaurant.find_one({"vendor_code":code} , {"_id":False})
		
		sales = db.sales
		data['sales']=sales.find_one({"vendor_code":code} , {"_id":False})
		data['sales']['commision']=data['info']['commision']
		week4=db.ops_data_4_week
		data['week4']=week4.find_one({"vendor_code":code} , {"_id":False})
		weekly = db.ops_data_weekly
		data['weekly']=weekly.find({"vendor_code":code} , {"_id":False})
		log=db.log_data
		data['logs']=log.find_one({"vendor_code":code} , {"_id":False})
		action = db.action_board
		data['action']=action.find({"vendor_code":code} , {"_id":False})
		data['info']['order_last_4_week'] = data['week4']['orders']
		return basic_success(data)
	except Exception as e:
		return basic_error(e)
def Saleshead(request):
	try:
		email = request.GET['email']
	except:
		return basic_error("Invalid Parameter")
	try:
		check_level =db.operation_heads
		check = check_level.find_one({"email":email} , {"_id":False})
		if check and int(check['type']) is 3:
			return basic_success(db.sales_head.find_one(projection={"_id":False}))
		else:
			return basic_error("Something went Wrong")
	except Exception as e:
		return basic_error(e)
def Cityhead(request):
	try:
		email = request.GET['email']
	except:
		return basic_error("Invalid Parameter")
	try:
		check_level =db.operation_heads
		check = check_level.find_one({"email":email} , {"_id":False})
		if check and int(check['type']) is 2:
			return basic_success(db.city_head.find_one(projection={"_id":False}))
		else:
			return basic_error("Something went Wrong")
	except Exception as e:
		return basic_error(e)
def AM(request):
	try:
		email = request.GET['email']
	except:
		return basic_error("Invalid Parameter")
	try:
		check_level =db.operation_heads
		check = check_level.find_one({"email":email} , {"_id":False})
		if check and int(check['type']) is 1:
			return basic_success(db.am.find_one(projection={"_id":False}))
		else:
			return basic_error("Something went Wrong")
	except Exception as e:
		return basic_error(e)

def restaurant_portfolio(request):
	try:
		email = request.GET['email']
	except Exception as e :
		return basic_error(e)
	try:
		check_level =db.operation_heads
		check = check_level.find_one({"email":email} , {"_id":False})
		if check and int(check['type']) is 3:
			data = db.restaurant_data.find(projection = {"_id":False})
		elif  check and int(check['type']) is 2:
			data = db.restaurant_data.find({"city_head_email":email}, {"_id":False})
		elif  check and int(check['type']) is 1:
			data = db.restaurant_data.find({"rm_email":email}, {"_id":False})
		else:
			return basic_error("Something went Wrong")
		data_orig=list()
		for res_data in data:
			temp={}
			temp['code']=res_data['vendor_code']
			temp['name']=res_data['vendor_name']
			temp['prof_order']=res_data.get("prof_order")
			temp['action_pending']=res_data.get("action_pending")
			temp['link']="http://lannister-api.elasticbeanstalk.com/joffrey/restaurant?vendor_code="+res_data['vendor_code']
			data_orig.append(temp.copy())
		return basic_success(data_orig)
	except Exception as e:
		return basic_error(e)
def AM_portfolio(request):
	try:
		email = request.GET['email']
	except:
		return basic_error("Invalid Parameter")
	try:
		check_level =db.operation_heads
		check = check_level.find_one({"email":email} , {"_id":False})
		if check and int(check['type']) is 3:
			data = db.am.find(projection = {"_id":False})
		elif  check and int(check['type']) is 2:
			data = db.am.find({"city_head_email":email}, {"_id":False})
		else:
			return basic_error("Something went Wrong")
		data_orig=list()
		for res_data in data:
			temp={}
			temp['name']=res_data['am_name']
			temp['prof_order']=res_data['prof_order']
			temp['deal']=res_data.get("deal_penetration")
			temp['target']=res_data.get("target_acheiv_month")
			temp['link']="http://lannister-api.elasticbeanstalk.com/joffrey/am?email="+res_data.get('rm_email')
			data_orig.append(temp.copy())
		return basic_success(data_orig)
	except Exception as e:
		return basic_error(e)
def city_portfolio(request):
	try:
		email = request.GET['email']
	except:
		return basic_error("Invalid Parameter")
	try:
		check_level =db.operation_heads
		check = check_level.find_one({"email":email} , {"_id":False})
		if check and int(check['type']) is 3:
			data = db.city_head.find(projection = {"_id":False})
		else:
			return basic_error("Something went Wrong")
		data_orig=list()
		for res_data in data:
			temp={}
			temp['name']=res_data['ch_name']
			temp['prof_order']=res_data['prof_order']
			temp['deal']=res_data.get("deal_penetration")
			temp['target']=res_data.get("target_acheiv_month")
			temp['link']="http://lannister-api.elasticbeanstalk.com/joffrey/city_head?email="+res_data.get('city_head_email')
			data_orig.append(temp.copy())
		return basic_success(data_orig)
	except Exception as e:
		return basic_error(e)