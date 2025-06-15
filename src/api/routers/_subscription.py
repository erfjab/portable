import asyncio
from fastapi import APIRouter, Request, HTTPException, Response
from aiohttp import ClientSession, ClientError
from src.clients import ClientManager
from ..dependencies import SubDep

router = APIRouter(prefix="/sub", tags=["Subscription"])


@router.get("/{key}")
async def subscription_info(request: Request, dbsub: SubDep):
    """Forward subscription requests to the appropriate endpoint."""
    user = await ClientManager.get_user(username=dbsub.key, server=dbsub.server)
    if not user or not user.get("subscription_url"):
        raise HTTPException(status_code=404)
    headers = dict(request.headers)
    headers.pop("host", None)
    params = dict(request.query_params)

    try:
        async with ClientSession() as session:
            async with session.request(
                method=request.method,
                url=user["subscription_url"],
                headers=headers,
                params=params,
                data=await request.body(),
                timeout=3.0,
                allow_redirects=True,
            ) as response:
                return Response(
                    content=await response.read(),
                    status_code=response.status,
                    headers=dict(response.headers),
                    media_type=response.headers.get("content-type", "text/plain"),
                )

    except asyncio.TimeoutError:
        raise HTTPException(status_code=504)
    except ClientError:
        raise HTTPException(status_code=502)
    except Exception:
        raise HTTPException(status_code=500)
