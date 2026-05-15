from TSN_Abstracter import *;
import asyncio, fastapi, pydantic;
App.JSON(cast(dict[str, Any], File.JSON_Read("App.tsna")));

from . import Type;



# Global Constants
API: fastapi.FastAPI = fastapi.FastAPI(
	title=App.Name, summary=App.Description, version=".".join(String.ify_Array(App.Version)),
	debug=False, root_path="/",
	openapi_tags=[
		{
			"name": "Nagisa",
			"description": "Adellian Mika Package Distributor Routes"
		}
	],
	contact={
		"name": "The Sirio Network",
		"url": "https://sirio-network.com/contact",
		"email": "contact+mika@sirio-network.com"
	},
	license_info={
		"name": App.License,
		"url": "https://sirio-network.com/license/2.2"
	}
);
HEADERS: dict[str, str] = { "User-Agent": f"Nagisa/{'.'.join(String.ify_Array(App.Version))} (+https://github.com/Ascellayn/Adellian_Nagisa)" };
REPOSITORIES: list[str] = cast(list[str], File.JSON_Read("Repositories.json"));



# Global Variables
Packages_Lock: bool = False;
Packages_Cached: Type.Nagisa_Packages = {
	"Last_Update": 0,
	"Error": REPOSITORIES,
	"Packages": []
};



File.Path_Require("Packages/Adellian");
File.Path_Require("Packages/Debian");
File.Path_Require(".cache/");