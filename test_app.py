import json
import urllib.request
import urllib.error

BASE_URL = "http://127.0.0.1:8006"

def test_health():
    with urllib.request.urlopen(BASE_URL + "/health") as response:
        assert response.status == 200

def test_attendance():
    with urllib.request.urlopen(BASE_URL + "/attendance") as response:
        data = json.loads(response.read().decode("utf-8"))
        assert data["version"] == "0.5.0"
        assert data["present"] == 3
        assert data["total"] == 5

def test_unknown_route():
    try:
        urllib.request.urlopen(BASE_URL + "/unknown")
        raise AssertionError("Ожидался HTTP 404")
    except urllib.error.HTTPError as error:
        assert error.code == 404

if __name__ == "__main__":
    test_health()
    test_attendance()
    test_unknown_route()
    print("Все автоматизированные тесты пройдены!")