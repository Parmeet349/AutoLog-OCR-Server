import requests

url = "http://127.0.0.1:8000/api/ocr"
# files = {"file": open("shell.jpg", "rb")}
# files = {"file": ("shell.jpg", open("shell.jpg", "rb"), "image/jpeg")}
# C:\Personal\AutoLog\autolog-ocr\shell.jpg

# Use the above path
files = {"file": ("test_image.jpg", open("C:/Personal/AutoLog/autolog-ocr/test_image.jpg", "rb"), "image/jpeg")}

response = requests.post(url, files=files)
print(response.json())