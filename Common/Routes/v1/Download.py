from ...Globals import *;
from ... import Package;
import pickle;





def __Read(P: str) -> bytes:
	with open(P, "r+b") as f: return f.read();



@API.post("/v1/Download", tags=["Nagisa"], response_class=fastapi.Response)
async def Download(Requested: Type.Request_Download) -> fastapi.Response:
	await Package.Acquire.All();

	# If this looks horrible that's because it is.
	nagisa_downloads: Type.Nagisa_Downloads = {
		"Error": [],
		"Packages": {}
	};
	for pkg in Requested["Packages"]:
		id: str = f"{pkg[0]}¤{pkg[1]}";
		if (not File.Exists(f".cache/{id}.MikaRoll")): raise Not_Found(f"Package \"{id}\" does not exist.");
	
		nagisa_downloads["Packages"][f"{pkg[0]}¤{pkg[1]}"] = __Read(f".cache/{id}.MikaRoll");

	return fastapi.Response(pickle.dumps(nagisa_downloads), media_type="binary/octet-stream");