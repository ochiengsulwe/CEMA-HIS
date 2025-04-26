""" A simulation of various medical boards' registry"""

dentists = [
    {
        'id_num': 101,
        'first_name': 'John',
        'middle_name': 'Kariuki',
        'last_name': 'Nyaga',
        'gender': 'Male',
        'license_num': 'D123456',
        'reg_year': '2020-05-01',
        'specialization': 'Orthodontics',
        'spec_reg_num': 'D78901',
        'spec_year': '2021-06-01'
    },
    {
        'id_num': 102,
        'first_name': 'Jane',
        'middle_name': 'Bosire',
        'last_name': 'Nyangau',
        'gender': 'Female',
        'license_num': 'D234567',
        'reg_year': '2019-07-15'
    },
    {
        'id_num': 103,
        'first_name': 'Chris',
        'middle_name': 'Choto',
        'last_name': 'Odhiambo',
        'gender': 'Male',
        'license_num': 'D345678',
        'reg_year': '2018-03-10',
        'specialization': 'Periodontics',
        'spec_reg_num': 'D89012',
        'spec_year': '2019-04-22'
    },
    {
        'id_num': 104,
        'first_name': 'Patricia',
        'middle_name': 'Dete',
        'last_name': 'Akinyi',
        'gender': 'Female',
        'license_num': 'D456789',
        'reg_year': '2021-11-20'
    },
    {
        'id_num': 105,
        'first_name': 'Abdi',
        'middle_name': 'Hassan',
        'last_name': 'Hussein',
        'gender': 'Male',
        'license_num': 'D567890',
        'reg_year': '2020-08-18',
        'specialization': 'Endodontics',
        'spec_reg_num': 'D90123',
        'spec_year': '2020-09-10'
    },
    {
        'id_num': 106,
        'first_name': 'Nancy',
        'middle_name': 'Malonza',
        'last_name': 'Mutii',
        'gender': 'Female',
        'license_num': 'D678901',
        'reg_year': '2019-05-25'
    },
    {
        'id_num': 107,
        'first_name': 'Karen',
        'middle_name': 'Chesang',
        'last_name': 'Cheruto',
        'gender': 'Female',
        'license_num': 'D789012',
        'reg_year': '2017-02-14',
        'specialization': 'Prosthodontics',
        'spec_reg_num': 'D01234',
        'spec_year': '2018-03-15'
    },
    {
        'id_num': 108,
        'first_name': 'James',
        'middle_name': 'Mwigwi',
        'last_name': 'Mutua',
        'gender': 'Male',
        'license_num': 'D890123',
        'reg_year': '2022-01-12'
    },
    {
        'id_num': 109,
        'first_name': 'Michael',
        'middle_name': 'Isinya',
        'last_name': 'Tipis',
        'gender': 'Male',
        'license_num': 'D901234',
        'reg_year': '2021-09-30',
        'specialization': 'Oral Surgery',
        'spec_reg_num': 'D12345',
        'spec_year': '2022-02-20'
    },
    {
        'id_num': 110,
        'first_name': 'Paul',
        'middle_name': 'Tunje',
        'last_name': 'Mwakisagu',
        'gender': 'Male',
        'license_num': 'D012345',
        'reg_year': '2018-04-17'
    }
]

