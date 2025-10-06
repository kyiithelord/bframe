from fastapi import APIRouter, Depends, UploadFile, File
from ..security import get_current_user
from ..rbac import require_permission
from ..storage_client import put_object

router = APIRouter(prefix="/files", tags=["files"]) 

@router.post("")
async def upload(file: UploadFile = File(...), user=Depends(get_current_user), perm=Depends(require_permission("files.write"))):
    data = await file.read()
    url = put_object(file.filename, data, len(data), content_type=file.content_type or "application/octet-stream")
    return {"name": file.filename, "url": url}
