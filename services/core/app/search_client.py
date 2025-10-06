from typing import Any, Dict
import meilisearch
from .config import settings

_client = None

def get_client() -> meilisearch.Client:
    global _client
    if _client is None:
        _client = meilisearch.Client(settings.MEILI_HOST, settings.MEILI_MASTER_KEY)
    return _client

LEADS_INDEX = "crm_leads"
INV_INDEX = "acc_invoices"


def ensure_indexes():
    client = get_client()
    try:
        client.create_index(LEADS_INDEX, {"primaryKey": "id"})
    except Exception:
        pass
    try:
        client.create_index(INV_INDEX, {"primaryKey": "id"})
    except Exception:
        pass


def index_lead(obj: Dict[str, Any]):
    client = get_client()
    client.index(LEADS_INDEX).add_documents([obj])


def delete_lead(lead_id: int):
    client = get_client()
    client.index(LEADS_INDEX).delete_document(str(lead_id))


def index_invoice(obj: Dict[str, Any]):
    client = get_client()
    client.index(INV_INDEX).add_documents([obj])
