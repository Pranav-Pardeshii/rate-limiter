# Token Bucket Rate Limiter

A rate limiter built from scratch using the token bucket algorithm, wrapped as a FastAPI dependency.

## How it works

A bucket holds a max number of tokens (e.g. 5). Each request costs 1 token and refills happen continuously at a fixed rate (e.g. 1/sec). Empty bucket → request blocked with a 429. Tokens regenerate over time, capped at max capacity — so idle time is rewarded, but bursts can't pile up indefinitely.

## Run it

```
uv sync
uv run uvicorn main:app --reload
```

Hit the endpoint a few times fast:
```
curl http://127.0.0.1:8000/ping
```
First few succeed, then you'll get `429 Too Many Requests` until the bucket refills.

## Test it

```
python test_bucket.py
```
Verifies blocking at capacity and refill behavior over time — no server needed.

## Next steps

- Per-user buckets (keyed by JWT user ID) instead of one global bucket
- Configurable capacity/refill rate per endpoint or user tier