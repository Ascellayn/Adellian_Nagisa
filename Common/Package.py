from .Globals import *;
import httpx;
import io, os, shutil, zipfile;
import multiprocessing;



class Acquire:
	@staticmethod
	async def All() -> Type.Nagisa_Packages:
		global Packages_Cached, Packages_Lock;
		while (Packages_Lock): await asyncio.sleep(1);

		if ((Time.Get_Unix() - Packages_Cached["Last_Update"]) < (Time.Unit_Unix.Minute * 5)): return Packages_Cached;

		Packages_Lock = True;
		NagisaPKGs: Type.Nagisa_Packages = await Acquire.Cache();
		NagisaPKGs["Last_Update"] = Time.Get_Unix();

		Packages_Cached = NagisaPKGs;
		Packages_Lock = False;
		return NagisaPKGs;





	@staticmethod
	async def Cache() -> Type.Nagisa_Packages:
		NagisaPKGs: Type.Nagisa_Packages = {
			"Last_Update": 0,
			"Error": [],
			"Packages": []
		};
		shutil.rmtree("./.cache/"); File.Path_Require("./.cache");
		with multiprocessing.Pool() as P:
			RESULTS: list[Type.Nagisa_Packages] = P.map(Acquire.Download, [x for x in enumerate(REPOSITORIES, start=1)]);
		for R in RESULTS:
			NagisaPKGs["Error"] += R["Error"];
			NagisaPKGs["Packages"] += R["Packages"];

		return NagisaPKGs;



	@staticmethod
	def Download(X: tuple[int, str]) -> Type.Nagisa_Packages:
		i: int = X[0]; REPO: str = X[1];
		NagisaPKGs: Type.Nagisa_Packages = {
			"Last_Update": 0,
			"Error": [],
			"Packages": []
		};
		Log.Stateless(f"GET [{i}/{len(REPOSITORIES)}]: {REPO}...");
		u_init: float = Time.Get_Unix(True);
		try:
			# Download Repo
			R: httpx.Response = httpx.get(REPO, headers=HEADERS, follow_redirects=True);
			if (R.status_code != 200): raise Exception(f"Invalid HTTP Code \"{R.status_code}\"");

			# Extract it
			A: zipfile.ZipFile = zipfile.ZipFile(io.BytesIO(R.content)); del R;
			A.extractall(f"./.cache/{i}"); del A;
			path: str = f"./.cache/{i}/{File.List(f'./.cache/{i}/')[0][0]}";

			# Delete if invalid
			if (not File.Exists(f"{path}/.adellian/Adellian.mpkg")):
				shutil.rmtree(f"./.cache/{i}");
				raise Exception(f"{REPO}: Adellian.mpkg not found!");

			# Read Mika Package and clean up undistributed files
			mPKG: Type.Package_Mika = cast(Type.Package_Mika, File.JSON_Read(f"{path}/.adellian/Adellian.mpkg"));
			NagisaPKGs["Packages"].append(mPKG);


			# Correct Folder Location
			shutil.move(path, f"./.cache/{mPKG['ID']}"); shutil.rmtree(f"./.cache/{i}");
			path = f"./.cache/{mPKG['ID']}";

			Files: File.Folder_Contents = File.List(path);
			for f in Files[0]:
				if (f not in mPKG["Data"][0] + [".adellian"]):
					shutil.rmtree(f"{path}/{f}");
			for f in Files[1]:
				if (f not in mPKG["Data"][1] + [".adellian"]):
					os.remove(f"{path}/{f}");



			Log.Awaited().OK(f"{round((Time.Get_Unix(True) - u_init) * 1000)}ms");

		except Exception as E:
			Log.Awaited().EXCEPTION(E, Traceback=False);
			NagisaPKGs["Error"].append(REPO);

		return NagisaPKGs;