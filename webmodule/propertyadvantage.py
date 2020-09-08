from .lib_httprequest import *
from bs4 import BeautifulSoup
import os.path
import re
import json
import datetime
import requests
import urllib3
import sys
import json

httprequestObj = lib_httprequest()

class propertyadvantage():
    
    name = 'propertyadvantage'

    def __init__(self):
    
        try:
            import configs

        except ImportError:
            configs = {}

        self.encoding = 'utf-8'
        self.imgtmp = 'imgtmp'
        self.debug = 0
        self.debugresdata = 0
        self.baseurl = 'https://propertyadvantage.net'
        self.parser = 'html.parser'

    
    def register_user(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        start_time = datetime.datetime.utcnow()

        result = {
            "websitename": "propertyadvantage",
            "success": "false",
            "start_time": str(start_time),
            "ds_id": postdata["ds_id"],
            "end_time": '',
            "usage_time": '',
            "detail": ''
        }

        data = {
            'status': 'owner',
            'email': '',
            'pass': '',
            'conpass': '',
            'name': '',
            'lastname': '',
            'phone': '',
            'address': '-',
            'submit': ''
        }

        data['email'] = postdata['user']
        data['pass'] = postdata['pass']
        data['conpass'] = postdata['pass']
        data['name'] = postdata['name_th']
        data['lastname'] = postdata['surname_th']
        data['phone'] = postdata['tel']

        response = httprequestObj.http_post('https://propertyadvantage.net/signup_member.php', data=data)

        soup = BeautifulSoup(response.content, features='html.parser')
        if soup.find_all('div',attrs={'class':"alert alert-danger"}):
            result['success'] = "false"
            result['detail'] = 'Already Registered!!'
        else:
            result['success'] = "true"
            result['detail'] = 'User Registered with Email:- {}'.format(data['email'])

        end_time = datetime.datetime.utcnow()     
        result['end_time'] = str(end_time)
        result['usage_time'] = str(end_time - start_time)

        return {
            "websitename": "propertyadvantage",
            "success": result['success'],
            'ds_id': postdata['ds_id'],
            "start_time": result['start_time'],
            "ds_id": result["ds_id"],
            "end_time": result['end_time'],
            "usage_time": result['usage_time'],
            "detail": result['detail']
        }

    def test_login(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        start_time = datetime.datetime.utcnow()

        data = {
            'log_u': '',
            'log_p': '',
            'submit': ''
        }

        data['log_u'] = postdata['user']
        data['log_p'] = postdata['pass']

        result = {
            "websitename": 'propertyadvantage',
            "success": "false",
            "start_time": '',
            "ds_id": postdata["ds_id"],
            "end_time": '',
            "usage_time": '',
            "detail": '',
        }
        result['start_time'] = str(start_time)

        response = httprequestObj.http_post('https://propertyadvantage.net/login', data=data)

        soup = BeautifulSoup(response.content, features='html.parser')
        if soup.find_all('div',attrs={'class':"alert alert-danger"}):
            result['success'] = "false"
            result['detail'] = 'Incorrect Username or Password !!'
        else:
            result['success'] = "true"
            result['detail'] = 'User Logged In with Email:- {}'.format(data['log_u'])

        end_time = datetime.datetime.utcnow()     
        result['end_time'] = str(end_time)
        result['usage_time'] = str(end_time - start_time)

        return {
            "websitename": 'propertyadvantage',
            "success": result['success'],
            "start_time": result['start_time'],
            "end_time": result['end_time'],
            "usage_time": result['usage_time'],
            "detail": result['detail'],
            "ds_id": result["ds_id"],
        }

    def edit_post(self,postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        start_time = datetime.datetime.utcnow()

        test_login = self.test_login(postdata)
        result =  {
            "success": test_login['success'],
            "usage_time": '',
            "start_time": str(start_time),
            "end_time": '',
            "log_id": postdata['log_id'],
            "account_type": "null",
            "detail": '',
            "websitename": "propertyadvantage"
        }

        if test_login['success'] == "true":
            params = (
                ('id', postdata['post_id']),
            )
            r = httprequestObj.http_get('https://propertyadvantage.net/edit_property', params=params)
            soup = BeautifulSoup(r.content,features='html.parser')
            if soup.text == '':
                end_time = datetime.datetime.utcnow()     
                result['end_time'] = str(end_time)
                result['usage_time'] = str(end_time - start_time)
                return {
                    "success": "false",
                    "usage_time": result["usage_time"],
                    "start_time": str(start_time),
                    "end_time": result['end_time'],
                    "log_id": postdata['log_id'],
                    "account_type": "null",
                    "detail": "No post to edit with given id",
                    "websitename": "propertyadvantage"
                }

            if 'web_project_name' not in postdata or postdata['web_project_name'] is None:
                if 'project_name' in postdata and postdata['project_name'] is not None:
                    postdata['web_project_name'] = postdata['project_name']
                else:
                    postdata['web_project_name'] = postdata['post_title_th']
            
            prod_address = ""
            for add in [postdata['addr_soi'], postdata['addr_road'], postdata['addr_sub_district'], postdata['addr_district'], postdata['addr_province']]:
                if add is not None:
                    prod_address += add + " "
            prod_address = prod_address[:-1]

            data = {
                'name': postdata['post_title_th'],
                'project': postdata['web_project_name'],
                'cate': '',
                'section': '',
                'number': prod_address,
                'soi': postdata['addr_soi'],
                'road': postdata['addr_road'],
                'Province': '64',
                'District': '864',
                'Subdistrict': '7785',
                'price': '',
                'area': '',
                'layer': '',
                'room': postdata['bed_room'],
                'toilet': postdata['bath_room'],
                'detail': postdata['post_description_th'],
                'ID': postdata['post_id'],
                'Submit': 'Save data'
            }

            if postdata['listing_type'] == 'ขาย':
                data['cate'] = '1'
            else:
                data['cate'] = '2'

            pd_properties = {
                '1': '4',
                '2': '1',
                '3': '1',
                '4': '2',
                '5': '12',
                '6': '6',
                '7': '5',
                '8': '7',
                '9': '10',
                '10': '8',
                '25': '8' 
            }
            
            data['section'] = pd_properties[str(postdata['property_type'])]
            data['price'] = str(postdata['price_baht'])

            if data['section'] == '4':
                data['area'] = str(postdata['floor_area']) + 'ตร.ม.'
            else:
                if postdata['land_size_rai'] == None:
                    postdata['land_size_rai'] = '0'
                if postdata['land_size_ngan'] == None:
                    postdata['land_size_ngan'] = '0'
                if postdata['land_size_wa'] == None:
                    postdata['land_size_wa'] = '0'
                rai = str(postdata['land_size_rai']) + 'ไร่'
                ngan = str(postdata['land_size_ngan']) + 'งาน'
                square_wah = str(postdata['land_size_wa']) + 'ตารางวา'
                data['area'] = rai + ngan + square_wah
            
            
            fp = open('./static/propertyadvantage_province.json')
            provinces = json.load(fp)
            
            province = ''.join(map(str,str(postdata['addr_province']).split(' ')))
            for item in provinces.items():
                if province in ''.join(map(str,str(item[0]).split(' '))):
                    data['Province'] = item[1]  
                    break              
            
            params = (
                ('ID', data['Province']),
                ('TYPE', 'District'),
            )
            
            districts = httprequestObj.http_get('https://propertyadvantage.net/getaddress.php', params= params).json()
            district = ''.join(map(str,str(postdata['addr_district']).split(' ')))
            for d in districts:
                if district in ''.join(map(str,str(d['amphur_name'].split(' ')[0]).split(' '))):
                    data['District'] = d['amphur_id']
                    break
            
            params = (
                ('ID', '864'),
                ('TYPE', 'Subdistrict'),
            )

            subdistricts = httprequestObj.http_get('https://propertyadvantage.net/getaddress.php', params=params).json()
            subdistrict = ''.join(map(str,str(postdata['addr_sub_district']).split(' ')))
            for sd in subdistricts:
                if subdistrict in ''.join(map(str,str(sd['district_name'].split(' ')[0]).split(' '))):
                    data['Subdistrict'] = sd['district_id']
                    break
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:71.0) Gecko/20100101 Firefox/71.0',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Content-Type': 'multipart/form-data; boundary=---------------------------9886700451728219814370362055',
                'Origin': 'https://propertyadvantage.net',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Referer': 'https://propertyadvantage.net/edit_property?id=148074',
                'Upgrade-Insecure-Requests': '1',
            }
            params = (
                ('id', postdata['post_id']),
            )
            data = urllib3.encode_multipart_formdata(data,boundary='---------------------------9886700451728219814370362055')[0].decode("utf-8")
            response = httprequestObj.http_post('https://propertyadvantage.net/edit_property', headers=headers, params=params, data=data.encode("utf-8"))
        
            mapurl = 'https://propertyadvantage.net/edit_map?id={}'.format(postdata['post_id'])
            httprequestObj.http_get(mapurl)
            map_data = {
                'action': 'addmap',
                'lat_value': postdata['geo_latitude'],
                'lon_value': postdata['geo_longitude'],
                'zoom_value': '0',
                'id_value': postdata['post_id']
            }
            response = requests.post('https://propertyadvantage.net/process_function.php', data=map_data)

            imgurl = 'https://propertyadvantage.net/add_img?id={}'.format(postdata['post_id'])
            httprequestObj.http_get(imgurl)
            
            files = {}
            imgtags = []
            allimages = postdata["post_images"]
            #print(allimages)
            for i in range(len(allimages)):
                r = open(os.getcwd()+"/"+allimages[i], 'rb')
                files['photoimg[]'] = r
                response = httprequestObj.http_post('https://propertyadvantage.net/ajax_img.php',data=None, files=files)
                #print(response.text)
                soup = BeautifulSoup(response.content, features='html.parser')
                if soup.find('li') != None:
                    imgtags.append(soup.find('li').attrs.get('id').split('_')[-1])
                
                          
            data = {
                'ids': ''
            }
            data['ids'] = ','.join(map(str,imgtags))
            response = httprequestObj.http_post('https://propertyadvantage.net/orderupdate.php', data=data)
                        
            result['detail'] = "Post Edited Succesfully"
            result['success'] = "true"

        else:
            result['success'] = "false"
            result['detail'] = 'cannot login'

        end_time = datetime.datetime.utcnow()     
        result['end_time'] = str(end_time)
        result['usage_time'] = str(end_time - start_time)

        return {
            "success": result['success'],
            "usage_time": result['usage_time'],
            "start_time": result['start_time'],
            "end_time": result['end_time'],
            "post_id": postdata["post_id"],
            "ds_id": postdata["ds_id"],
            "log_id": postdata['log_id'],
            "account_type": "null",
            "detail": result['detail'],
            "websitename": "propertyadvantage"
        }





    def create_post(self,postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        start_time = datetime.datetime.utcnow()

        test_login = self.test_login(postdata)
        result =  {
            "success": test_login['success'],
            "usage_time": '',
            "start_time": str(start_time),
            "end_time": '',
            "post_url": '',
            "ds_id": str(postdata['ds_id']),
            "post_id": '',
            "account_type": "null",
            "detail": '',
            "websitename": "propertyadvantage"
        }

        if test_login['success'] == "true":

            r = httprequestObj.http_get("https://propertyadvantage.net/add_property")

            if 'web_project_name' not in postdata or postdata['web_project_name'] is None:
                if 'project_name' in postdata and postdata['project_name'] is not None:
                    postdata['web_project_name'] = postdata['project_name']
                else:
                    postdata['web_project_name'] = postdata['post_title_th']
            
            prod_address = ""
            for add in [postdata['addr_soi'], postdata['addr_road'], postdata['addr_sub_district'], postdata['addr_district'], postdata['addr_province']]:
                if add is not None:
                    prod_address += add + " "
            prod_address = prod_address[:-1]  

    
        
            data = {
                'action': 'addpost',
                'p_name': postdata['post_title_th'],
                'p_project': postdata['web_project_name'],
                'p_cate': '',
                'p_section': '',
                'p_number': prod_address,
                'p_soi': postdata['addr_soi'],
                'p_road': postdata['addr_road'],
                'p_province': '64',
                'p_district': '864',
                'p_subdistrict': '7785',
                'p_price': '',
                'p_area': '',
                'p_layer': '',
                'p_room': postdata['bed_room'],
                'p_toilet': postdata['bath_room'],
                'p_detail': postdata['post_description_th'],
                'p_tag': '',
                'p_facility': '',
                'p_around': 'undefined'
            }

            if postdata['listing_type'] == 'ขาย':
                data['p_cate'] = '1'
            else:
                data['p_cate'] = '2'

            pd_properties = {
                '1': '4',
                '2': '1',
                '3': '1',
                '4': '2',
                '5': '12',
                '6': '6',
                '7': '5',
                '8': '7',
                '9': '10',
                '10': '8',
                '25': '8' 
            }
            
            data['p_section'] = pd_properties[str(postdata['property_type'])]

            data['p_price'] = str(postdata['price_baht'])
            
            if data['p_section'] == '4':
                data['p_area'] = str(postdata['floor_area']) + 'ตร.ม.'
            else:
                if postdata['land_size_rai'] == None:
                    postdata['land_size_rai'] = '0'
                if postdata['land_size_ngan'] == None:
                    postdata['land_size_ngan'] = '0'
                if postdata['land_size_wa'] == None:
                    postdata['land_size_wa'] = '0'
                rai = str(postdata['land_size_rai']) + 'ไร่'
                ngan = str(postdata['land_size_ngan']) + 'งาน'
                square_wah = str(postdata['land_size_wa']) + 'ตารางวา'
                data['p_area'] = rai + ngan + square_wah

            fp = open('./static/propertyadvantage_province.json')
            provinces = json.load(fp)

            province = ''.join(map(str,str(postdata['addr_province']).split(' ')))
            for item in provinces.items():
                if province in ''.join(map(str,str(item[0]).split(' '))):
                    data['p_province'] = item[1]  
                    break 
            
            params = (
                ('ID', data['p_province']),
                ('TYPE', 'District'),
            )
            
            districts = httprequestObj.http_get('https://propertyadvantage.net/getaddress.php', params= params).json()
            district = ''.join(map(str,str(postdata['addr_district']).split(' ')))
            for d in districts:
                if district in ''.join(map(str,str(d['amphur_name'].split(' ')[0]).split(' '))):
                    data['p_district'] = d['amphur_id']
                    break
            
            params = (
                ('ID', '864'),
                ('TYPE', 'Subdistrict'),
            )

            subdistricts = httprequestObj.http_get('https://propertyadvantage.net/getaddress.php', params=params).json()
            subdistrict = ''.join(map(str,str(postdata['addr_sub_district']).split(' ')))
            for sd in subdistricts:
                if subdistrict in ''.join(map(str,str(sd['district_name'].split(' ')[0]).split(' '))):
                    data['p_subdistrict'] = sd['district_id']
                    break

            
            post_id = httprequestObj.http_post('https://propertyadvantage.net/process_function.php', data=data).text
            map_data = {
                'action': 'addmap',
                'lat_value': postdata['geo_latitude'],
                'lon_value': postdata['geo_longitude'],
                'zoom_value': '0',
                'id_value': post_id
            }
            post_id = httprequestObj.http_post('https://propertyadvantage.net/process_function.php', data=map_data).text                        
            post_url = "https://propertyadvantage.net/property/{}-{}".format(post_id,data['p_name'])
            imgurl = 'https://propertyadvantage.net/add_img?id={}'.format(post_id)
            httprequestObj.http_get(imgurl)

            files = {}
            imgtags = []
            allimages = postdata["post_images"][:5]
            #print(allimages)
            for i in range(len(allimages)):
                r = open(os.getcwd()+"/"+allimages[i], 'rb')
                files['photoimg[]'] = r
                response = httprequestObj.http_post('https://propertyadvantage.net/ajax_img.php',data=None, files=files)
                #print(response.text)
                soup = BeautifulSoup(response.content, features='html.parser')
                if soup.find('li') != None:
                    imgtags.append(soup.find('li').attrs.get('id').split('_')[-1])
            
            
            data = {
                'ids': ''
            }
            data['ids'] = ','.join(map(str,imgtags))

            response = httprequestObj.http_post('https://propertyadvantage.net/orderupdate.php', data=data)
        
            result['post_url'] = post_url
            result['post_id'] = post_id
            result['detail'] = "Post Created Succesfully"
            result['success'] = "true"

        else:
            result['success'] = "false"
            result['detail'] = 'cannot login'

        end_time = datetime.datetime.utcnow()     
        result['end_time'] = str(end_time)
        result['usage_time'] = str(end_time - start_time)

        return {
            "success": result['success'],
            "usage_time": result['usage_time'],
            "start_time": result['start_time'],
            "end_time": result['end_time'],
            "post_url": result['post_url'],
            "ds_id": result['ds_id'],
            "post_id": result['post_id'],
            "account_type": result['account_type'],
            "detail": result['detail'],
            "websitename": result['websitename']
        }

    
    def delete_post(self, postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        start_time = datetime.datetime.utcnow()

        test_login = self.test_login(postdata)
        
        result = {
            "success": test_login["success"],
            "usage_time": '',
            "start_time": str(start_time),
            "end_time": '',
            "detail": '',
            "websitename": "propertyadvantage",
            "log_id": postdata['log_id']
        }
        if test_login['success'] == "true":
            r = httprequestObj.http_get('https://propertyadvantage.net/maneg_property') 
            soup = BeautifulSoup(r.content,features='html.parser')
            postids = []
            if soup.find('ul',attrs={'class':'pagination'}):
                pages = []
                lis = soup.find('ul',attrs={'class':'pagination'}).find_all('li')[:-1]
                for li in  lis:
                    pages.append(li.text)
                for page in pages:
                    url = 'https://propertyadvantage.net/maneg_property.php?&page={}'.format(int(page)-1)
                    r = httprequestObj.http_get(url) 
                    soup = BeautifulSoup(r.content,features='html.parser')
                    tablerows = soup.find('table',attrs={'class':'table table-striped'}).find('tbody').find_all('tr')
                    for tr in tablerows:
                        id = tr.find('a',attrs={'href':'#'}).attrs.get('onclick')
                        postids.append(re.search(r'\d+', id).group())
            
            else:
                tablerows = soup.find('table',attrs={'class':'table table-striped'}).find('tbody').find_all('tr')
                for tr in tablerows:
                    id = tr.find('a',attrs={'href':'#'}).attrs.get('onclick')
                    postids.append(re.search(r'\d+', id).group())

            
            postid = postdata['post_id']
            if postid not in postids:
                result['success'] = "false"
                result['detail'] = 'No post found with given id.'
            else:
                delete_url = 'https://propertyadvantage.net/maneg_property?delete={}'.format(postdata['post_id'])
                httprequestObj.http_get(delete_url)
                result['success'] = "true"
                result['detail'] = "Post deleted successfully."         

        else:
            result['success'] = "false"
            detail = "cannot login"

        end_time = datetime.datetime.utcnow()     
        result['end_time'] = str(end_time)
        result['usage_time'] = str(end_time - start_time)

        return {
            "success": result["success"],
            "usage_time": result["usage_time"],
            "start_time": result["start_time"],
            "end_time": result["end_time"],
            "detail": result['detail'],
            "websitename": "propertyadvantage",
            "post_id": postdata["post_id"],
            "ds_id": postdata["ds_id"],
            "log_id": postdata['log_id']
        } 

    def boost_post(self,postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        start_time = datetime.datetime.utcnow()

        test_login = self.test_login(postdata)
        
        result = {
            "success": test_login["success"],
            "usage_time": '',
            "start_time": str(start_time),
            "end_time": '',
            "detail": '',
            "websitename": "propertyadvantage",
            "log_id": postdata['log_id']
        }
        if test_login['success'] == "true":
            r = httprequestObj.http_get('https://propertyadvantage.net/maneg_property') 
            soup = BeautifulSoup(r.content, features='html.parser')
            postids = []
            posturls = []
            
            if soup.find('ul',attrs={'class':'pagination'}):
                max_pages = 0
                lis = soup.find('ul',attrs={'class':'pagination'}).find_all('li')[:-1]
                for li in  lis:
                    max_pages = max(max_pages, int(li.text.replace('.','').strip()))
                
                for page in range(1, max_pages+1):
                    url = 'https://propertyadvantage.net/maneg_property.php?&page={}'.format(int(page)-1)
                    r = httprequestObj.http_get(url) 
                    soup = BeautifulSoup(r.content,features='html.parser')
                    tablerows = soup.find('table',attrs={'class':'table table-striped'}).find('tbody').find_all('tr')

                    for tr in tablerows:
                        id = tr.find('a',attrs={'href':'#'}).attrs.get('onclick')
                        postids.append(re.search(r'\d+', id).group())
                        posturls.append(tr.find('a',attrs={'target':'_blank'}).attrs.get('href'))
            
            else:
                tablerows = soup.find('table',attrs={'class':'table table-striped'}).find('tbody').find_all('tr')

                for tr in tablerows:
                    id = tr.find('a',attrs={'href':'#'}).attrs.get('onclick')
                    postids.append(re.search(r'\d+', id).group())
                    posturls.append(tr.find('a',attrs={'target':'_blank'}).attrs.get('href'))

            
            print(postids)
            postid = postdata['post_id']
            if postid not in postids:
                result['success'] = "false"
                result['detail'] = 'No post found with given id.'
            else:
                postidx = postids.index(postid)
                post_url = posturls[postidx]
                print(post_url)
                httprequestObj.http_get(post_url)
                result['success'] = "true"
                result['detail'] = "Post boosted successfully."
       

        else:
            result['success'] = "false"
            detail = "cannot login"

        end_time = datetime.datetime.utcnow()     
        result['end_time'] = str(end_time)
        result['usage_time'] = str(end_time - start_time)

        return {
            "success": result["success"],
            "usage_time": result["usage_time"],
            "start_time": result["start_time"],
            "end_time": result["end_time"],
            "detail": result['detail'],
            "websitename": "propertyadvantage",
            "post_id": postdata["post_id"],
            "ds_id": postdata["ds_id"],
            "log_id": postdata['log_id'],
        }


    def search_post(self,postdata):
        self.print_debug('function ['+sys._getframe().f_code.co_name+']')
        start_time = datetime.datetime.utcnow()

        test_login = self.test_login(postdata)

        result = {
            "success": test_login['success'],
            "usage_time": '',
            "start_time": str(start_time),
            "end_time": '',
            "detail": '',
            "websitename": "propertyadvantage",
            "account_type":None,
            "ds_id": postdata['ds_id'],
            "log_id": postdata['log_id'],
            "post_id": '',
            "post_create_time": '',
            "post_modify_time": '',
            "post_view": '',
            "post_url": '',
            "post_found": "false"
        }

        if test_login['success'] == "true":
            r = httprequestObj.http_get('https://propertyadvantage.net/maneg_property') 
            soup = BeautifulSoup(r.content,features='html.parser')
            post_titles,post_urls,post_ids,post_views = [],[],[],[]

            if soup.find('ul',attrs={'class':'pagination'}):
                pages = []
                lis = soup.find('ul',attrs={'class':'pagination'}).find_all('li')[:-1]
                for li in  lis:
                    pages.append(li.text)
                for page in pages:
                    url = 'https://propertyadvantage.net/maneg_property.php?&page={}'.format(int(page)-1)
                    r = httprequestObj.http_get(url) 
                    soup = BeautifulSoup(r.content,features='html.parser')
                    tablerows = soup.find('table',attrs={'class':'table table-striped'}).find('tbody').find_all('tr')
                    for tr in tablerows:
                        post_titles.append(tr.find('a',attrs={'target':'_blank'}).text)
                        post_urls.append(tr.find('a',attrs={'target':'_blank'}).attrs.get('href'))
                        post_ids.append(tr.find('a',attrs={'target':'_blank'}).attrs.get('href').split('-')[0].split('/')[-1])
                        post_views.append(str(tr.find("p",attrs={'class':'gray'}).text))
            else:
                tablerows = soup.find('table',attrs={'class':'table table-striped'}).find('tbody').find_all('tr')
                for tr in tablerows:
                    post_titles.append(tr.find('a',attrs={'target':'_blank'}).text)
                    post_urls.append(tr.find('a',attrs={'target':'_blank'}).attrs.get('href'))
                    post_ids.append(tr.find('a',attrs={'target':'_blank'}).attrs.get('href').split('-')[0].split('/')[-1])
                    post_views.append(str(tr.find("p",attrs={'class':'gray'}).text))

            
            if postdata['post_title_th'] in post_titles:
                idx = post_titles.index(postdata['post_title_th'])
                result['post_id'] = post_ids[idx]
                result['post_url'] = post_urls[idx]
                result['detail'] = "Post Found"
                result['post_found'] = "true"
                result['post_view'] = post_views[idx]
            else:
                result['success'] = "false"
                result['detail'] = "No post found with given title"

        else:
            result['success'] = "false"
            result['detail'] = "cannot login"
        
        end_time = datetime.datetime.utcnow()     
        result['end_time'] = str(end_time)
        result['usage_time'] = str(end_time - start_time)

        return {
            "success": test_login['success'],
            "usage_time": result['usage_time'],
            "start_time": result['start_time'],
            "end_time": result['end_time'],
            "detail": result['detail'],
            "websitename": "propertyadvantage",
            "account_type":None,
            "ds_id": postdata['ds_id'],
            "log_id": postdata['log_id'],
            "post_id": result['post_id'],
            "post_create_time": '',
            "post_modify_time": '',
            "post_view": result['post_view'],
            "post_url": result['post_url'],
            "post_found": result['post_found']
        }
        


    def print_debug(self, msg):
        if(self.debug == 1):
            print(msg)
        return True

    def print_debug_data(self, data):
        if(self.debugdata == 1):
            print(data)
        return True

        if(self.debugdata == 1):
            print(data)
        return True