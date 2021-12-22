# -*- coding: utf-8 -*-

class sample():

    name = 'sample'

    def __init__(self, params):        
        self.web_name = params["web_name"]
        self.login_user = params["login_user"]
        self.login_pass = params["login_pass"]      
        self.email = params["email"]
        self.post_id = params["post_id"]

    def get_test_login_json_string(self):
        json_string = '''
            {
                "action": "test_login",
                "timeout": "7",
                "web": [
                    {
                        "ds_name": "''' + self.web_name + '''",
                        "ds_id": "4",
                        "user": "''' + self.login_user + '''",
                        "pass": "''' + self.login_pass + '''"                        
                    }
                ]
            }
            '''
        return json_string

    def get_register_json_string(self):
        json_string = '''
            {
                "action": "register_user",
                "timeout": "7",
                "web": [
                    {
                        "ds_name": "''' + self.web_name + '''",
                        "ds_id": "4",
                        "user": "''' + self.login_user + '''",
                        "pass": "''' + self.login_pass + '''",
                        "email": "''' + self.email + '''",
                        "company_name": "amarin inc",
                        "name_title": "mr",
                        "name_th": "อัมรินทร์",
                        "surname_th": "บุญเกิด",
                        "name_en": "Amarinxyz",
                        "surname_en": "Boonkirt",
                        "tel": "0891999450",
                        "line": "amarin.ta",
                        "addr_province" : "nonthaburi"            
                    }
                ]
            }
            '''
        return json_string
        
    def get_create_post_json_string(self):
        json_string = '''
            {
            "action": "create_post",
            "timeout": "5",
            "post_img_url_lists": [
                "https://storage.googleapis.com/reas-240123.appspot.com/property/images/PR_aa00000442842_86e8f4ee-5b68-4db4-b880-e228469f592d.jpg",
                "https://storage.googleapis.com/reas-240123.appspot.com/property/images/PR_aa00000442842_59ba30c3-40ef-4cca-a6ad-a6f9072c6b8b.jpg",
                "https://storage.googleapis.com/reas-240123.appspot.com/property/images/PR_aa00000442842_7d339cee-d097-4bc8-bde3-09d16e10c24b.jpg",
                "https://storage.googleapis.com/reas-240123.appspot.com/property/images/PR_aa00000442842_96f816c0-634d-4343-b1e7-b6e3a68233e2.jpg",
                "https://storage.googleapis.com/reas-240123.appspot.com/property/images/PR_aa00000442842_ed7933d8-54e0-4de6-8b91-9fb322db79bd.jpg",
                "https://storage.googleapis.com/reas-240123.appspot.com/property/images/PR_aa00000442842_930d9a2d-540f-4f97-bcd8-f5bd9074db4e.jpg",
                "https://storage.googleapis.com/reas-240123.appspot.com/property/images/PR_aa00000442842_f6d05ffd-0527-4bf4-964f-194ec2c0c150.jpg",
                "https://storage.googleapis.com/reas-240123.appspot.com/property/images/PR_aa00000442842_d069ecdb-d0f4-4b53-b37f-6dafc0839dff.jpg",
                "https://storage.googleapis.com/reas-240123.appspot.com/property/images/PR_aa00000442842_9225b49e-1b3c-45dd-ae3a-6e04f2b1790b.jpg",
                "https://storage.googleapis.com/reas-240123.appspot.com/property/images/PR_aa00000442842_c2197f82-5c7c-4483-9f61-8abb303d7716.jpg",
                "https://storage.googleapis.com/reas-240123.appspot.com/property/images/PR_aa00000442842_8ac8f6df-f1d5-4cfa-b963-ebb456fa4d70.jpg",
                "https://storage.googleapis.com/reas-240123.appspot.com/property/images/PR_aa00000442842_ebc251c9-ff77-466a-b50f-c8ac89e4d029.jpg"
            ],
            "geo_latitude": "13.884",
            "geo_longitude": "100.501",
            "property_id": "PR_aa00000442842",
            "post_title_th": "ให้เช่า บ้านเดี่ยว หลังมุม เศรษฐสิริ สนามบินน้ำ 120 ตร.วา สภาพดี",
            "short_post_title_th": "",
            "post_description_th": "ให้เช่า บ้านเดี่ยว หลังมุม เศรษฐสิริ สนามบินน้ำ 120 ตร.วา สภาพดี\r\n\r\nให้เช่า บ้านเดี่ยว หลังมุม หมู่บ้านเศรษฐสิริ สนามบินน้ำ\r\nบรรยากาศร่มรื่น ไม่พลุกพล่าน หมู่บ้านติดถ.สนามบิน้ำ ไม่ต้องเข้าซอย\r\nใกล้กองสลาก ใกล้เซ็นทรัลรัตนาธิเบศร์ ใกล้เดอะมอลล์งามวงศ์วาน\r\n\r\n:: ที่ตั้ง ::\r\nหมู่บ้านเศรษฐสิริ สนามบินน้ำ ซอย 9\r\nถ.สนามบินน้ำ ต.ท่าทราย อ.เมืองนนทบุรี จ.นนทบุรี\r\n\r\n::จุดเด่น::\r\nขนาดพื้นที่ 120 ตร.วา\r\nพื้นที่ใช้สอย 350 ตร.ม.\r\nบ้านหลังมุม\r\nหน้าบ้านหันทิศใต้\r\nจอดรถ 2 คัน\r\nสนามหญ้ากว้างมาก\r\n::ประกอบด้วย::\r\n3 ห้องนอน 4 ห้องน้ำ 1ห้องนั่งเล่น 1 ห้องทำงาน 1 ห้องอาหาร\r\n2 ห้องครัว 1 ห้องแม่บ้าน \r\nชั้น 2 มีโถงกลาง ทำเป็นห้องนั่งเล่นได้\r\nให้เช่าเป็นบ้านเปล่า มีเฟอร์นิเจอร์บางส่วน\r\nมีแอร์ 6 เครื่อง\r\nปูพื้นชั้นล่างกระเบื้อง - ชั้นบนเป็นปาร์เก้\r\n\r\n::รายละเอียดโครงการ::\r\nหมู่บ้านเศรษฐสิริ สนามบินน้ำ\r\nมีสระว่ายน้ำ ฟิตเนส สโมสร\r\n\r\n::สถานที่ใกล้เคียง::\r\n– ใกล้ห้างสรรพสินค้าเซ็นทรัล รัตนาธิเบศร์ ,เดอะมอลล์งามวงศ์วาน ,พันธ์ทิพย์งามวงศ์วาน ,Big C รัตนาธิเบศร์ ,Tesco Lotus \r\nแคราย ,เอสพลานาด แคราย ,ตลาดนกฮูก\r\n– ใกล้โรงพยาบาลพระนั่งเกล้า ,โรงพยาบาลเกษมราษฏร์ ประชาชื่น ,โรงพยาบาลบำราศนราดูร ,สถาบันโรคทรวงอก\r\n– ใกล้โรงเรียนศรีบุญยานนท์ ,มหาวิทยาลัยเทคโนโลยีราชมงคลสุวรรณภูมิ ,วิทยาลัยเทคโนโลยีสยามบริหารธุรกิจ\r\n– ใกล้ธนาคารทุกธนาคาร\r\n\r\n::พิกัด::\r\nhttps://goo.gl/maps/k7o8URq7M7FJ3Vic7\r\n\r\nค่าเช่า 40,000 บาท\r\nสัญญาขั้นต่ำ 1 ปี จ่ายล่วงหน้า 1 เดือน เงินประกัน 2 เดือน\r\n\r\nสนใจติดต่อ: ธนพร 092-514-1987 / 0 9 2 5 1 4 1 9 8 7\r\nLine I D: tkproperty987\r\nhttps://line.me/ti/p/tQDsEigadM\r\nบริการเป็นกันเอง ยินดีให้คำปรึกษาก่อนตัดสินใจซื้อ\r\nERA PROPERTY NETWORK",
            "post_title_en": "House for rent at the corner of Setthasiri Sanambinnam 120 sq. wa. Good condition.",
            "short_post_title_en": "",
            "post_description_en": "House for rent at the corner of Setthasiri Village Sanambinnam\r\nThe atmosphere is shady, not crowded, the village is next to Sanambinnam Rd. don't have to go into the alley\r\nnear the lottery, near Central Rattanathibet near The Mall Ngamwongwan\r\n\r\n:: Location ::\r\nSetthasiri Village, Sanambinnam Soi 9\r\nSanambinnam Rd., Tha Sai Subdistrict, Mueang Nonthaburi District, Nonthaburi Province\r\n\r\n::Highlights::\r\nArea size 120 sq wa\r\nUsable area 350 sq m.\r\ncorner house\r\nfront of the house facing south\r\nParking for 2 cars\r\nvery wide lawn\r\n\r\n::include::\r\n3 bedrooms, 4 bathrooms, 1 living room, 1 office room, 1 dining room\r\n2 kitchens, 1 maid's room\r\n2nd floor has a central hall that can be used as a living room.\r\nRent as an empty house have some furniture\r\nThere are 6 air conditioners.\r\nFloor tiles downstairs - upstairs is parquet.\r\n\r\n::Project details::\r\nSetthasiri Village, Sanambinnam\r\nThere is a swimming pool, fitness center and club.\r\n\r\n::Nearby Places::\r\n- Near Central Department Store, Rattanathibet, The Mall Ngamwongwan , Pantip Ngamwongwan, Big C \r\nRattanathibet, Tesco Lotus, Khae Rai, Esplanade, Khae Rai, Owl Market.\r\n- Near Phranangklao Hospital , Kasemrad Hospital Prachachuen, Bamrasnaradura Hospital. , Chest Disease \r\nInstitute\r\n- Near Sribunyanon School , Rajamangala University of Technology Suvarnabhumi , Siam Technology College of \r\nBusiness Administration\r\n- Near all banks\r\n\r\n::coordinates::\r\nhttps://goo.gl/maps/k7o8URq7M7FJ3Vic7\r\n\r\nRental fee 40,000 baht\r\nMinimum contract 1 year, advance payment 1 month, security deposit 2 months.\r\n\r\nContact: Thanaporn 092-514-1987 / 0 9 2 5 1 4 1 9 8 7\r\nLine I D: tkproperty987\r\nhttps://line.me/ti/p/tQDsEigadM\r\nfriendly service Happy to give advice before making a purchase.\r\nERA PROPERTY NETWORK",
            "price_baht": "40000",
            "listing_type": "เช่า",
            "property_type": "house",
            "building": "",
            "floor_level": "",
            "floor_total": "2",
            "floor_area": "350",
            "bath_room": "4",
            "bed_room": "3",
            "prominent_point": "บ้านหลังมุม\r\nพื้นที่สวนกว้างมาก\r\nจอดรถได้ 2 คัน\r\nมีห้องนั่งเล่น ห้องทำงาน ห้องโถงชั้นบน\r\nทุกห้องนอนมีห้องน้ำ\r\nมีห้องแม่บ้าน+ห้องน้ำ ภายนอกบ้าน\r\nทุกห้องมีแอร์ รวม 6 ตัว",
            "view_type": "",
            "direction_type": "12",
            "addr_province": "นนทบุรี",
            "addr_district": "เมืองนนทบุรี",
            "addr_sub_district": "ท่าทราย",
            "addr_number": "-",
            "addr_road": "สนามบินน้ำ",
            "addr_soi": "-",
            "addr_near_by": "",
            "addr_postcode": "11000",
            "floorarea_sqm": "350",
            "land_size_rai": "",
            "land_size_ngan": "1",
            "land_size_wa": "20",
            "name": "มัทนา",
            "mobile": "0805965799",
            "email": "baankaibaan@gmail.com",
            "line": "@697fybbq",
            "project_name": "เศรษฐสิริ สนามบินน้ำ",
            "web": [
                {
                "ds_name": "''' + self.web_name + '''",
                "ds_id": 2,
                "web_project_name": "",
                "location_area": "",
                "user": "''' + self.login_user + '''",
                "pass": "''' + self.login_pass + '''"
                }
            ]
        }
        '''
        return json_string

    def get_edit_post_json_string(self):
        json_string = '''
        {
            "action": "edit_post",
            "timeout": "5",
            "post_img_url_lists": [
                "https://storage.googleapis.com/reas-240123.appspot.com/property/images/PR_aa00000442842_86e8f4ee-5b68-4db4-b880-e228469f592d.jpg",
                "https://storage.googleapis.com/reas-240123.appspot.com/property/images/PR_aa00000442842_59ba30c3-40ef-4cca-a6ad-a6f9072c6b8b.jpg",
                "https://storage.googleapis.com/reas-240123.appspot.com/property/images/PR_aa00000442842_7d339cee-d097-4bc8-bde3-09d16e10c24b.jpg",
                "https://storage.googleapis.com/reas-240123.appspot.com/property/images/PR_aa00000442842_96f816c0-634d-4343-b1e7-b6e3a68233e2.jpg",
                "https://storage.googleapis.com/reas-240123.appspot.com/property/images/PR_aa00000442842_ed7933d8-54e0-4de6-8b91-9fb322db79bd.jpg",
                "https://storage.googleapis.com/reas-240123.appspot.com/property/images/PR_aa00000442842_930d9a2d-540f-4f97-bcd8-f5bd9074db4e.jpg",
                "https://storage.googleapis.com/reas-240123.appspot.com/property/images/PR_aa00000442842_f6d05ffd-0527-4bf4-964f-194ec2c0c150.jpg",
                "https://storage.googleapis.com/reas-240123.appspot.com/property/images/PR_aa00000442842_d069ecdb-d0f4-4b53-b37f-6dafc0839dff.jpg",
                "https://storage.googleapis.com/reas-240123.appspot.com/property/images/PR_aa00000442842_9225b49e-1b3c-45dd-ae3a-6e04f2b1790b.jpg",
                "https://storage.googleapis.com/reas-240123.appspot.com/property/images/PR_aa00000442842_c2197f82-5c7c-4483-9f61-8abb303d7716.jpg",
                "https://storage.googleapis.com/reas-240123.appspot.com/property/images/PR_aa00000442842_8ac8f6df-f1d5-4cfa-b963-ebb456fa4d70.jpg",
                "https://storage.googleapis.com/reas-240123.appspot.com/property/images/PR_aa00000442842_ebc251c9-ff77-466a-b50f-c8ac89e4d029.jpg"
            ],
            "geo_latitude": "13.884",
            "geo_longitude": "100.501",
            "property_id": "PR_aa00000442842",
            "post_id": "''' + self.post_id + '''",
            "post_title_th": "ให้เช่า บ้านเดี่ยว หลังมุม เศรษฐสิริ สนามบินน้ำ 120 ตร.วา สภาพดี",
            "short_post_title_th": "",
            "post_description_th": "ให้เช่า บ้านเดี่ยว หลังมุม เศรษฐสิริ สนามบินน้ำ 120 ตร.วา สภาพดี\r\n\r\nให้เช่า บ้านเดี่ยว หลังมุม หมู่บ้านเศรษฐสิริ สนามบินน้ำ\r\nบรรยากาศร่มรื่น ไม่พลุกพล่าน หมู่บ้านติดถ.สนามบิน้ำ ไม่ต้องเข้าซอย\r\nใกล้กองสลาก ใกล้เซ็นทรัลรัตนาธิเบศร์ ใกล้เดอะมอลล์งามวงศ์วาน\r\n\r\n:: ที่ตั้ง ::\r\nหมู่บ้านเศรษฐสิริ สนามบินน้ำ ซอย 9\r\nถ.สนามบินน้ำ ต.ท่าทราย อ.เมืองนนทบุรี จ.นนทบุรี\r\n\r\n::จุดเด่น::\r\nขนาดพื้นที่ 120 ตร.วา\r\nพื้นที่ใช้สอย 350 ตร.ม.\r\nบ้านหลังมุม\r\nหน้าบ้านหันทิศใต้\r\nจอดรถ 2 คัน\r\nสนามหญ้ากว้างมาก\r\n::ประกอบด้วย::\r\n3 ห้องนอน 4 ห้องน้ำ 1ห้องนั่งเล่น 1 ห้องทำงาน 1 ห้องอาหาร\r\n2 ห้องครัว 1 ห้องแม่บ้าน \r\nชั้น 2 มีโถงกลาง ทำเป็นห้องนั่งเล่นได้\r\nให้เช่าเป็นบ้านเปล่า มีเฟอร์นิเจอร์บางส่วน\r\nมีแอร์ 6 เครื่อง\r\nปูพื้นชั้นล่างกระเบื้อง - ชั้นบนเป็นปาร์เก้\r\n\r\n::รายละเอียดโครงการ::\r\nหมู่บ้านเศรษฐสิริ สนามบินน้ำ\r\nมีสระว่ายน้ำ ฟิตเนส สโมสร\r\n\r\n::สถานที่ใกล้เคียง::\r\n– ใกล้ห้างสรรพสินค้าเซ็นทรัล รัตนาธิเบศร์ ,เดอะมอลล์งามวงศ์วาน ,พันธ์ทิพย์งามวงศ์วาน ,Big C รัตนาธิเบศร์ ,Tesco Lotus \r\nแคราย ,เอสพลานาด แคราย ,ตลาดนกฮูก\r\n– ใกล้โรงพยาบาลพระนั่งเกล้า ,โรงพยาบาลเกษมราษฏร์ ประชาชื่น ,โรงพยาบาลบำราศนราดูร ,สถาบันโรคทรวงอก\r\n– ใกล้โรงเรียนศรีบุญยานนท์ ,มหาวิทยาลัยเทคโนโลยีราชมงคลสุวรรณภูมิ ,วิทยาลัยเทคโนโลยีสยามบริหารธุรกิจ\r\n– ใกล้ธนาคารทุกธนาคาร\r\n\r\n::พิกัด::\r\nhttps://goo.gl/maps/k7o8URq7M7FJ3Vic7\r\n\r\nค่าเช่า 40,000 บาท\r\nสัญญาขั้นต่ำ 1 ปี จ่ายล่วงหน้า 1 เดือน เงินประกัน 2 เดือน\r\n\r\nสนใจติดต่อ: ธนพร 092-514-1987 / 0 9 2 5 1 4 1 9 8 7\r\nLine I D: tkproperty987\r\nhttps://line.me/ti/p/tQDsEigadM\r\nบริการเป็นกันเอง ยินดีให้คำปรึกษาก่อนตัดสินใจซื้อ\r\nERA PROPERTY NETWORK",
            "post_title_en": "House for rent at the corner of Setthasiri Sanambinnam 120 sq. wa. Good condition.",
            "short_post_title_en": "",
            "post_description_en": "House for rent at the corner of Setthasiri Village Sanambinnam\r\nThe atmosphere is shady, not crowded, the village is next to Sanambinnam Rd. don't have to go into the alley\r\nnear the lottery, near Central Rattanathibet near The Mall Ngamwongwan\r\n\r\n:: Location ::\r\nSetthasiri Village, Sanambinnam Soi 9\r\nSanambinnam Rd., Tha Sai Subdistrict, Mueang Nonthaburi District, Nonthaburi Province\r\n\r\n::Highlights::\r\nArea size 120 sq wa\r\nUsable area 350 sq m.\r\ncorner house\r\nfront of the house facing south\r\nParking for 2 cars\r\nvery wide lawn\r\n\r\n::include::\r\n3 bedrooms, 4 bathrooms, 1 living room, 1 office room, 1 dining room\r\n2 kitchens, 1 maid's room\r\n2nd floor has a central hall that can be used as a living room.\r\nRent as an empty house have some furniture\r\nThere are 6 air conditioners.\r\nFloor tiles downstairs - upstairs is parquet.\r\n\r\n::Project details::\r\nSetthasiri Village, Sanambinnam\r\nThere is a swimming pool, fitness center and club.\r\n\r\n::Nearby Places::\r\n- Near Central Department Store, Rattanathibet, The Mall Ngamwongwan , Pantip Ngamwongwan, Big C \r\nRattanathibet, Tesco Lotus, Khae Rai, Esplanade, Khae Rai, Owl Market.\r\n- Near Phranangklao Hospital , Kasemrad Hospital Prachachuen, Bamrasnaradura Hospital. , Chest Disease \r\nInstitute\r\n- Near Sribunyanon School , Rajamangala University of Technology Suvarnabhumi , Siam Technology College of \r\nBusiness Administration\r\n- Near all banks\r\n\r\n::coordinates::\r\nhttps://goo.gl/maps/k7o8URq7M7FJ3Vic7\r\n\r\nRental fee 40,000 baht\r\nMinimum contract 1 year, advance payment 1 month, security deposit 2 months.\r\n\r\nContact: Thanaporn 092-514-1987 / 0 9 2 5 1 4 1 9 8 7\r\nLine I D: tkproperty987\r\nhttps://line.me/ti/p/tQDsEigadM\r\nfriendly service Happy to give advice before making a purchase.\r\nERA PROPERTY NETWORK",
            "price_baht": "40000",
            "listing_type": "เช่า",
            "property_type": "house",
            "building": "",
            "floor_level": "",
            "floor_total": "2",
            "floor_area": "350",
            "bath_room": "4",
            "bed_room": "3",
            "prominent_point": "บ้านหลังมุม\r\nพื้นที่สวนกว้างมาก\r\nจอดรถได้ 2 คัน\r\nมีห้องนั่งเล่น ห้องทำงาน ห้องโถงชั้นบน\r\nทุกห้องนอนมีห้องน้ำ\r\nมีห้องแม่บ้าน+ห้องน้ำ ภายนอกบ้าน\r\nทุกห้องมีแอร์ รวม 6 ตัว",
            "view_type": "",
            "direction_type": "12",
            "addr_province": "นนทบุรี",
            "addr_district": "เมืองนนทบุรี",
            "addr_sub_district": "ท่าทราย",
            "addr_number": "-",
            "addr_road": "สนามบินน้ำ",
            "addr_soi": "-",
            "addr_near_by": "",
            "addr_postcode": "11000",
            "floorarea_sqm": "350",
            "land_size_rai": "",
            "land_size_ngan": "1",
            "land_size_wa": "20",
            "name": "มัทนา",
            "mobile": "0805965799",
            "email": "baankaibaan@gmail.com",
            "line": "@697fybbq",
            "project_name": "เศรษฐสิริ สนามบินน้ำ",
            "web": [
                {
                "ds_name": "''' + self.web_name + '''",
                "ds_id": 2,
                "web_project_name": "",
                "location_area": "",
                "user": "''' + self.login_user + '''",
                "pass": "''' + self.login_pass + '''"
                }
            ]
            }
            '''
        return json_string

    def get_delete_post_json_string(self):
        json_string = '''
        {
            "action": "delete_post",
            "post_id": "''' + self.post_id + '''",
            "web": [
                {
                    "ds_name": "''' + self.web_name + '''",
                    "ds_id": "4",              
                    "user": "''' + self.login_user + '''",
                    "pass": "''' + self.login_pass + '''"
                }
            ]
        }
        '''
        return json_string

    def get_boost_post_json_string(self):
        json_string = '''
            {
                "action": "boost_post",
                "timeout": "5",
                "post_img_url_lists": [
                    "https://storage.googleapis.com/reas-240123.appspot.com/property/images/PR_aa00000442842_86e8f4ee-5b68-4db4-b880-e228469f592d.jpg",
                    "https://storage.googleapis.com/reas-240123.appspot.com/property/images/PR_aa00000442842_59ba30c3-40ef-4cca-a6ad-a6f9072c6b8b.jpg",
                    "https://storage.googleapis.com/reas-240123.appspot.com/property/images/PR_aa00000442842_7d339cee-d097-4bc8-bde3-09d16e10c24b.jpg",
                    "https://storage.googleapis.com/reas-240123.appspot.com/property/images/PR_aa00000442842_96f816c0-634d-4343-b1e7-b6e3a68233e2.jpg",
                    "https://storage.googleapis.com/reas-240123.appspot.com/property/images/PR_aa00000442842_ed7933d8-54e0-4de6-8b91-9fb322db79bd.jpg",
                    "https://storage.googleapis.com/reas-240123.appspot.com/property/images/PR_aa00000442842_930d9a2d-540f-4f97-bcd8-f5bd9074db4e.jpg",
                    "https://storage.googleapis.com/reas-240123.appspot.com/property/images/PR_aa00000442842_f6d05ffd-0527-4bf4-964f-194ec2c0c150.jpg",
                    "https://storage.googleapis.com/reas-240123.appspot.com/property/images/PR_aa00000442842_d069ecdb-d0f4-4b53-b37f-6dafc0839dff.jpg",
                    "https://storage.googleapis.com/reas-240123.appspot.com/property/images/PR_aa00000442842_9225b49e-1b3c-45dd-ae3a-6e04f2b1790b.jpg",
                    "https://storage.googleapis.com/reas-240123.appspot.com/property/images/PR_aa00000442842_c2197f82-5c7c-4483-9f61-8abb303d7716.jpg",
                    "https://storage.googleapis.com/reas-240123.appspot.com/property/images/PR_aa00000442842_8ac8f6df-f1d5-4cfa-b963-ebb456fa4d70.jpg",
                    "https://storage.googleapis.com/reas-240123.appspot.com/property/images/PR_aa00000442842_ebc251c9-ff77-466a-b50f-c8ac89e4d029.jpg"
                ],
                "geo_latitude": "13.884",
                "geo_longitude": "100.501",
                "property_id": "PR_aa00000442842",
                "post_id": "''' + self.post_id + '''",
                "post_title_th": "ให้เช่า บ้านเดี่ยว หลังมุม เศรษฐสิริ สนามบินน้ำ 120 ตร.วา สภาพดี",
                "short_post_title_th": "",
                "post_description_th": "ให้เช่า บ้านเดี่ยว หลังมุม เศรษฐสิริ สนามบินน้ำ 120 ตร.วา สภาพดี\r\n\r\nให้เช่า บ้านเดี่ยว หลังมุม หมู่บ้านเศรษฐสิริ สนามบินน้ำ\r\nบรรยากาศร่มรื่น ไม่พลุกพล่าน หมู่บ้านติดถ.สนามบิน้ำ ไม่ต้องเข้าซอย\r\nใกล้กองสลาก ใกล้เซ็นทรัลรัตนาธิเบศร์ ใกล้เดอะมอลล์งามวงศ์วาน\r\n\r\n:: ที่ตั้ง ::\r\nหมู่บ้านเศรษฐสิริ สนามบินน้ำ ซอย 9\r\nถ.สนามบินน้ำ ต.ท่าทราย อ.เมืองนนทบุรี จ.นนทบุรี\r\n\r\n::จุดเด่น::\r\nขนาดพื้นที่ 120 ตร.วา\r\nพื้นที่ใช้สอย 350 ตร.ม.\r\nบ้านหลังมุม\r\nหน้าบ้านหันทิศใต้\r\nจอดรถ 2 คัน\r\nสนามหญ้ากว้างมาก\r\n::ประกอบด้วย::\r\n3 ห้องนอน 4 ห้องน้ำ 1ห้องนั่งเล่น 1 ห้องทำงาน 1 ห้องอาหาร\r\n2 ห้องครัว 1 ห้องแม่บ้าน \r\nชั้น 2 มีโถงกลาง ทำเป็นห้องนั่งเล่นได้\r\nให้เช่าเป็นบ้านเปล่า มีเฟอร์นิเจอร์บางส่วน\r\nมีแอร์ 6 เครื่อง\r\nปูพื้นชั้นล่างกระเบื้อง - ชั้นบนเป็นปาร์เก้\r\n\r\n::รายละเอียดโครงการ::\r\nหมู่บ้านเศรษฐสิริ สนามบินน้ำ\r\nมีสระว่ายน้ำ ฟิตเนส สโมสร\r\n\r\n::สถานที่ใกล้เคียง::\r\n– ใกล้ห้างสรรพสินค้าเซ็นทรัล รัตนาธิเบศร์ ,เดอะมอลล์งามวงศ์วาน ,พันธ์ทิพย์งามวงศ์วาน ,Big C รัตนาธิเบศร์ ,Tesco Lotus \r\nแคราย ,เอสพลานาด แคราย ,ตลาดนกฮูก\r\n– ใกล้โรงพยาบาลพระนั่งเกล้า ,โรงพยาบาลเกษมราษฏร์ ประชาชื่น ,โรงพยาบาลบำราศนราดูร ,สถาบันโรคทรวงอก\r\n– ใกล้โรงเรียนศรีบุญยานนท์ ,มหาวิทยาลัยเทคโนโลยีราชมงคลสุวรรณภูมิ ,วิทยาลัยเทคโนโลยีสยามบริหารธุรกิจ\r\n– ใกล้ธนาคารทุกธนาคาร\r\n\r\n::พิกัด::\r\nhttps://goo.gl/maps/k7o8URq7M7FJ3Vic7\r\n\r\nค่าเช่า 40,000 บาท\r\nสัญญาขั้นต่ำ 1 ปี จ่ายล่วงหน้า 1 เดือน เงินประกัน 2 เดือน\r\n\r\nสนใจติดต่อ: ธนพร 092-514-1987 / 0 9 2 5 1 4 1 9 8 7\r\nLine I D: tkproperty987\r\nhttps://line.me/ti/p/tQDsEigadM\r\nบริการเป็นกันเอง ยินดีให้คำปรึกษาก่อนตัดสินใจซื้อ\r\nERA PROPERTY NETWORK",
                "post_title_en": "House for rent at the corner of Setthasiri Sanambinnam 120 sq. wa. Good condition.",
                "short_post_title_en": "",
                "post_description_en": "House for rent at the corner of Setthasiri Village Sanambinnam\r\nThe atmosphere is shady, not crowded, the village is next to Sanambinnam Rd. don't have to go into the alley\r\nnear the lottery, near Central Rattanathibet near The Mall Ngamwongwan\r\n\r\n:: Location ::\r\nSetthasiri Village, Sanambinnam Soi 9\r\nSanambinnam Rd., Tha Sai Subdistrict, Mueang Nonthaburi District, Nonthaburi Province\r\n\r\n::Highlights::\r\nArea size 120 sq wa\r\nUsable area 350 sq m.\r\ncorner house\r\nfront of the house facing south\r\nParking for 2 cars\r\nvery wide lawn\r\n\r\n::include::\r\n3 bedrooms, 4 bathrooms, 1 living room, 1 office room, 1 dining room\r\n2 kitchens, 1 maid's room\r\n2nd floor has a central hall that can be used as a living room.\r\nRent as an empty house have some furniture\r\nThere are 6 air conditioners.\r\nFloor tiles downstairs - upstairs is parquet.\r\n\r\n::Project details::\r\nSetthasiri Village, Sanambinnam\r\nThere is a swimming pool, fitness center and club.\r\n\r\n::Nearby Places::\r\n- Near Central Department Store, Rattanathibet, The Mall Ngamwongwan , Pantip Ngamwongwan, Big C \r\nRattanathibet, Tesco Lotus, Khae Rai, Esplanade, Khae Rai, Owl Market.\r\n- Near Phranangklao Hospital , Kasemrad Hospital Prachachuen, Bamrasnaradura Hospital. , Chest Disease \r\nInstitute\r\n- Near Sribunyanon School , Rajamangala University of Technology Suvarnabhumi , Siam Technology College of \r\nBusiness Administration\r\n- Near all banks\r\n\r\n::coordinates::\r\nhttps://goo.gl/maps/k7o8URq7M7FJ3Vic7\r\n\r\nRental fee 40,000 baht\r\nMinimum contract 1 year, advance payment 1 month, security deposit 2 months.\r\n\r\nContact: Thanaporn 092-514-1987 / 0 9 2 5 1 4 1 9 8 7\r\nLine I D: tkproperty987\r\nhttps://line.me/ti/p/tQDsEigadM\r\nfriendly service Happy to give advice before making a purchase.\r\nERA PROPERTY NETWORK",
                "price_baht": "40000",
                "listing_type": "เช่า",
                "property_type": "house",
                "building": "",
                "floor_level": "",
                "floor_total": "2",
                "floor_area": "350",
                "bath_room": "4",
                "bed_room": "3",
                "prominent_point": "บ้านหลังมุม\r\nพื้นที่สวนกว้างมาก\r\nจอดรถได้ 2 คัน\r\nมีห้องนั่งเล่น ห้องทำงาน ห้องโถงชั้นบน\r\nทุกห้องนอนมีห้องน้ำ\r\nมีห้องแม่บ้าน+ห้องน้ำ ภายนอกบ้าน\r\nทุกห้องมีแอร์ รวม 6 ตัว",
                "view_type": "",
                "direction_type": "12",
                "addr_province": "นนทบุรี",
                "addr_district": "เมืองนนทบุรี",
                "addr_sub_district": "ท่าทราย",
                "addr_number": "-",
                "addr_road": "สนามบินน้ำ",
                "addr_soi": "-",
                "addr_near_by": "",
                "addr_postcode": "11000",
                "floorarea_sqm": "350",
                "land_size_rai": "",
                "land_size_ngan": "1",
                "land_size_wa": "20",
                "name": "มัทนา",
                "mobile": "0805965799",
                "email": "baankaibaan@gmail.com",
                "line": "@697fybbq",
                "project_name": "เศรษฐสิริ สนามบินน้ำ",
                "web": [
                    {
                    "ds_name": "''' + self.web_name + '''",
                    "ds_id": 2,
                    "web_project_name": "",
                    "location_area": "",
                    "user": "''' + self.login_user + '''",
                    "pass": "''' + self.login_pass + '''"
                    }
                ]
                }
                '''
        return json_string

    def get_search_post_json_string(self):
        json_string = '''
            {
                "action": "search_post",
                "timeout": "5",
                "post_img_url_lists": [
                    "https://storage.googleapis.com/reas-240123.appspot.com/property/images/PR_aa00000442842_86e8f4ee-5b68-4db4-b880-e228469f592d.jpg",
                    "https://storage.googleapis.com/reas-240123.appspot.com/property/images/PR_aa00000442842_59ba30c3-40ef-4cca-a6ad-a6f9072c6b8b.jpg",
                    "https://storage.googleapis.com/reas-240123.appspot.com/property/images/PR_aa00000442842_7d339cee-d097-4bc8-bde3-09d16e10c24b.jpg",
                    "https://storage.googleapis.com/reas-240123.appspot.com/property/images/PR_aa00000442842_96f816c0-634d-4343-b1e7-b6e3a68233e2.jpg",
                    "https://storage.googleapis.com/reas-240123.appspot.com/property/images/PR_aa00000442842_ed7933d8-54e0-4de6-8b91-9fb322db79bd.jpg",
                    "https://storage.googleapis.com/reas-240123.appspot.com/property/images/PR_aa00000442842_930d9a2d-540f-4f97-bcd8-f5bd9074db4e.jpg",
                    "https://storage.googleapis.com/reas-240123.appspot.com/property/images/PR_aa00000442842_f6d05ffd-0527-4bf4-964f-194ec2c0c150.jpg",
                    "https://storage.googleapis.com/reas-240123.appspot.com/property/images/PR_aa00000442842_d069ecdb-d0f4-4b53-b37f-6dafc0839dff.jpg",
                    "https://storage.googleapis.com/reas-240123.appspot.com/property/images/PR_aa00000442842_9225b49e-1b3c-45dd-ae3a-6e04f2b1790b.jpg",
                    "https://storage.googleapis.com/reas-240123.appspot.com/property/images/PR_aa00000442842_c2197f82-5c7c-4483-9f61-8abb303d7716.jpg",
                    "https://storage.googleapis.com/reas-240123.appspot.com/property/images/PR_aa00000442842_8ac8f6df-f1d5-4cfa-b963-ebb456fa4d70.jpg",
                    "https://storage.googleapis.com/reas-240123.appspot.com/property/images/PR_aa00000442842_ebc251c9-ff77-466a-b50f-c8ac89e4d029.jpg"
                ],
                "geo_latitude": "13.884",
                "geo_longitude": "100.501",
                "property_id": "PR_aa00000442842",
                "post_id": "''' + self.post_id + '''",
                "log_id": "",
                "post_title_th": "ให้เช่า บ้านเดี่ยว หลังมุม เศรษฐสิริ สนามบินน้ำ 120 ตร.วา สภาพดี",
                "short_post_title_th": "",
                "post_description_th": "ให้เช่า บ้านเดี่ยว หลังมุม เศรษฐสิริ สนามบินน้ำ 120 ตร.วา สภาพดี\r\n\r\nให้เช่า บ้านเดี่ยว หลังมุม หมู่บ้านเศรษฐสิริ สนามบินน้ำ\r\nบรรยากาศร่มรื่น ไม่พลุกพล่าน หมู่บ้านติดถ.สนามบิน้ำ ไม่ต้องเข้าซอย\r\nใกล้กองสลาก ใกล้เซ็นทรัลรัตนาธิเบศร์ ใกล้เดอะมอลล์งามวงศ์วาน\r\n\r\n:: ที่ตั้ง ::\r\nหมู่บ้านเศรษฐสิริ สนามบินน้ำ ซอย 9\r\nถ.สนามบินน้ำ ต.ท่าทราย อ.เมืองนนทบุรี จ.นนทบุรี\r\n\r\n::จุดเด่น::\r\nขนาดพื้นที่ 120 ตร.วา\r\nพื้นที่ใช้สอย 350 ตร.ม.\r\nบ้านหลังมุม\r\nหน้าบ้านหันทิศใต้\r\nจอดรถ 2 คัน\r\nสนามหญ้ากว้างมาก\r\n::ประกอบด้วย::\r\n3 ห้องนอน 4 ห้องน้ำ 1ห้องนั่งเล่น 1 ห้องทำงาน 1 ห้องอาหาร\r\n2 ห้องครัว 1 ห้องแม่บ้าน \r\nชั้น 2 มีโถงกลาง ทำเป็นห้องนั่งเล่นได้\r\nให้เช่าเป็นบ้านเปล่า มีเฟอร์นิเจอร์บางส่วน\r\nมีแอร์ 6 เครื่อง\r\nปูพื้นชั้นล่างกระเบื้อง - ชั้นบนเป็นปาร์เก้\r\n\r\n::รายละเอียดโครงการ::\r\nหมู่บ้านเศรษฐสิริ สนามบินน้ำ\r\nมีสระว่ายน้ำ ฟิตเนส สโมสร\r\n\r\n::สถานที่ใกล้เคียง::\r\n– ใกล้ห้างสรรพสินค้าเซ็นทรัล รัตนาธิเบศร์ ,เดอะมอลล์งามวงศ์วาน ,พันธ์ทิพย์งามวงศ์วาน ,Big C รัตนาธิเบศร์ ,Tesco Lotus \r\nแคราย ,เอสพลานาด แคราย ,ตลาดนกฮูก\r\n– ใกล้โรงพยาบาลพระนั่งเกล้า ,โรงพยาบาลเกษมราษฏร์ ประชาชื่น ,โรงพยาบาลบำราศนราดูร ,สถาบันโรคทรวงอก\r\n– ใกล้โรงเรียนศรีบุญยานนท์ ,มหาวิทยาลัยเทคโนโลยีราชมงคลสุวรรณภูมิ ,วิทยาลัยเทคโนโลยีสยามบริหารธุรกิจ\r\n– ใกล้ธนาคารทุกธนาคาร\r\n\r\n::พิกัด::\r\nhttps://goo.gl/maps/k7o8URq7M7FJ3Vic7\r\n\r\nค่าเช่า 40,000 บาท\r\nสัญญาขั้นต่ำ 1 ปี จ่ายล่วงหน้า 1 เดือน เงินประกัน 2 เดือน\r\n\r\nสนใจติดต่อ: ธนพร 092-514-1987 / 0 9 2 5 1 4 1 9 8 7\r\nLine I D: tkproperty987\r\nhttps://line.me/ti/p/tQDsEigadM\r\nบริการเป็นกันเอง ยินดีให้คำปรึกษาก่อนตัดสินใจซื้อ\r\nERA PROPERTY NETWORK",
                "post_title_en": "House for rent at the corner of Setthasiri Sanambinnam 120 sq. wa. Good condition.",
                "short_post_title_en": "",
                "post_description_en": "House for rent at the corner of Setthasiri Village Sanambinnam\r\nThe atmosphere is shady, not crowded, the village is next to Sanambinnam Rd. don't have to go into the alley\r\nnear the lottery, near Central Rattanathibet near The Mall Ngamwongwan\r\n\r\n:: Location ::\r\nSetthasiri Village, Sanambinnam Soi 9\r\nSanambinnam Rd., Tha Sai Subdistrict, Mueang Nonthaburi District, Nonthaburi Province\r\n\r\n::Highlights::\r\nArea size 120 sq wa\r\nUsable area 350 sq m.\r\ncorner house\r\nfront of the house facing south\r\nParking for 2 cars\r\nvery wide lawn\r\n\r\n::include::\r\n3 bedrooms, 4 bathrooms, 1 living room, 1 office room, 1 dining room\r\n2 kitchens, 1 maid's room\r\n2nd floor has a central hall that can be used as a living room.\r\nRent as an empty house have some furniture\r\nThere are 6 air conditioners.\r\nFloor tiles downstairs - upstairs is parquet.\r\n\r\n::Project details::\r\nSetthasiri Village, Sanambinnam\r\nThere is a swimming pool, fitness center and club.\r\n\r\n::Nearby Places::\r\n- Near Central Department Store, Rattanathibet, The Mall Ngamwongwan , Pantip Ngamwongwan, Big C \r\nRattanathibet, Tesco Lotus, Khae Rai, Esplanade, Khae Rai, Owl Market.\r\n- Near Phranangklao Hospital , Kasemrad Hospital Prachachuen, Bamrasnaradura Hospital. , Chest Disease \r\nInstitute\r\n- Near Sribunyanon School , Rajamangala University of Technology Suvarnabhumi , Siam Technology College of \r\nBusiness Administration\r\n- Near all banks\r\n\r\n::coordinates::\r\nhttps://goo.gl/maps/k7o8URq7M7FJ3Vic7\r\n\r\nRental fee 40,000 baht\r\nMinimum contract 1 year, advance payment 1 month, security deposit 2 months.\r\n\r\nContact: Thanaporn 092-514-1987 / 0 9 2 5 1 4 1 9 8 7\r\nLine I D: tkproperty987\r\nhttps://line.me/ti/p/tQDsEigadM\r\nfriendly service Happy to give advice before making a purchase.\r\nERA PROPERTY NETWORK",
                "price_baht": "40000",
                "listing_type": "เช่า",
                "property_type": "house",
                "building": "",
                "floor_level": "",
                "floor_total": "2",
                "floor_area": "350",
                "bath_room": "4",
                "bed_room": "3",
                "prominent_point": "บ้านหลังมุม\r\nพื้นที่สวนกว้างมาก\r\nจอดรถได้ 2 คัน\r\nมีห้องนั่งเล่น ห้องทำงาน ห้องโถงชั้นบน\r\nทุกห้องนอนมีห้องน้ำ\r\nมีห้องแม่บ้าน+ห้องน้ำ ภายนอกบ้าน\r\nทุกห้องมีแอร์ รวม 6 ตัว",
                "view_type": "",
                "direction_type": "12",
                "addr_province": "นนทบุรี",
                "addr_district": "เมืองนนทบุรี",
                "addr_sub_district": "ท่าทราย",
                "addr_number": "-",
                "addr_road": "สนามบินน้ำ",
                "addr_soi": "-",
                "addr_near_by": "",
                "addr_postcode": "11000",
                "floorarea_sqm": "350",
                "land_size_rai": "",
                "land_size_ngan": "1",
                "land_size_wa": "20",
                "name": "มัทนา",
                "mobile": "0805965799",
                "email": "baankaibaan@gmail.com",
                "line": "@697fybbq",
                "project_name": "เศรษฐสิริ สนามบินน้ำ",
                "web": [
                    {
                    "ds_name": "''' + self.web_name + '''",
                    "ds_id": 2,
                    "web_project_name": "",
                    "location_area": "",
                    "user": "''' + self.login_user + '''",
                    "pass": "''' + self.login_pass + '''"
                    }
                ]
                }
                '''
        return json_string