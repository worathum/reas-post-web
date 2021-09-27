# SEND username for login, not email
import json
import re
from itertools import count
from os import getcwd
from typing import Dict, List, Tuple

from bs4 import BeautifulSoup

from .lib_httprequest import *
from .lib_utils import *

httprequestObj = lib_httprequest()


class house4post:
    def __init__(self):
        try:
            import configs
        except ImportError:
            configs = {}

        self.encoding = "utf-8"
        self.imgtmp = "imgtmp"
        self.debug = 0
        self.debugresdata = 0
        self.parser = "html.parser"
        self.website_name = "house4post"

    def logout_user(self):
        url = "https://www.house4post.com/logout_member"
        httprequestObj.http_get(url)

    """
    def register_user(self, data):
        self.logout_user()
        start_time = datetime.datetime.utcnow()
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36"
        }
        success = "true"
        detail = ""
        postdata = {}
        postdata["username"] = data["user"].split("@")[0]
        postdata["pass"] = postdata["conpass"] = data["pass"]
        postdata["email"] = data["user"]
        postdata["name"] = data["name_th"]
        postdata["lastname"] = data["surname_th"]
        postdata["phone"] = data["tel"]
        postdata["address"] = "พญาไท,กรุงเทพ"
        postdata["submit"] = ""
        regex = "^\\w+([\\.-]?\\w+)*@\\w+([\\.-]?\\w+)*$"
        f1 = True
        regex = "^\\w+([\\.-]?\\w+)*@\\w+([\\.-]?\\w+)*$"
        if re.search(regex, postdata["email"]):
            f1 = True
        else:
            f1 = False
        if f1 == False:
            success = "false"
            detail = "Invalid email"
        if (
            postdata["username"] == ""
            or postdata["pass"] == ""
            or postdata["name"] == ""
            or postdata["lastname"] == ""
            or postdata["phone"] == ""
        ):
            success = "false"
            detail = "Empty credentials"
        if success == "true":
            url = "https://www.house4post.com/signup_member.php"
            req = httprequestObj.http_post(url, data=postdata, headers=headers)
            txt = str(req.text)
            if txt.find("สมัครสมาชิกเรียบร้อยแล้ว") == -1:
                success = "false"
                detail = "Already a user"
            else:
                success = "true"
                detail = "Successfully Registered"
        end_time = datetime.datetime.utcnow()
        result = {
            "websitename": "house4post",
            "success": success,
            "start_time": str(start_time),
            "end_time": str(end_time),
            "usage_time": str(end_time - start_time),
            "detail": detail,
            "ds_id": data["ds_id"],
        }
        return result
    """

    @serialize_dict
    @timeit_to_dict()
    def register_user(self, postdata: Dict[str, str]) -> Dict[str, str]:
        self.logout_user()

        result = {
            "websitename": self.website_name,
            "success": False,
            "detail": "",
            "ds_id": postdata["ds_id"],
        }

        payload = {
            "username": postdata["user"].split("@")[0],
            "pass": postdata["pass"],
            "conpass": postdata["pass"],
            "email": postdata["user"],
            "name": postdata["name_th"],
            "lastname": postdata["surname_th"],
            "phone": postdata["tel"],
            "address": "พญาไท,กรุงเทพ",
            "submit": "",
        }

        if not all(
            [
                payload.get(key)
                for key in ["username", "pass", "name", "lastname", "phone"]
            ]
        ):
            result["detail"] = "Empty credentials"
            return result

        EMAIL_REGEX = r"^\\w+([\\.-]?\\w+)*@\\w+([\\.-]?\\w+)*$"
        if not re.search(EMAIL_REGEX, result["email"]):
            result["detail"] = "Invalid email"
            return result

        url = "https://www.house4post.com/signup_member.php"
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36"
        }
        response = httprequestObj.http_post(url, data=payload, headers=headers)

        if "สมัครสมาชิกเรียบร้อยแล้ว" in response.text:
            result["success"] = True
            result["detail"] = "Successfully Registered"
        else:
            result["detail"] = "Already a user"

        return result

    @serialize_dict
    @timeit_to_dict()
    def test_login(self, postdata: Dict[str, str]) -> Dict[str, str]:
        self.logout_user()

        result = {
            "websitename": self.website_name,
            "success": False,
            "ds_id": postdata["ds_id"],
            "detail": "Cannot Login",
        }

        payload = {
            "log_u": postdata["user"].split("@")[0],
            "log_p": postdata["pass"],
            "submit": "Login",
        }

        url = "https://www.house4post.com/login.php"
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36"
        }
        response = httprequestObj.http_post(url, data=payload, headers=headers)

        if "Username หรือ Password ไม่ถูกต้อง" in response.text:
            result["detail"] = "User not registered yet"
        else:
            result["success"] = True
            result["detail"] = "Successfully login"

        return result

    @serialize_dict
    @timeit_to_dict()
    def create_post(self, postdata: Dict[str, str]) -> Dict[str, str]:
        login_result = self.test_login(postdata)

        result = {
            "websitename": self.website_name,
            "success": False,
            "post_url": "",
            "post_id": "",
            "account_type": "null",
            "ds_id": postdata["ds_id"],
            "detail": login_result["detail"],
        }

        if login_result["success"] == "false":
            return result

        payload = self.prepare_postdata(postdata)

        url = "https://www.house4post.com/add_property.php"
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36"
        }
        try:
            response = httprequestObj.http_post(url, data=payload, headers=headers)
        except Exception as e:
            result["detail"] = f"Some thing went wrong when post: {e}"
            return result
        soup = BeautifulSoup(response.content, "html.parser")

        try:
            post_id = soup.find(class_="well").meta["content"].split("=")[-1]  # type: ignore
        except (AttributeError, KeyError):
            result["success"] = False
            alert = soup.find(class_="alert-danger")
            if alert:
                result["detail"] = alert.get_text(strip=True)  # type: ignore
            else:
                result["detail"] = "Network error"
            return result

        post_url = f"https://www.house4post.com/idasungha-{post_id}-{postdata['post_title_th']}"
        post_url = post_url.replace(" ", "-")

        if not postdata.get("post_images"):
            postdata["post_images"] = ["./imgtmp/default/white.jpg"]  # type: ignore

        try:
            img_url = f"https://www.house4post.com/add_img.php?id={post_id}"
            httprequestObj.http_get(img_url)
            for img in postdata["post_images"][:6]:
                with open(getcwd() + "/" + img, "rb") as r:
                    response = httprequestObj.http_post(
                        "https://www.house4post.com/ajax_img.php",
                        data=None,
                        files={"photoimg": r},
                    )
                    time.sleep(3)
        except Exception as e:
            result["detail"] = f"Some thing went wrong when upload img: {e}"
            return result

        result["post_url"] = post_url
        result["post_id"] = post_id
        result["detail"] = "Successful post"
        result["success"] = True

        return result

    def prepare_postdata(self, postdata: Dict[str, str]) -> Dict[str, str]:
        try:
            if postdata.get("web_project_name", ""):
                project = postdata["web_project_name"]
            else:
                project = postdata["project_name"]
        except KeyError:
            project = postdata["post_title_th"]

        province_id, district_id, subdistrict_id = self._get_address_id(
            postdata["addr_province"],
            postdata["addr_district"],
            postdata["addr_sub_district"],
        )

        area = ""
        if postdata.get("land_size_rai"):
            area += f"{postdata['land_size_rai']} ไร่"
        if postdata.get("land_size_ngan"):
            area += f"{postdata['land_size_ngan']} งาน"
        if postdata.get("land_size_wa"):
            area += f"{postdata['land_size_wa']} ตรว"
        if postdata.get("floor_area"):
            area += f"{postdata['floor_area']} ตรม"

        payload = {
            "name": postdata["post_title_th"],
            "project": project,
            "cate": "1" if postdata["listing_type"] == "ขาย" else "2",
            "section": self._get_postdata_section(postdata["property_type"]),
            "number": "",
            "soi": postdata.get("addr_soi", ""),
            "road": postdata.get("addr_road", ""),
            "Province": province_id,
            "District": district_id,
            "Subdistrict": subdistrict_id,
            "price": postdata["price_baht"],
            "area": area,
            "layer": postdata.get("floor_total", ""),
            "room": postdata.get("bed_room", ""),
            "toilet": postdata.get("bath_room", ""),
            "detail": postdata.get("post_description_th", ""),
            "Submit": "Submit",
        }

        return payload

    def _get_postdata_section(self, property_type: str) -> str:
        if not isinstance(property_type, str):
            property_type = str(property_type)
        property_type_id = {
            "คอนโด": "1",
            "บ้านเดี่ยว": "2",
            "บ้านแฝด": "3",
            "ทาวน์เฮ้าส์": "4",
            "ตึกแถว-อาคารพาณิชย์": "5",
            "ที่ดิน": "6",
            "อพาร์ทเมนท์": "7",
            "โรงแรม": "8",
            "ออฟฟิศสำนักงาน": "9",
            "โกดัง-โรงงาน": "10",
            "โรงงาน": "25",
        }
        property_id_map = {
            "1": "1",
            "2": "5",
            "3": "15",
            "4": "3",
            "5": "2",
            "6": "4",
            "7": "7",
            "8": "13",
            "9": "9",
            "10": "8",
            "25": "10",
        }
        try:
            return property_id_map[property_type_id[property_type]]
        except KeyError:
            return property_id_map[property_type]

    def _get_address_id(
        self, province: str, district: str, subdistrict: str
    ) -> Tuple[int, int, int]:
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36"
        }
        response = httprequestObj.http_get_with_headers(
            "https://www.house4post.com/add_property", headers=headers
        )
        soup = BeautifulSoup(response.content, "html.parser")
        options = soup.find("select", {"name": "Province"}).find_all("option")  # type: ignore
        province_id = int(options[0]["value"] or 0)  # type: ignore
        for opt in options:
            if province.strip() in opt.get_text(strip=True):  # type: ignore
                province_id = int(opt["value"])  # type: ignore
                break

        url = (
            f"https://www.house4post.com/getaddress.php?ID={province_id}&TYPE=District"
        )
        response = httprequestObj.http_get_with_headers(url, headers=headers)
        district_json: List[Dict[str, str]] = json.loads(response.content)
        district_id = int(district_json[0]["amphur_id"])
        for dist in district_json:
            if district.strip() in dist["amphur_name"].strip():
                district_id = int(dist["amphur_id"])

        url = f"https://www.house4post.com/getaddress.php?ID={district_id}&TYPE=Subdistrict"
        response = httprequestObj.http_get_with_headers(url, headers=headers)
        subdistrict_json: List[Dict[str, str]] = json.loads(response.content)
        subdistrict_id = int(subdistrict_json[0]["district_id"])
        for subdist in subdistrict_json:
            if subdistrict.strip() in subdist["district_name"].strip():
                subdistrict_id = int(subdist["district_id"])

        return province_id, district_id, subdistrict_id

    @serialize_dict
    @timeit_to_dict()
    def delete_post(self, postdata):
        login_info = self.test_login(postdata)

        result = {
            "websitename": self.website_name,
            "success": False,
            "post_id": postdata["post_id"],
            "log_id": postdata["log_id"],
            "ds_id": postdata["ds_id"],
            "detail": "",
        }

        if login_info["success"] == "false":
            result["detail"] = "Cannot login"
            return result

        url = (
            f"https://www.house4post.com/maneg_property.php?delete={result['post_id']}"
        )
        response = httprequestObj.http_get_with_headers(url)

        if "ลบรายการที่เลือกเรียบร้อยแล้ว" in response.text:
            result["detail"] = "Successfully deleted"
            result["success"] = True
        else:
            result["detail"] = "Network error"

        return result

    @serialize_dict
    @timeit_to_dict()
    def search_post(self, postdata: Dict[str, str]) -> Dict[str, str]:
        login_info = self.test_login(postdata)

        result = {
            "websitename": self.website_name,
            "success": False,
            "detail": "No post found with given title",
            "account_type": "null",
            "ds_id": postdata["ds_id"],
            "log_id": postdata["log_id"],
            "post_create_time": "",
            "post_modify_time": "",
            "post_view": "",
            "post_id": "",
            "post_url": "",
            "post_found": False,
        }

        if login_info["success"] == "false":
            result["detail"] = "Cannot login"
            return result

        page = count(0)
        while True:
            response = httprequestObj.http_get(
                f"https://www.house4post.com//maneg_property.php?&page={next(page)}"
            )
            if response.status_code != 200:
                break

            soup = BeautifulSoup(response.text, features=self.parser)
            posts_element = soup.find(class_="well")
            try:
                posts = posts_element.find("tbody").find_all("tr")  # type: ignore
            except AttributeError:
                continue
            for post in posts:
                title = post.find_all("td")[1].a  # type: ignore
                title_text = title.get_text().strip()
                if title_text == str(postdata["post_title_th"]).strip():
                    result["post_found"] = True
                    result["detail"] = "Post found successfully"
                    post_url = title.get("href")
                    result["post_url"] = post_url
                    result["post_id"] = re.findall(r"idasungha-(\d+)", post_url)[0]
                    break  # for post in posts:

            if len(posts) < 10 or result["post_found"]:
                break

        return result

    @serialize_dict
    @timeit_to_dict()
    def edit_post(self, data):
        result = self.test_login(data)
        success = result["success"]
        detail = result["detail"]
        post_url = ""
        post_id = data["post_id"]

        """if success == 'true':
            post_found = False
            page_num = 0
            flag = True
            while flag:
                response = httprequestObj.http_get('https://www.house4post.com//maneg_property.php?&page='+str(page_num))
                if response.status_code==200:
                    soup = BeautifulSoup(response.text, features=self.parser)
                    posts_element = soup.find(class_='well')             
                    
                    if posts_element and posts_element.find('tbody'): 
                        posts = posts_element.find('tbody').find_all('tr')
                        if len(posts)<10:
                            flag = False
                        for post in posts:
                            id_link = post.find_all('td')[-1].a
                            id = id_link.get('href').split("id=")[-1]
                            if id==post_id:
                                post_found = True
                                break
                    else:
                        break
                page_num += 1

            # headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'}
            # url = 'https://www.house4post.com/maneg_property.php'
            # valid_ids = []
            # req = httprequestObj.http_get_with_headers(url, headers=headers)
            # soup = BeautifulSoup(req.text, 'html.parser')
            # total_pages = 1
            # if soup.find('ul', {'class': 'pagination'}) != None:
            #     total_pages = len(soup.find('ul', {'class': 'pagination'}).findAll('li'))
            #     if total_pages > 0:
            #         total_pages -= 1
            # for i in range(total_pages):
            #     url = 'https://www.house4post.com/maneg_property.php?&page=' + str(i)
            #     req = httprequestObj.http_get_with_headers(url, headers=headers)
            #     soup = BeautifulSoup(req.text, 'html.parser')
            #     posts = soup.find('table', {'class': 'table table-striped'}).find('tbody').findAll('tr')
            #     for post in posts:
            #         id = ''
            #         a = str(post.find('a')['href'])
            #         print(a)
            #         ind = a.find('-') + 1
            #         while a[ind] != '-':
            #             id += a[ind]
            #             ind += 1

            #         valid_ids.append(id)

            # print(valid_ids)
            if not post_found:
                success = 'false'
                detail = 'No post found with given id'
            else:
                self.delete_post(data)
                success, detail, post_url, post_id = self.create_post(data, to_edit=1)
                detail = 'Successfully edited'"""
        try:
            self.delete_post(data)
            edit_result = self.create_post(data)
            success = edit_result["success"]
            detail = edit_result["detail"]
            post_url = edit_result["post_url"]
            post_id = edit_result["post_id"]
            detail = "Successfully edited"
        except:
            success = "false"
            detail = "No post found with given id"

        result = {
            "success": success,
            "post_url": post_url,
            "post_id": post_id,
            "account_type": "null",
            "ds_id": data["ds_id"],
            "log_id": data["log_id"],
            "detail": detail,
            "websitename": self.website_name,
        }
        return result

    @serialize_dict
    @timeit_to_dict()
    def boost_post(self, data):
        post_id = data["post_id"]
        log_id = data["log_id"]
        result = self.test_login(data)
        success = result["success"]
        detail = result["detail"]
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36"
        }
        url = "https://www.house4post.com/maneg_property.php"
        valid_ids = []
        req = httprequestObj.http_get_with_headers(url, headers=headers)
        soup = BeautifulSoup(req.text, "html.parser")
        total_pages = 1
        if soup.find("ul", {"class": "pagination"}) != None:
            total_pages = len(soup.find("ul", {"class": "pagination"}).findAll("li"))
            if total_pages > 0:
                total_pages -= 1
        for i in range(total_pages):
            url = "https://www.house4post.com/maneg_property.php?&page=" + str(i)
            req = httprequestObj.http_get_with_headers(url, headers=headers)
            soup = BeautifulSoup(req.text, "html.parser")
            posts = (
                soup.find("table", {"class": "table table-striped"})
                .find("tbody")
                .findAll("tr")
            )
            for post in posts:
                id = ""
                a = str(post.find("a")["href"])
                ind = a.find("-") + 1
                while a[ind] != "-":
                    id += a[ind]
                    ind += 1

                valid_ids.append(id)

        if str(post_id) not in valid_ids:
            success = "false"
            detail = "Invalid id"
        if success == "true":
            url = "https://www.house4post.com/maneg_property.php?refresh=" + str(
                post_id
            )
            req = httprequestObj.http_get_with_headers(url, headers=headers)
            txt = req.text
            if txt.find(" เลื่อนประกาศเรียบร้อยแล้ว") == -1:
                success = "false"
                detail = "Postpone failed"
            else:
                success = "true"
                detail = "Successfully postponed"
        result = {
            "success": "true",
            "detail": detail,
            "ds_id": data["ds_id"],
            "log_id": log_id,
            "post_id": post_id,
            "websitename": "house4post",
        }
        return result
