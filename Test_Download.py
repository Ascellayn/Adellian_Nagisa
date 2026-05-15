from TSN_Abstracter import *;
import httpx, lzma, pickle;

data = {
	"Packages": [
		[
			"TSN_Abstracter",
			"Stable"
		]
	]
};

R: httpx.Response = httpx.post("http://127.0.0.1:8000/v1/Download", json=data);
if (R.status_code != 200): print(R.content);
else: print(pickle.loads(R.content));