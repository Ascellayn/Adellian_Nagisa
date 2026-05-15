# Adellian "Mika" Package Distributor *(Adellian "Nagisa")*
This is a FastAPI-Based Backend Server that delivers to the Adellian Package Manager a way to easily download Adellian Packages (auto-updating) and Debian Packages that Adellian has patches for.  

## Mika Package Format
Adellian Repositories must have a folder named `.adellian` containing files ending in `.mpkg` with the following JSON:
```json
{
	"ID": str,
	"Type": Literal["Adellian", "Debian"],
	"Name": str,
	"Description": str,
	"Version": tuple[int, ...] | None,
	"Required": Literal["Eleison", "Kyrie", "Server"] | None,
	"Dependencies": list[str(f'{Type}¤{Name}')],
	"Default": Literal["Eleison", "Kyrie", "Server"] | None,
	"Conflicts": list[str(f'{Type}¤{Name}')],
	"Options": list[
		{
			"Scripts": {
				"Install": str,
				"Uninstall": str,
				"Updater": str | None
			},
			"Name": str,
			"Description": str
		},
		...
	],
	"Data": [
		str
	]
}
```
Nagisa automatically detects every `.mpkg` files and automatically builds `.MikaArchive` files in `.cache` to be easily distributed to clients.

<br>

### WHY?
idk i'm stupid  
This uses HTTP bullshit so do mind that this is probably the SLOWEST package manager on the planet.  
I could write this with raw sockets to make it competitive but I decided to not bother because at that point I'd just write the whole thing in C.  
Or you know. APT / Pacman exists so I shouldn't even bother.  
But I'm out here having fun so please politely piss off.  