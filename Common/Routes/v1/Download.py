from ...Globals import *;
from ... import Package;
import lzma, pickle, json;






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
			if (cpkg["Name"] == pkg[0]): pkgIndex = i; break;
		if (pkgIndex == -1): nagisa_downloads["Error"].append(f"Package \"{pkg[0]}\" does not exist."); continue;

		# Verify Package Option Exists
		optIndex: int = -1;
		for i, copt in enumerate(Cached["Packages"][pkgIndex]["Options"]):
			if (copt["Name"] == pkg[1]): optIndex = i; break;
		if (optIndex == -1): nagisa_downloads["Error"].append(f"Package Option \"{pkg[1]}\" for \"{pkg[0]}\" does not exist."); continue;


		# Add Files
		mpkg: Type.Nagisa_Download = {
			"Name": "¤".join(pkg),
			"Files": [
				{
					"File": "Adellian.mpkg",
					"Data": json.dumps(Cached["Packages"][pkgIndex]).encode()
				}
			]
		};

		# Figure out a way to add everything it needs for installation here, might need an update to the MikaPKG Format

		nagisa_downloads["Packages"].append(mpkg);
	return fastapi.Response(
		lzma.compress(
			pickle.dumps(nagisa_downloads),
			format=lzma.FORMAT_XZ, preset=9 | lzma.PRESET_EXTREME
		), media_type="binary/octet-stream"
	);