from typing import TypedDict, Literal;





type Adellian_Branches = Literal["Eleison", "Kyrie", "Server"];





class Package_Scripts(TypedDict):
	Data: str;
	Install: str;
	Uninstall: str;
	Update: str | None;



class Package_Option(TypedDict):
	Scripts: Package_Scripts;
	Name: str;
	Description: str;



class MikaPackage(TypedDict):
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
	Data: tuple[list[str], list[str]];



class MikaArchive(TypedDict):
	_VERSION: tuple[int, int, int];
	Package: MikaPackage;
	Scripts: dict[str, bytes];
	Data: dict[str, bytes];










class Nagisa_Packages(TypedDict):
	Last_Update: int;
	Error: list[str];
	Packages: list[MikaPackage];



class Nagisa_Files(TypedDict):
	File: str;
	Data: bytes;



class Nagisa_Download(TypedDict):
	ID: str;
	Archive: bytes;



class Nagisa_Downloads(TypedDict):
	Error: list[str];
	Packages: list[Nagisa_Download];










class Request_Download(TypedDict):
	Packages: list[tuple[str, str]]