doctors = [
    {
        'id_num': 201,
        'first_name': 'Alice',
        'middle_name': 'Wahome',
        'last_name': 'Munene',
        'gender': 'Female',
        'license_num': 'M345678',
        'reg_year': '2018-03-10',
        'specialization': 'Cardiology',
        'spec_reg_num': 'M89012',
        'spec_year': '2019-04-22'
    },
    {
        'id_num': 202,
        'first_name': 'Bob',
        'middle_name': 'Miran',
        'last_name': 'Tipis',
        'gender': 'Male',
        'license_num': 'M456789',
        'reg_year': '2021-11-20'
    },
    {
        'id_num': 203,
        'first_name': 'Carol',
        'middle_name': 'Emali',
        'last_name': 'Wesonga',
        'gender': 'Female',
        'license_num': 'M567890',
        'reg_year': '2020-08-18',
        'specialization': 'Neurology',
        'spec_reg_num': 'M9012',
        'spec_year': '2020-09-10'
    },
    {
        'id_num': 204,
        'first_name': 'Rashid',
        'middle_name': 'Nusra',
        'last_name': 'Amin',
        'gender': 'Male',
        'license_num': 'M678901',
        'reg_year': '2019-05-25'
    },
    {
        'id_num': 205,
        'first_name': 'Emily',
        'middle_name': 'Gatwiri',
        'last_name': 'Matuu',
        'gender': 'Female',
        'license_num': 'M789012',
        'reg_year': '2017-02-14',
        'specialization': 'Pediatrics',
        'spec_reg_num': 'M01234',
        'spec_year': '2018-03-15'
    },
    {
        'id_num': 206,
        'first_name': 'Frank',
        'middle_name': 'Ososo',
        'last_name': 'Kavugwe',
        'gender': 'Male',
        'license_num': 'M890123',
        'reg_year': '2022-01-12'
    },
    {
        'id_num': 207,
        'first_name': 'Grace',
        'middle_name': 'Musenyia',
        'last_name': 'Wabwire',
        'gender': 'Female',
        'license_num': 'M901234',
        'reg_year': '2021-09-30',
        'specialization': 'Dermatology',
        'spec_reg_num': 'M12345',
        'spec_year': '2022-02-20'
    },
    {
        'id_num': 208,
        'first_name': 'Henry',
        'middle_name': 'Jowi',
        'last_name': 'Hamisi',
        'gender': 'Male',
        'license_num': 'M012345',
        'reg_year': '2018-04-17'
    },
    {
        'id_num': 209,
        'first_name': 'Irene',
        'middle_name': 'Kithue',
        'last_name': 'Mwangaza',
        'gender': 'Female',
        'license_num': 'M123456',
        'reg_year': '2020-05-01',
        'specialization': 'Oncology',
        'spec_reg_num': 'M23456',
        'spec_year': '2021-06-01'
    },
    {
        'id_num': 210,
        'first_name': 'Jack',
        'middle_name': 'Mitei',
        'last_name': 'Mutembei',
        'gender': 'Male',
        'license_num': 'M234567',
        'reg_year': '2019-07-15'
    }
]

clinical_officers = [
    {
        'id_num': 301,
        'first_name': 'Chris',
        'middle_name': 'Enkai',
        'last_name': 'Sebo',
        'gender': 'Male',
        'license_num': 'CO567890',
        'reg_year': '2020-08-18'
    },
    {
        'id_num': 302,
        'first_name': 'Patricia',
        'middle_name': 'Funyulu',
        'last_name': 'Wanyee',
        'gender': 'Female',
        'license_num': 'CO678901',
        'reg_year': '2019-05-25'
    },
    {
        'id_num': 303,
        'first_name': 'Dabasso',
        'middle_name': 'Bokayo',
        'last_name': 'Jatanny',
        'gender': 'Female',
        'license_num': 'CO789012',
        'reg_year': '2017-02-14'
    },
    {
        'id_num': 304,
        'first_name': 'Nancy',
        'middle_name': 'Atieno',
        'last_name': 'Odhiambo',
        'gender': 'Female',
        'license_num': 'CO890123',
        'reg_year': '2022-01-12'
    },
    {
        'id_num': 305,
        'first_name': 'Karen',
        'middle_name': 'Iminza',
        'last_name': 'Wee',
        'gender': 'Female',
        'license_num': 'CO901234',
        'reg_year': '2021-09-30'
    },
    {
        'id_num': 306,
        'first_name': 'James',
        'middle_name': 'Jaloch',
        'last_name': 'Hono',
        'gender': 'Male',
        'license_num': 'CO012345',
        'reg_year': '2018-04-17'
    },
    {
        'id_num': 307,
        'first_name': 'Michael',
        'middle_name': 'Kiraitu',
        'last_name': 'Murungi',
        'gender': 'Male',
        'license_num': 'CO123456',
        'reg_year': '2020-05-01'
    },
    {
        'id_num': 308,
        'first_name': 'Paul',
        'middle_name': 'Lodwar',
        'last_name': 'Lukenya',
        'gender': 'Male',
        'license_num': 'CO234567',
        'reg_year': '2019-07-15'
    },
    {
        'id_num': 309,
        'first_name': 'Alice',
        'middle_name': 'Malit',
        'last_name': 'Jeda',
        'gender': 'Female',
        'license_num': 'CO345678',
        'reg_year': '2018-03-10'
    },
    {
        'id_num': 310,
        'first_name': 'Bitanga',
        'middle_name': 'Ndemo',
        'last_name': 'Wote',
        'gender': 'Male',
        'license_num': 'CO456789',
        'reg_year': '2021-11-20'
    }
]

