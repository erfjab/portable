import asyncio
from fastapi import APIRouter, Request, HTTPException, Response
from aiohttp import ClientSession, ClientError
from src.clients import ClientManager
from src.db import Subscription
from ..dependencies import SubDep, MarzneshinSubDep

router = APIRouter(prefix="/sub", tags=["Subscription"])


async def forward_subscription_request(request: Request, subscription: Subscription):
    user = await ClientManager.get_user(
        username=subscription.key, server=subscription.server
    )
    if not user or not user.subscription_url:
        raise HTTPException(status_code=404)

    headers = dict(request.headers)
    headers.pop("host", None)
    params = dict(request.query_params)

    try:
        async with ClientSession() as session:
            async with session.request(
                method=request.method,
                url=user.subscription_url,
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


@router.get("/{key}")
async def subscription_info(request: Request, dbsub: SubDep):
    """Forward subscription requests to the appropriate endpoint."""
    return await forward_subscription_request(request, dbsub)


@router.get("/{key}/{username}")
async def subscription_marzneshin_info(request: Request, dbsub: MarzneshinSubDep):
    """Forward subscription requests to the appropriate endpoint."""
    return await forward_subscription_request(request, dbsub)
