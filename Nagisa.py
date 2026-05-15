from Common import *;



@API.get("/", tags=["Nagisa"])
async def Root() -> Type.Nagisa_Packages:
	""" Acquire every Adellian and Debian Packages that Nagisa knows."""
	return await Package.Acquire.All();