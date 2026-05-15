from .Globals import *;
from . import Package;
import contextlib;



@contextlib.asynccontextmanager
async def Lifespan(App: fastapi.FastAPI):
	global Packages_Cached;
	TSN_Abstracter.App_Init(True);
	File.Path_Require(".cache/");

	if (File.Exists("Nagisa.cache")): Packages_Cached = cast(Type.Nagisa_Packages, File.JSON_Read("Nagisa.cache", True));
	else: await Package.Acquire.All();



	Log.Info(f"Ready to serve packages.");
	yield;