nurses = [
    {
        'id_num': 401,
        'first_name': 'Daniel',
        'middle_name': 'Gituu',
        'last_name': 'Marara',
        'gender': 'Male',
        'license_num': 'N789012',
        'reg_year': '2017-02-14'
    },
    {
        'id_num': 402,
        'first_name': 'Susan',
        'middle_name': 'Akinyi',
        'last_name': 'Adero',
        'gender': 'Female',
        'license_num': 'N890123',
        'reg_year': '2022-01-12'
    },
    {
        'id_num': 403,
        'first_name': 'Sarah',
        'middle_name': 'Imani',
        'last_name': 'Hawi',
        'gender': 'Female',
        'license_num': 'N901234',
        'reg_year': '2021-09-25'
    },
    {
        'id_num': 404,
        'first_name': 'Nancy',
        'middle_name': 'Jerono',
        'last_name': 'Chemutai',
        'gender': 'Female',
        'license_num': 'N012345',
        'reg_year': '2018-04-17'
    },
    {
        'id_num': 405,
        'first_name': 'Karen',
        'middle_name': 'Mulonza',
        'last_name': 'Wabwire',
        'gender': 'Female',
        'license_num': 'N123456',
        'reg_year': '2020-05-01'
    },
    {
        'id_num': 406,
        'first_name': 'James',
        'middle_name': 'Lunalo',
        'last_name': 'Lukenya',
        'gender': 'Male',
        'license_num': 'N234567',
        'reg_year': '2019-07-15'
    },
    {
        'id_num': 407,
        'first_name': 'Alice',
        'middle_name': 'Mwango',
        'last_name': 'Mwitu',
        'gender': 'Female',
        'license_num': 'N345678',
        'reg_year': '2018-03-10'
    },
    {
        'id_num': 408,
        'first_name': 'Ali',
        'middle_name': 'Nusra',
        'last_name': 'Waliye',
        'gender': 'Male',
        'license_num': 'N456789',
        'reg_year': '2021-11-20'
    },
    {
        'id_num': 409,
        'first_name': 'Patricia',
        'middle_name': 'Odhiambo',
        'last_name': 'Adhiambo',
        'gender': 'Female',
        'license_num': 'N567890',
        'reg_year': '2020-08-18'
    },
    {
        'id_num': 410,
        'first_name': 'Chris',
        'middle_name': 'Mogusu',
        'last_name': 'Bitoto',
        'gender': 'Male',
        'license_num': 'N678901',
        'reg_year': '2019-05-25'
    }
]


