from TSN_Abstracter import *;
import httpx, lzma, pickle;

data = {
	"Packages": [
		[
			"com.sirio-network.tsna+stable",
			"Stable"
		]
	]
};

R: httpx.Response = httpx.post("http://127.0.0.1:8000/v1/Download", json=data);
print(pickle.loads(lzma.decompress(R.content, lzma.FORMAT_XZ)));