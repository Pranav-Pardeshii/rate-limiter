import time
from main import TokenBucket

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

if __name__ == '__main__':     
    test()