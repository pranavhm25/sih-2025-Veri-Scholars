import urllib.request
import urllib.parse
import json
import time

# Create a dummy multipart form data
boundary = '----WebKitFormBoundary7MA4YWxkTrZu0gW'
body = (
    f'--{boundary}\r\n'
    'Content-Disposition: form-data; name="file"; filename="test.png"\r\n'
    'Content-Type: image/png\r\n\r\n'
    '\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x0a\x00\x00\x00\x0a\x08\x02\x00\x00\x00\x02\xeb\x35\x07\x00\x00\x00\x0cIDATx\x9cc\xf8\xff\xff\x3f\x00\x05\x80\x01\x01\x8f\x0e\x1c\x14\x00\x00\x00\x00IEND\xaeB`\x82\r\n'
    f'--{boundary}--\r\n'
).encode('utf-8')

url = "https://veri-scholars.onrender.com/api/verify/upload"

req = urllib.request.Request(url, data=body)
req.add_header('Content-Type', f'multipart/form-data; boundary={boundary}')

print("Uploading dummy image...")
try:
    with urllib.request.urlopen(req) as response:
        print("Status:", response.status)
        resp_data = json.loads(response.read().decode('utf-8'))
        print("Response JSON:", resp_data)
        
        job_id = resp_data.get("job_id")
        if job_id:
            print("Polling status for job:", job_id)
            for _ in range(10):
                time.sleep(2)
                status_url = f"https://veri-scholars.onrender.com/api/verify/status/{job_id}"
                with urllib.request.urlopen(status_url) as status_resp:
                    status_json = json.loads(status_resp.read().decode('utf-8'))
                    print("Status JSON:", status_json)
                    if status_json.get("status") in ["completed", "failed"]:
                        break
except Exception as e:
    print("Error:", e)
