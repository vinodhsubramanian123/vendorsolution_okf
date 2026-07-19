import threading
from ikp_platform.api import get_repo

results = []


def thread_func():
    try:
        repo = get_repo()
        results.append(id(repo))
    except Exception as e:
        results.append(e)


threads = []
for _ in range(20):
    t = threading.Thread(target=thread_func)
    threads.append(t)

for t in threads:
    t.start()
for t in threads:
    t.join()

unique_ids = set(r for r in results if isinstance(r, int))
exceptions = [r for r in results if isinstance(r, Exception)]

print(f"Total threads: {len(results)}")
print(f"Unique instances: {len(unique_ids)}")
if exceptions:
    print("Exceptions occurred:", exceptions)
    exit(1)
if len(unique_ids) > 1:
    print("FAILED: Multiple RepoManager instances created! Cache not thread-safe.")
    exit(1)
elif len(unique_ids) == 1:
    print("SUCCESS: Only one instance created.")
else:
    print("FAILED: No instances created.")
    exit(1)
