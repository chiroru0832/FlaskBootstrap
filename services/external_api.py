import requests

def fetch_users():
    # 外部APIのURL
    api_url = "https://randomuser.me/api/"
    
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # エラーがあれば例外をスロー
        data = response.json()
        
        # 必要なデータを抽出
        users = []
        for item in data.get("results", []):
            user = {
                "first_name": item["name"]["first"],
                "last_name": item["name"]["last"],
                "email": item["email"],
                "phone": item.get("phone", ""),
                "city": item["location"]["city"],
                "state": item["location"]["state"],
                "country": item["location"]["country"],
                "profile_picture": item["picture"]["large"]
            }
            users.append(user)
        
        return users
    except requests.RequestException as e:
        print(f"Error fetching data from external API: {e}")
        return []
