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

MikaRoll: bytes = pickle.loads(R.content)["Packages"]["TSN_Abstracter¤Stable"];
with open("TSN_Abstracter¤Stable.MikaRoll", "w+b") as f: f.write(MikaRoll);

Log.Stateless(f"MikaRoll Archive v{".".join([str(x) for x in MikaRoll[8:11]])}");
HeaderSize: int = int.from_bytes(MikaRoll[11:13], "little");
Log.Stateless(f"MikaRoll Header Size: {HeaderSize}");
print(json.dumps(json.loads(lzma.decompress(MikaRoll[16 : HeaderSize+16], lzma.FORMAT_XZ)), indent=2));
Data: dict[str, dict[str, bytes]] = pickle.loads(lzma.decompress(MikaRoll[HeaderSize+16:], lzma.FORMAT_XZ));
print(f"Script Files ({len(Data["Scripts"].keys())}):\n{Data["Scripts"].keys()}");
print(f"Data Files ({len(Data["Data"].keys())}):\n{Data["Data"].keys()}");