dietitians = [
    {
        'id_num': 501,
        'first_name': 'Emily',
        'middle_name': 'Amunansa',
        'last_name': 'Gitobu',
        'gender': 'Female',
        'license_num': 'D123456',
        'reg_year': '2015-06-20',
        'specialization': 'Clinical Nutrition',
        'spec_reg_num': 'CN123',
        'spec_year': '2017-05-14'
    },
    {
        'id_num': 502,
        'first_name': 'Jonathan',
        'middle_name': 'Bitok',
        'last_name': 'Swee',
        'gender': 'Male',
        'license_num': 'D234567',
        'reg_year': '2018-07-15'
    },
    {
        'id_num': 503,
        'first_name': 'Anna',
        'middle_name': 'Chuka',
        'last_name': 'Taa',
        'gender': 'Female',
        'license_num': 'D345678',
        'reg_year': '2016-08-10',
        'specialization': 'Pediatric Nutrition',
        'spec_reg_num': 'PN345',
        'spec_year': '2019-09-25'
    },
    {
        'id_num': 504,
        'first_name': 'Michael',
        'middle_name': 'Dege',
        'last_name': 'Bunyula',
        'gender': 'Male',
        'license_num': 'D456789',
        'reg_year': '2017-09-01'
    },
    {
        'id_num': 505,
        'first_name': 'Olivia',
        'middle_name': 'Esaili',
        'last_name': 'Mathenge',
        'gender': 'Female',
        'license_num': 'D567890',
        'reg_year': '2020-10-22',
        'specialization': 'Sports Nutrition',
        'spec_reg_num': 'SN567',
        'spec_year': '2021-11-30'
    },
    {
        'id_num': 506,
        'first_name': 'William',
        'middle_name': 'Farade',
        'last_name': 'Chute',
        'gender': 'Male',
        'license_num': 'D678901',
        'reg_year': '2019-11-12'
    },
    {
        'id_num': 507,
        'first_name': 'Sophia',
        'middle_name': 'Gatuu',
        'last_name': 'Mulembe',
        'gender': 'Female',
        'license_num': 'D789012',
        'reg_year': '2021-12-05',
        'specialization': 'Renal Nutrition',
        'spec_reg_num': 'RN789',
        'spec_year': '2022-01-18'
    },
    {
        'id_num': 508,
        'first_name': 'James',
        'middle_name': 'Hulu',
        'last_name': 'Matawi',
        'gender': 'Male',
        'license_num': 'D890123',
        'reg_year': '2018-01-25'
    },
    {
        'id_num': 509,
        'first_name': 'Isabella',
        'middle_name': 'Irungu',
        'last_name': 'Mikai',
        'gender': 'Female',
        'license_num': 'D901234',
        'reg_year': '2019-02-15',
        'specialization': 'Diabetes Nutrition',
        'spec_reg_num': 'DN901',
        'spec_year': '2020-03-22'
    },
    {
        'id_num': 510,
        'first_name': 'Benjamin',
        'middle_name': 'Jaoko',
        'last_name': 'Weya',
        'gender': 'Male',
        'license_num': 'D012345',
        'reg_year': '2020-03-10'
    }
]


lab_techs = [
    {
        'id_num': 601,
        'first_name': 'Alice',
        'middle_name': 'Aoko',
        'last_name': 'Mula',
        'gender': 'Female',
        'license_num': 'LT123456',
        'reg_year': '2015-06-20'
    },
    {
        'id_num': 602,
        'first_name': 'Brian',
        'middle_name': 'Bosire',
        'last_name': 'Ochwea',
        'gender': 'Male',
        'license_num': 'LT234567',
        'reg_year': '2018-07-15'
    },
    {
        'id_num': 603,
        'first_name': 'Carol',
        'middle_name': 'Chido',
        'last_name': 'Were',
        'gender': 'Female',
        'license_num': 'LT345678',
        'reg_year': '2016-08-10'
    },
    {
        'id_num': 604,
        'first_name': 'David',
        'middle_name': 'Omwami',
        'last_name': 'Bunde',
        'gender': 'Male',
        'license_num': 'LT456789',
        'reg_year': '2017-09-01'
    },
    {
        'id_num': 605,
        'first_name': 'Eva',
        'middle_name': 'Elosy',
        'last_name': 'Jonyo',
        'gender': 'Female',
        'license_num': 'LT567890',
        'reg_year': '2020-10-22'
    },
    {
        'id_num': 606,
        'first_name': 'Frank',
        'middle_name': 'Ragira',
        'last_name': 'Dorore',
        'gender': 'Male',
        'license_num': 'LT678901',
        'reg_year': '2019-11-12'
    },
    {
        'id_num': 607,
        'first_name': 'Grace',
        'middle_name': 'Gweno',
        'last_name': 'Gwere',
        'gender': 'Female',
        'license_num': 'LT789012',
        'reg_year': '2021-12-05'
    },
    {
        'id_num': 608,
        'first_name': 'Henry',
        'middle_name': 'Inda',
        'last_name': 'Malit',
        'gender': 'Male',
        'license_num': 'LT890123',
        'reg_year': '2018-01-25'
    },
    {
        'id_num': 609,
        'first_name': 'Ivy',
        'middle_name': 'Liet',
        'last_name': 'Miliny',
        'gender': 'Female',
        'license_num': 'LT901234',
        'reg_year': '2019-02-15'
    },
    {
        'id_num': 610,
        'first_name': 'Jack',
        'middle_name': 'Jaba',
        'last_name': 'Welukhye',
        'gender': 'Male',
        'license_num': 'LT012345',
        'reg_year': '2020-03-10'
    }
]


