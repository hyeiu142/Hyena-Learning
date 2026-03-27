import redis

r = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

print("Check redis connection...")

if r.ping():
    print("ping done, redis is ready")

r.flushdb()

print("TEST RAM CACHE")
r.set("direction", "Trương Gia Bình")
print("Save to RAM")

name = r.get("direction")
print(f"Get from RAM: {name}")

# set time to kill cache
r.setex("stock_price", 5, "102,000 VND")

print("\nSave stock price to RAM, will expire in 5 seconds")

