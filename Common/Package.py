from .Globals import *;
import httpx;
import io, shutil, zipfile;
import multiprocessing;



class Acquire:
	@staticmethod
	async def All() -> Type.Nagisa_Packages:
		global Packages_Cached, Packages_Lock;
		while (Packages_Lock): await asyncio.sleep(1);

		if ((Time.Get_Unix() - Packages_Cached["Last_Update"]) < (Time.Unit_Unix.Minute * 5)): return Packages_Cached;

		Packages_Lock = True;
		mPKGS: Type.Nagisa_Packages = await Acquire.Cache();
		mPKGS["Last_Update"] = Time.Get_Unix();

		Packages_Cached = mPKGS;
		Packages_Lock = False;
		return mPKGS;





	@staticmethod
	async def Cache() -> Type.Nagisa_Packages:
		pkgs: Type.Nagisa_Packages = {
			"Last_Update": 0,
			"Error": [],
			"Packages": []
		};
		shutil.rmtree("./.cache/"); File.Path_Require("./.cache");
		with multiprocessing.Pool() as P:
			RESULTS: list[Type.Nagisa_Packages] = P.map(Acquire.Download, [x for x in enumerate(REPOSITORIES, start=1)]);
		for R in RESULTS:
			pkgs["Error"] += R["Error"];
			pkgs["Packages"] += R["Packages"];

		return pkgs;



	@staticmethod
	def Download(X: tuple[int, str]) -> Type.Nagisa_Packages:
		i: int = X[0]; REPO: str = X[1];
		pkgs: Type.Nagisa_Packages = {
			"Last_Update": 0,
			"Error": [],
			"Packages": []
		};
		Log.Stateless(f"GET [{i}/{len(REPOSITORIES)}]: {REPO}...");
		u_init: float = Time.Get_Unix(True);
		try:
			MPKG: httpx.Response = httpx.get(REPO, headers=HEADERS, follow_redirects=True);
			if (MPKG.status_code != 200): raise Exception(f"Invalid HTTP Code \"{MPKG.status_code}\"");

			archive: zipfile.ZipFile = zipfile.ZipFile(io.BytesIO(MPKG.content)); del MPKG;
			archive.extractall(f"./.cache/{i}"); del archive;

			path: str = f"./.cache/{i}/{File.List(f'./.cache/{i}/')[0][0]}";

			if (not File.Exists(f"{path}/.adellian/Adellian.mpkg")): raise Exception(f"{REPO}: Adellian.mpkg not found!");
			pkgs["Packages"].append(cast(Type.Package_Mika, File.JSON_Read(f"{path}/.adellian/Adellian.mpkg")));

			Log.Awaited().OK(f"{round((Time.Get_Unix(True) - u_init) * 1000)}ms");

		except Exception as E:
			Log.Awaited().EXCEPTION(E, Traceback=False);
			pkgs["Error"].append(REPO);

		return pkgs;