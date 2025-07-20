import requests

API_KEY = "135457U6df9439ad521011cedc614ab5e4405a0"
COUNTRY = 2  # Казахстан по твоим данным

resp = requests.get(
    "https://smshub.org/stubs/handler_api.php",
    params={"api_key": API_KEY, "action": "getPrices", "country": COUNTRY}
)

try:
    data = resp.json()
except Exception as e:
    print("Ошибка при чтении JSON:", e)
    print("Ответ:", resp.text)
    exit()

print("🔍 Доступные сервисы для country=2:")
for service, info in data.get(str(COUNTRY), {}).items():
    # выведем только сервисы с номерами
    if info.get("count", 0) > 0:
        print(f"- {service}: count={info['count']}, price={info['cost']}")
