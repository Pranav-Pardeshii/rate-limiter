import time
from fastapi import FastAPI, HTTPException, Depends

app = FastAPI()


class TokenBucket:
    def __init__(self, capacity, refill_rate):
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.tokens = capacity
        self.last_refill = time.time()

    def _refill(self):
        elapsed = time.time() - self.last_refill
        tokens_earned = elapsed * self.refill_rate
        self.tokens = min(self.capacity, tokens_earned + self.tokens)
        self.last_refill = time.time()
    
    def consume(self, tokens = 1):
        self._refill()
        if self.tokens >= tokens:
            self.tokens = self.tokens - tokens
            return True
        return False
    
bucket = TokenBucket(capacity=5, refill_rate=1)
def rate_limit():
    allowed = bucket.consume()
    print(f"tokens left: {bucket.tokens:.2f}, allowed: {allowed}")
    if not allowed:
        raise HTTPException(status_code=429, detail="Too many requests!")

@app.get("/ping")
def ping(limit = Depends(rate_limit)):
    return {"message": "pong"}
    

if __name__ == "__main__":
    def test():
        bucket = TokenBucket(capacity=5, refill_rate=1)

        for i in range(5):
            result = bucket.consume()
            print(f"Request {i+1}: {'allowed' if result else 'BLOCKED'} (tokens left: {bucket.tokens:.2f})")

        print("--- waiting 3 seconds ---")
        time.sleep(3)

        for i in range(5, 9):
            result = bucket.consume()
            print(f"Request {i+1}: {'allowed' if result else 'BLOCKED'} (tokens left: {bucket.tokens:.2f})")

    test()
    