pharmacists = [
    {
        'id_num': 701,
        'first_name': 'Kate',
        'middle_name': 'Kiragu',
        'last_name': 'Adwar',
        'gender': 'Female',
        'license_num': 'P123456',
        'reg_year': '2015-06-20',
        'specialization': 'Clinical Pharmacy',
        'spec_reg_num': 'CP123',
        'spec_year': '2017-05-14'
    },
    {
        'id_num': 702,
        'first_name': 'Leo',
        'middle_name': 'Lumumba',
        'last_name': 'Wavinya',
        'gender': 'Male',
        'license_num': 'P234567',
        'reg_year': '2018-07-15'
    },
    {
        'id_num': 703,
        'first_name': 'Mia',
        'middle_name': 'Amisi',
        'last_name': 'Saidi',
        'gender': 'Female',
        'license_num': 'P345678',
        'reg_year': '2016-08-10',
        'specialization': 'Oncology Pharmacy',
        'spec_reg_num': 'OP345',
        'spec_year': '2019-09-25'
    },
    {
        'id_num': 704,
        'first_name': 'Nate',
        'middle_name': 'Sirwa',
        'last_name': 'Kinembe',
        'gender': 'Male',
        'license_num': 'P456789',
        'reg_year': '2017-09-01'
    },
    {
        'id_num': 705,
        'first_name': 'Olivia',
        'middle_name': 'Ogwede',
        'last_name': 'Wahu',
        'gender': 'Female',
        'license_num': 'P567890',
        'reg_year': '2020-10-22',
        'specialization': 'Pediatric Pharmacy',
        'spec_reg_num': 'PP567',
        'spec_year': '2021-11-30'
    },
    {
        'id_num': 706,
        'first_name': 'Paul',
        'middle_name': 'Pwani',
        'last_name': 'Lote',
        'gender': 'Male',
        'license_num': 'P678901',
        'reg_year': '2019-11-12'
    },
    {
        'id_num': 707,
        'first_name': 'Quinn',
        'middle_name': 'Kwisero',
        'last_name': 'Nyamita',
        'gender': 'Female',
        'license_num': 'P789012',
        'reg_year': '2021-12-05',
        'specialization': 'Geriatric Pharmacy',
        'spec_reg_num': 'GP789',
        'spec_year': '2022-01-18'
    },
    {
        'id_num': 708,
        'first_name': 'Rachel',
        'middle_name': 'Rukia',
        'last_name': 'Kunde',
        'gender': 'Female',
        'license_num': 'P890123',
        'reg_year': '2018-01-25'
    },
    {
        'id_num': 709,
        'first_name': 'Sam',
        'middle_name': 'Sidho',
        'last_name': 'Bare',
        'gender': 'Male',
        'license_num': 'P901234',
        'reg_year': '2019-02-15',
        'specialization': 'Hospital Pharmacy',
        'spec_reg_num': 'HP901',
        'spec_year': '2020-03-22'
    },
    {
        'id_num': 710,
        'first_name': 'Tina',
        'middle_name': 'Tuei',
        'last_name': 'Sang',
        'gender': 'Female',
        'license_num': 'P012345',
        'reg_year': '2020-03-10'
    }
]

