import requests
import json
from flatten_json import flatten
import pymysql.cursors
import config
import datetime
import warnings

api_key = config.api_key
domain = config.domain
api_password = config.api_password

#how many results per page
per_page = config.per_page
#first page number to retrieve
page_number = config.page_number
#first date from which to retrieve tickets (don't worry about duplicated tickets; table will automatically reject duplicates)
first_date = config.first_date

def nice_encode(string):
	if isinstance(string, str):
		return string.encode('utf-8')
	elif string is None:
		return ""
	else:
		return string

def fix(dictionary, key):
	if key in dictionary:
		pass
	else:
		dictionary[key] = None

def nice_convert_timestamp(ts):
	if ts is not None:
		return datetime.datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ")
	else:
		return ts

def update_source(api_key, domain, api_password, connection, per_page, page_number, source):
	cursor = connection.cursor()

	#filter out warnings about duplicated keys
	warnings.filterwarnings('ignore', "\(1062.*")

	while True:
		if source == "tickets":
			r = requests.get("https://"+ domain +".freshdesk.com/api/v2/" + source + "?per_page="+ str(per_page) + "&page=" + str(page_number) + "&updated_since=" + first_date, auth = (api_key, api_password))
		else:
			r = requests.get("https://"+ domain +".freshdesk.com/api/v2/" + source + "?per_page="+ str(per_page) + "&page=" + str(page_number), auth = (api_key, api_password))

		if r.status_code == 200:
		  response = json.loads(r.content)
		  try:
		  	if source == "tickets":
		  		sql = "INSERT INTO `tickets` (`fr_escalated`,`spam`,`email_config_id`,`group_id`,`priority`,`requester_id`,`responder_id`,`source`,`company_id`,`status`,`subject`,`to_emails`,`product_id`,`id`,`type`,`due_by`,`fr_due_by`,`is_escalated`,`description`,`description_text`,`custom_fields_cf_number_provider`,`custom_fields_cf_priority_level`,`custom_fields_cf_is_bug`,`created_at`,`updated_at`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE `fr_escalated` = %s,`spam` = %s,`email_config_id` = %s,`group_id` = %s,`priority` = %s,`requester_id` = %s,`responder_id` = %s,`source` = %s,`company_id` = %s,`status` = %s,`subject` = %s,`to_emails` = %s,`product_id` = %s,`type` = %s,`due_by` = %s,`fr_due_by` = %s,`is_escalated` = %s,`description` = %s,`description_text` = %s,`custom_fields_cf_number_provider` = %s,`custom_fields_cf_priority_level` = %s,`custom_fields_cf_is_bug` = %s,`created_at` = %s,`updated_at` = %s"
			  	for i in range(len(response)):
			  		flat = flatten(response[i])
			  		for key in ['fr_escalated','spam','email_config_id','group_id','priority','requester_id','responder_id','source','company_id','status','subject','to_emails','product_id','id','type','due_by','fr_due_by','is_escalated','description','description_text','custom_fields_cf_number_provider','custom_fields_cf_priority_level','custom_fields_cf_is_bug','created_at','updated_at']:
			  			fix(flat, key)
			  		try:
			  			cursor.execute(sql, (nice_encode(flat['fr_escalated']), nice_encode(flat['spam']), nice_encode(flat['email_config_id']), nice_encode(flat['group_id']), nice_encode(flat['priority']), nice_encode(flat['requester_id']), nice_encode(flat['responder_id']), nice_encode(flat['source']), nice_encode(flat['company_id']), nice_encode(flat['status']), nice_encode(flat['subject']), nice_encode(flat['to_emails']), nice_encode(flat['product_id']), nice_encode(flat['id']), nice_encode(flat['type']), nice_convert_timestamp(flat['due_by']), nice_convert_timestamp(flat['fr_due_by']), nice_encode(flat['is_escalated']), nice_encode(flat['description']), nice_encode(flat['description_text']), nice_encode(flat['custom_fields_cf_number_provider']), nice_encode(flat['custom_fields_cf_priority_level']), nice_encode(flat['custom_fields_cf_is_bug']), nice_convert_timestamp(flat['created_at']), nice_convert_timestamp(flat['updated_at']), nice_encode(flat['fr_escalated']), nice_encode(flat['spam']), nice_encode(flat['email_config_id']), nice_encode(flat['group_id']), nice_encode(flat['priority']), nice_encode(flat['requester_id']), nice_encode(flat['responder_id']), nice_encode(flat['source']), nice_encode(flat['company_id']), nice_encode(flat['status']), nice_encode(flat['subject']), nice_encode(flat['to_emails']), nice_encode(flat['product_id']), nice_encode(flat['type']), nice_convert_timestamp(flat['due_by']), nice_convert_timestamp(flat['fr_due_by']), nice_encode(flat['is_escalated']), nice_encode(flat['description']), nice_encode(flat['description_text']), nice_encode(flat['custom_fields_cf_number_provider']), nice_encode(flat['custom_fields_cf_priority_level']), nice_encode(flat['custom_fields_cf_is_bug']), nice_convert_timestamp(flat['created_at']), nice_convert_timestamp(flat['updated_at'])))
			  		except pymysql.InternalError as e:
			  			print(e)
		  	elif source == "companies":
		  		sql = "INSERT INTO `companies` (`id`, `name`, `description`, `note`, `created_at`, `updated_at`, `custom_fields_sfaccountid`, `custom_fields_slug`, `health_score`, `account_tier`, `renewal_date`, `industry`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE `name` = %s, `description` = %s, `note` = %s, `created_at` = %s, `updated_at` = %s, `custom_fields_sfaccountid` = %s, `custom_fields_slug` = %s, `health_score` = %s, `account_tier` = %s, `renewal_date` = %s, `industry` = %s"
			  	for i in range(len(response)):
			  		flat = flatten(response[i])
			  		for key in ['id', 'name', 'description', 'note', 'created_at', 'updated_at', 'custom_fields_sfaccountid', 'custom_fields_slug', 'health_score', 'account_tier', 'renewal_date', 'industry']:
			  			fix(flat, key)
			  		try:
			  			cursor.execute(sql, (nice_encode(flat['id']), nice_encode(flat['name']), nice_encode(flat['description']), nice_encode(flat['note']), nice_convert_timestamp(flat['created_at']), nice_convert_timestamp(flat['updated_at']), nice_encode(flat['custom_fields_sfaccountid']), nice_encode(flat['custom_fields_slug']), nice_encode(flat['health_score']), nice_encode(flat['account_tier']), nice_encode(flat['renewal_date']), nice_encode(flat['industry']), nice_encode(flat['name']), nice_encode(flat['description']), nice_encode(flat['note']), nice_convert_timestamp(flat['created_at']), nice_convert_timestamp(flat['updated_at']), nice_encode(flat['custom_fields_sfaccountid']), nice_encode(flat['custom_fields_slug']), nice_encode(flat['health_score']), nice_encode(flat['account_tier']), nice_encode(flat['renewal_date']), nice_encode(flat['industry'])))
			  		except pymysql.InternalError as e:
			  			print(e)
		  	elif source == "contacts":
		  		sql = "INSERT INTO `contacts` (`active`,`address`,`company_id`,`description`,`email`,`id`,`job_title`,`language`,`mobile`,`name`,`phone`,`time_zone`,`twitter_id`,`custom_fields_slug`,`custom_fields_sfcontactid`,`facebook_id`,`created_at`,`updated_at`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE `active` = %s,`address` = %s,`company_id` = %s,`description` = %s,`email` = %s,`job_title` = %s,`language` = %s,`mobile` = %s,`name` = %s,`phone` = %s,`time_zone` = %s,`twitter_id` = %s,`custom_fields_slug` = %s,`custom_fields_sfcontactid` = %s,`facebook_id` = %s,`created_at` = %s,`updated_at` = %s"
			  	for i in range(len(response)):
			  		flat = flatten(response[i])
			  		for key in ['active','address','company_id','description','email','id','job_title','language','mobile','name','phone','time_zone','twitter_id','custom_fields_slug','custom_fields_sfcontactid','facebook_id','created_at','updated_at']:
			  			fix(flat, key)
			  		try:
			  			cursor.execute(sql, (nice_encode(flat['active']), nice_encode(flat['address']), nice_encode(flat['company_id']), nice_encode(flat['description']), nice_encode(flat['email']), nice_encode(flat['id']), nice_encode(flat['job_title']), nice_encode(flat['language']), nice_encode(flat['mobile']), nice_encode(flat['name']), nice_encode(flat['phone']), nice_encode(flat['time_zone']), nice_encode(flat['twitter_id']), nice_encode(flat['custom_fields_slug']), nice_encode(flat['custom_fields_sfcontactid']), nice_encode(flat['facebook_id']), nice_convert_timestamp(flat['created_at']), nice_convert_timestamp(flat['updated_at']), nice_encode(flat['active']), nice_encode(flat['address']), nice_encode(flat['company_id']), nice_encode(flat['description']), nice_encode(flat['email']), nice_encode(flat['job_title']), nice_encode(flat['language']), nice_encode(flat['mobile']), nice_encode(flat['name']), nice_encode(flat['phone']), nice_encode(flat['time_zone']), nice_encode(flat['twitter_id']), nice_encode(flat['custom_fields_slug']), nice_encode(flat['custom_fields_sfcontactid']), nice_encode(flat['facebook_id']), nice_convert_timestamp(flat['created_at']), nice_convert_timestamp(flat['updated_at'])))
			  		except pymysql.InternalError as e:
			  			print(e)
		  	else:
		  		print("Source", source, "not recognized")
		  	connection.commit()
		  	print("Page", page_number, "of", source, "written successfully")
		  except:
		  	print("Error writing page", page_number, "to table")
		else:
		  print("Failed to read " + source + " page " + page_number + "; errors are displayed below")
		  response = json.loads(r.content)
		  print(response["message"])

		  print("x-request-id :", r.headers['x-request-id'])
		  print("Status Code :", str(r.status_code))

		#checks if there is another page of results and breaks the loop if not
		try:
			r.headers['link']
			page_number += 1
		except:
			break

connection = pymysql.connect(host=config.host,
                             user=config.user,
                             password=config.password,
                             db=config.database,
                             cursorclass=pymysql.cursors.DictCursor)

sources = ["tickets", "companies", "contacts"]
for source in sources:
	update_source(api_key, domain, api_password, connection, per_page, page_number, source)