from ...Globals import *;
from ... import Package;
import lzma, pickle, json;






def __FileRead(P: str) -> bytes:
	with open(P, "r+b") as F:
		return F.read();



def __MikaArchive(BASE: str, P: str = "./", MikaArchive: dict[str, Any] = {}) -> dict[str, bytes]:
	T: File.Folder_Contents = File.List(BASE);

	for f in T[1]: MikaArchive[f"{P}/{f}"] = __FileRead(f"{BASE}/{f}");
	for f in T[0]:
		for m in __MikaArchive(f"{BASE}/{f}", f"{P}/{f}").items():
			MikaArchive[m[0]] = m[1];

	return MikaArchive;





@API.post("/v1/Download", tags=["Nagisa"], response_class=fastapi.Response)
async def Download(Requested: Type.Request_Download) -> fastapi.Response:
	Cached: Type.Nagisa_Packages = await Package.Acquire.All();

	# If this looks horrible that's because it is.
	nagisa_downloads: Type.Nagisa_Downloads = {
		"Error": [],
		"Packages": []
	};
	for pkg in Requested["Packages"]:
		# Verify Package Exists
		pkgIndex: int = -1;
		for i, cpkg in enumerate(Cached["Packages"]):
			if (cpkg["ID"] == pkg[0]): pkgIndex = i; break;
		if (pkgIndex == -1): nagisa_downloads["Error"].append(f"Package \"{pkg[0]}\" does not exist."); continue;

		# Verify Package Option Exists
		optIndex: int = -1;
		for i, copt in enumerate(Cached["Packages"][pkgIndex]["Options"]):
			if (copt["Name"] == pkg[1]): optIndex = i; break;
		if (optIndex == -1): nagisa_downloads["Error"].append(f"Package Option \"{pkg[1]}\" for \"{pkg[0]}\" does not exist."); continue;


		# Add Files
		npkg: Type.Nagisa_Download = {
			"ID": pkg[0],
			"Archive": pickle.dumps(__MikaArchive(f"./.cache/{pkg[0]}/"))
		};


		nagisa_downloads["Packages"].append(npkg);
	return fastapi.Response(
		lzma.compress(
			pickle.dumps(nagisa_downloads),
			format=lzma.FORMAT_XZ, preset=9 | lzma.PRESET_EXTREME
		), media_type="binary/octet-stream"
	);