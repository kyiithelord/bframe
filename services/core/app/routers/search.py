from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from ..security import get_current_user, get_db
from ..rbac import require_permission
from ..search_client import get_client, ensure_indexes, LEADS_INDEX, INV_INDEX

router = APIRouter(prefix="/search", tags=["search"]) 

@router.get("")
def search(q: str = Query(..., min_length=1), user=Depends(get_current_user), perm=Depends(require_permission("search.read"))):
    ensure_indexes()
    client = get_client()
    results = []
    for idx, itype in [(LEADS_INDEX, "lead"), (INV_INDEX, "invoice")]:
        try:
            r = client.index(idx).search(q, {"limit": 5})
            for hit in r.get("hits", []):
                results.append({"type": itype, **hit})
        except Exception:
            pass
    return {"results": results}
