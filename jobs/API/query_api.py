
# RADARR https://github.com/Radarr/Radarr/wiki/API


# def digicert_api_call(request_code="GET",endpoint="/"):
#     api_token = "BPKRV2CHLFBCV6M2IHT7GBJUH4NCLXONI67BMOXSKIIM4HPJKZAAEGN6ZXKWZGGFVMZTJYBCCQI6LWY5P"
#     api_url_base = "https://www.digicert.com/services/v2"
#     headers = { "Content-Type": "application/json", \
#                 "Authorization": f"Bearer {api_token}"}         # may make sense to have a separate function that passes this based on 0rovider
#     api_url = f"{api_url_base}/{endpoint}"
#     if request_code == "GET":
#         response = requests.get(api_url, headers=headers)
#     elif request_code is "POST":
#         response = requests.post(api_url, headers=headers)
#     elif request_code is "HEAD":
#         response = requests.head(api_url, headers=headers)
#     elif request_code is "DELETE":
#         response = requests.delete(api_url, headers=headers)
#     elif request_code is "PUT":
#         response = requests.put(api_url, headers=headers)
#     else:
#         message_code(-1)
#     payload=json.loads(response.content.decode('utf-8'))                # find out what fields are needed to program
#     status_code = response.status_code
#     print(f"{payload}")             # status printing
#     try:
#         if status_code == 200:
#             message_code(code)
#         if status_code == 403:
#             message_code(code)
#         if status_code == 404:
#             message_code(code)
#         else:
#             message_code(-1)
#         return payload
#     except:
#         message_code(-2)
#
#
# def set(self,
#         endpoint = ""):
# 	self.api_url = f"{self.api_url_base}/{endpoint}"
# 	self.show_values()
#
# 	def digicert_api_response_parser(self,
# 	                                 request_code = "GET",
# 	                                 debug = False):
# 		import json
# 		from requests import (
# 			get,
# 			head,
# 			put,
# 			post,
# 			delete,
# 			)
#
# 		message_code(602,
# 		             "Display API Response Parser",`
# 		             debug)
#
# 		if request_code == "GET":
# 			response = get(self.api_url,
# 			               auth = (self.username,
# 			                       self.api_token))
#
# 		elif request_code == "HEAD":
# 			response = head(self.api_url,
# 			                auth = (self.username,
# 			                        self.api_token))
#
# 		elif request_code == "PUT":
# 			response = put(self.api_url,
# 			               auth = (self.username,
# 			                       self.api_token))
#
# 		elif request_code == "POST":
# 			response = post(self.api_url,
# 			                auth = (self.username,
# 			                        self.api_token))
#
# 		elif request_code == "DELETE":
# 			response = delete(self.api_url,
# 			                  auth = (self.username,
# 			                          self.api_token))
#
# 		else:
# 			message_code(-1)
#
# 		message_code(603,
# 		             f"DIGICERT API {request_code}",
# 		             response)
#
# 		message_code(601,
# 		             "Display API Response Parser")
#
# 		return json.loads(response.content.decode('utf-8')), response.status_code
