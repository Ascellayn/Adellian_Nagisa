from typing import TypedDict, Literal;





type Adellian_Branches = Literal["Eleison", "Kyrie", "Server"];





class Package_Scripts(TypedDict):
	Install: str;
	Uninstall: str;
	Update: str | None;



class Package_Option(TypedDict):
	Scripts: Package_Scripts;
	Name: str;
	Description: str;



class Package_Mika(TypedDict):
	""" Adellian .MikaPackage JSON Format"""
	ID: str;
	Type: Literal["Adellian", "Debian"];
	Name: str;
	Description: str;
	Version: tuple[int, ...] | None;
	Required: list[Literal[Adellian_Branches]];
	Default: list[Literal[Adellian_Branches]];
	Dependencies: list[str];
	Conflicts: list[str];
	Options: list[Package_Option];










class Nagisa_Packages(TypedDict):
	Last_Update: int;
	Error: list[str];
	Packages: list[Package_Mika];



class Nagisa_Files(TypedDict):
	File: str;
	Data: bytes;



class Nagisa_Download(TypedDict):
	ID: str;
	Files: list[Nagisa_Files];



class Nagisa_Downloads(TypedDict):
	Error: list[str];
	Packages: list[Nagisa_Download];










class Request_Download(TypedDict):
	Packages: list[tuple[str, str]]