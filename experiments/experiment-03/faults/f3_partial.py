import os
os.makedirs("/tmp/exp03-state", exist_ok=True)
for i in range(3):
    open(f"/tmp/exp03-state/step{i}.txt", "w").write(f"step {i} done\n")
open("/tmp/exp03-state/step3.txt", "w").write("boom\n")   # fails mid-way leaving partial state
