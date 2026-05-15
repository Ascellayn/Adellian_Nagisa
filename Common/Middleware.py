from .Globals import *;
import traceback;



async def Exception_Handler(R: fastapi.Request, Next: Callable[[Any], Any]) -> Any:
	""" Because we use the TSNA Awaited System, we might as well do our logging here.
	This Middleware should be the first one to run anyways so it's a pretty safe bet to run our logging here."""

	Log.Stateless(f"{R.client.host}:{R.client.port} → [{R.method}] {R.url}..."); # pyright: ignore[reportOptionalMemberAccess] | I don't think in this context it's possible for R.client to be None
	try:
		buffer = await Next(R);
		Log.Awaited().OK();
		return buffer;
	except (Not_Found, Unauthorized, Bad_Request) as e:
		Log.Awaited().EXCEPTION(e);

		match e:
			case Not_Found(): code: int = 404;
			case Unauthorized(): code: int = 404;
			case Bad_Request(): code: int = 400;

		return fastapi.responses.JSONResponse({
			"Error": True,
			"Debug": App.Public["Debug"],
			"Message": str(e)
		}, status_code=code);

	except Exception as E:
		Log.Awaited().EXCEPTION(E);
		return fastapi.responses.JSONResponse({
			"Error": True,
			"Debug": App.Public["Debug"],
			"Message": f"{str(E)}\nEXCEPTION TRACE BACK:\n{'\n'.join(traceback.format_exception(E))}" if (App.Public["Debug"]) else str(E)
		}, status_code=500);
