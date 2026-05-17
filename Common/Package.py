from .Globals import *;
import httpx;
import io, os, shutil, zipfile;
import multiprocessing;

from . import Mika;



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
		File.JSON_Write(f"Nagisa.cache", Packages_Cached, True);
		return NagisaPKGs;





	@staticmethod
	async def Cache() -> Type.Nagisa_Packages:
		NagisaPKGs: Type.Nagisa_Packages = {
			"Last_Update": 0,
			"Error": [],
			"Packages": []
		};
		shutil.rmtree("./.cache/");
		with multiprocessing.Pool() as P:
			RESULTS: list[Type.Nagisa_Packages] = P.map(Acquire.Download, [x for x in enumerate(REPOSITORIES, start=1)]);
		for r in RESULTS:
			NagisaPKGs["Error"] += r["Error"];
			NagisaPKGs["Packages"] += r["Packages"];

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
			A.extractall(f".cache/{i}/"); del A;
			path: str = f".cache/{i}/{File.List(f'.cache/{i}/')[0][0]}";


			# Find MikaPackages
				# Delete if invalid
			if (not File.Exists(f"{path}/.adellian/")):
				shutil.rmtree(f".cache/{i}/");
				raise Exception(f"{REPO}: .adellian not found!");

			mPKGs: list[str] = [];
			for f in File.List(f"{path}/.adellian/")[1]:
				if (f.endswith(".mpkg")):
					mPKGs.append(f"{path}/.adellian/{f}");
			if (len(mPKGs) == 0): raise Exception(f"{REPO}: No MikaPackage found!");


			# Read Mika Packages and initiate MikaArchive compilations
			for mpkg in mPKGs:
				mPKG: Type.MikaRoll_Header = cast(Type.MikaRoll_Header, File.JSON_Read(mpkg));
				for opt in mPKG["Options"]:
					Mika.Roll(path, f".cache/{mPKG['ID']}¤{opt['Name']}.MikaRoll", mpkg.split("/")[-1], opt["Name"]);
				NagisaPKGs["Packages"].append(mPKG);

			# Cleanup
			shutil.rmtree(f".cache/{i}/");

			Log.Awaited().OK(f"{round((Time.Get_Unix(True) - u_init) * 1000)}ms");

		except Exception as E:
			Log.Awaited().EXCEPTION(E, Traceback=False);
			NagisaPKGs["Error"].append(REPO);

		return NagisaPKGs;