import re,requests

def get_address(pincode):
    url = f'https://api.postalpincode.in/pincode/{pincode}'
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        try:
            data=data[0]["PostOffice"][0]
            address=[data["District"],data["State"],data["Pincode"]]
        except:
            return None
        return ",".join(address)
    except:
        return None

def extract_info(entry):
    name_pattern = r"नाम\s*(.*?)\s*जन्म"
    dob_pattern = r"जन्म\s*तिथि\s*(.*?)\s*कक्षा"
    mobile_pattern = r"(\d{10,13})"
    pincode=r"पिन\s*कोड(.*?)\s*प्रदेश"
    name_match = re.search(name_pattern, entry)
    dob_match = re.search(dob_pattern, entry)
    mobile_match = re.search(mobile_pattern, entry)
    pin_match=re.search(pincode, entry)
    details={"name":None,"dob":None,"mobile":None,"address":None}
    if name_match:
        details["name"] = name_match.group(1)        
    if dob_match:
        details["dob"] = dob_match.group(1)
    if mobile_match:
        details["mobile"] = mobile_match.group(1)
    if pin_match:
        pin=pin_match.group(1)
        address=get_address(pin)
        if address is not None:
            details["address"] = address
        else:
            details["address"] = pin
    return details