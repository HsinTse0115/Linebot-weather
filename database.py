USER_CITIES = {
    'U3632271fc7f921b0eaf90c70131f4552': '台中市',
    'U4d47bd2cb93cb8010cbbe2f503a1e92e': '新竹市',
    'Udcbad5bd52eb511d2ff11f1d9870a7ac': '台北市',
    'Ucddbe415236a1013269854098fae9ee7': '彰化市'
}

def get_user_city(user_id):
    return USER_CITIES.get(user_id)

def set_user_city(user_id, city):
    USER_CITIES[user_id] = city