physiotherapists = [
    {
        'id_num': 716,
        'first_name': 'Mark',
        'middle_name': 'Mulinge',
        'last_name': 'Tula',
        'gender': 'Male',
        'license_num': 'PH123456',
        'reg_year': '2008-07-10'
    },
    {
        'id_num': 717,
        'first_name': 'Anna',
        'middle_name': 'Anita',
        'last_name': 'Chesang',
        'gender': 'Female',
        'license_num': 'PH234567',
        'reg_year': '2011-11-25'
    },
    {
        'id_num': 718,
        'first_name': 'Richard',
        'middle_name': 'Rwee',
        'last_name': 'Adera',
        'gender': 'Male',
        'license_num': 'PH345678',
        'reg_year': '2014-03-30'
    },
    {
        'id_num': 719,
        'first_name': 'Julia',
        'middle_name': 'Jasiri',
        'last_name': 'Matendo',
        'gender': 'Female',
        'license_num': 'PH456789',
        'reg_year': '2017-06-15'
    },
    {
        'id_num': 720,
        'first_name': 'Daniel',
        'middle_name': 'Dibu',
        'last_name': 'Gachuki',
        'gender': 'Male',
        'license_num': 'PH567890',
        'reg_year': '2020-02-20'
    },
    {
        'id_num': 721,
        'first_name': 'Emma',
        'middle_name': 'Wanyoike',
        'last_name': 'Weitethia',
        'gender': 'Female',
        'license_num': 'PH678901',
        'reg_year': '2023-05-05'
    }
]

psychologists = [
    {
        'id_num': 710,
        'first_name': 'John',
        'middle_name': 'Jwala',
        'last_name': 'Dote',
        'gender': 'Male',
        'license_num': 'PY123456',
        'reg_year': '2010-05-15',
        'specialization': 'Clinical Psychology',
        'spec_reg_num': 'CL123',
        'spec_year': '2012-08-20'
    },
    {
        'id_num': 711,
        'first_name': 'Jane',
        'middle_name': 'Jicho',
        'last_name': 'Sinde',
        'gender': 'Female',
        'license_num': 'PY234567',
        'reg_year': '2012-09-20',
        'specialization': 'Counseling Psychology',
        'spec_reg_num': 'CO456',
        'spec_year': '2014-03-10'
    },
    {
        'id_num': 712,
        'first_name': 'Michael',
        'middle_name': 'Makau',
        'last_name': 'Metoo',
        'gender': 'Male',
        'license_num': 'PY345678',
        'reg_year': '2015-11-30',
        'specialization': 'Child Psychology',
        'spec_reg_num': 'CH789',
        'spec_year': '2017-06-25'
    },
    {
        'id_num': 713,
        'first_name': 'Emily',
        'middle_name': 'Emunyasi',
        'last_name': 'Batongolo',
        'gender': 'Female',
        'license_num': 'PY456789',
        'reg_year': '2018-04-12',
        'specialization': 'Forensic Psychology',
        'spec_reg_num': 'FO321',
        'spec_year': '2020-01-15'
    },
    {
        'id_num': 714,
        'first_name': 'David',
        'middle_name': 'Dangote',
        'last_name': 'Aliko',
        'gender': 'Male',
        'license_num': 'PY567890',
        'reg_year': '2020-08-03',
        'specialization': 'Health Psychology',
        'spec_reg_num': 'HE654',
        'spec_year': '2022-04-28'
    },
    {
        'id_num': 715,
        'first_name': 'Sarah',
        'middle_name': 'Suraya',
        'last_name': 'Lekungu',
        'gender': 'Female',
        'license_num': 'PY678901',
        'reg_year': '2023-01-10',
        'specialization': 'Industrial-Organizational Psychology',
        'spec_reg_num': 'IO987',
        'spec_year': '2024-05-30'
    }
]
