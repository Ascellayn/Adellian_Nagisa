from TSN_Abstracter import *;
import asyncio, fastapi, pydantic;
App.JSON(cast(dict[str, Any], File.JSON_Read("App.tsna")));

from . import Type;
from . import Middleware;





# Global Constants (Pre-FastAPI)
HEADERS: dict[str, str] = { "User-Agent": f"Nagisa/{'.'.join(String.ify_Array(App.Version))} (+https://github.com/Ascellayn/Adellian_Nagisa)" };
REPOSITORIES: list[str] = cast(list[str], File.JSON_Read("Repositories.json"));





# Wrapper for Exceptions just so we can detect it properly in the Error Handler and report a different HTTP Code
class Not_Found(Exception): ...;
class Unauthorized(Exception): ...;
class Bad_Request(Exception): ...;



# Global Variables
Packages_Lock: bool = False;
Packages_Cached: Type.Nagisa_Packages = {
	"Last_Update": 0,
	"Error": REPOSITORIES,
	"Packages": []
};



from Common.Routine import Lifespan;



# Global Constants
API: fastapi.FastAPI = fastapi.FastAPI(
	title=App.Name, summary=App.Description, version=".".join(String.ify_Array(App.Version)),
	debug=False, root_path="/", lifespan=Lifespan,
	openapi_tags=[
		{
			"name": "Nagisa",
			"description": "Adellian Mika Package Distributor Routes"
		}
	],
	contact={
		"name": "The Sirio Network",
		"url": "https://sirio-network.com/contact",
		"email": "contact+nagisa@sirio-network.com"
	},
	license_info={
		"name": App.License,
		"url": "https://sirio-network.com/license/2.2"
	}
);
API.middleware("http")(Middleware.Exception_Handler);