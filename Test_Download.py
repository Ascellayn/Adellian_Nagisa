from TSN_Abstracter import *;
import httpx, lzma, json, pickle;

data = {
	"Packages": [
		[
			"TSN_Abstracter",
			"Stable"
		]
	]
};

R: httpx.Response = httpx.post("http://127.0.0.1:7040/v1/Download", json=data);
if (R.status_code != 200): print(R.content);
else: Log.Info(f"{len(R.content)} bytes downloaded.");
with open("TSN_Abstracter¤Stable.MikaArchive", "w+b") as f: f.write(R.content);

Log.Stateless(f"MikaPackage Information:");
print(
	pickle.loads(
		lzma.decompress(
			pickle.loads(R.content)["Packages"][0]["Archive"]
		, lzma.FORMAT_XZ)
	)["Package"]
);