import hashlib
import json
from sqlalchemy.orm import Session
from ..models import IdempotencyKey

def fingerprint(payload: dict) -> str:
    # Normalize to a stable string and hash
    stable = json.dumps(payload, sort_keys=True, separators=(',', ':'))
    return hashlib.sha256(stable.encode('utf-8')).hexdigest()

def get_cached_response(db: Session, key: str, payload: dict) -> dict | None:
    fp = fingerprint(payload)
    row = db.get(IdempotencyKey, key)
    if row and row.request_fingerprint == fp:
        return row.response_cache
    return None

def store_response(db: Session, key: str, payload: dict, response: dict) -> None:
    fp = fingerprint(payload)
    row = db.get(IdempotencyKey, key)
    if row is None:
        row = IdempotencyKey(key=key, request_fingerprint=fp, response_cache=response)
        db.add(row)
    else:
        row.request_fingerprint = fp
        row.response_cache = response
    db.commit()
