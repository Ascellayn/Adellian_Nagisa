from .Globals import *;
import httpx, json;



class Acquire:
	@staticmethod
	async def All() -> Type.Nagisa_Packages:
		global Packages_Cached, Packages_Lock;
		while (Packages_Lock): await asyncio.sleep(1);

		if ((Time.Get_Unix() - Packages_Cached["Last_Update"]) < (Time.Unit_Unix.Minute * 5)): return Packages_Cached;

		Packages_Lock = True;
		mPKGS: Type.Nagisa_Packages = await Acquire.Adellian();
		mPKGS["Packages"] += await Acquire.Debian();
		mPKGS["Last_Update"] = Time.Get_Unix();

		Packages_Cached = mPKGS;
		Packages_Lock = False;
		return mPKGS;



	@staticmethod
	async def Adellian() -> Type.Nagisa_Packages:
		# This code could be optimized... This is all synchronous which is bad because that means zero parallelization.
		# Nagisa is pretty small and quite a useless project, I don't think I need to optimize this for thousands of people. It'll do for 1 person.
		pkgs: Type.Nagisa_Packages = {
			"Last_Update": 0,
			"Error": [],
			"Packages": []
		};
		for i, REPO in enumerate(REPOSITORIES, start=1):
			Log.Stateless(f"GET [{i}/{len(REPOSITORIES)}]: {REPO}...");
			u_init: float = Time.Get_Unix(True);
			try:
				MPKG: httpx.Response = httpx.get(REPO + ".adellian/Adellian.mpkg", headers=HEADERS);
				if (MPKG.status_code != 200): raise Exception(f"Invalid HTTP Code \"{MPKG.status_code}\"");
				pkgs["Packages"].append(cast(Type.Package_Mika, json.loads(MPKG.read())));
				Log.Awaited().OK(f"{round((Time.Get_Unix(True) - u_init) * 1000)}ms");

			except Exception as E:
				Log.Awaited().EXCEPTION(E, Traceback=False);
				pkgs["Error"].append(REPO);

		return pkgs;



	@staticmethod
	async def Debian() -> list[Type.Package_Mika]:
		pkgs: list[Type.Package_Mika] = [];
		for F in File.List("Packages/Debian")[0]:
			pkgs.append(cast(Type.Package_Mika, File.JSON_Read(f"Packages/Debian/{F}/Adellian.mpkg")));

		return pkgs;