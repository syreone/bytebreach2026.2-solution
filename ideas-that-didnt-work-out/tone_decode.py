from itertools import product
import math

nums = [21, 44, 60, 85]

def a1z26(v):
    return chr(64 + v) if 1 <= v <= 26 else None

def mod26_alpha(v):
    return a1z26(v % 26 or 26)

def rot13(s):
    t = str.maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZ", "NOPQRSTUVWXYZABCDEFGHIJKLM")
    return s.translate(t)

def atbash_ch(c):
    if 'A' <= c <= 'Z':
        return chr(ord('Z') - (ord(c) - ord('A')))
    if 'a' <= c <= 'z':
        return chr(ord('z') - (ord(c) - ord('a')))
    return c

results = {}

# 1) direct A1Z26 (numbers up to 26 -> letters; else mod)
direct = "".join(mod26_alpha(v) for v in nums)
results["mod26 fwd"] = direct

# 2) reversed order
results["mod26 rev"] = "".join(mod26_alpha(v) for v in nums[::-1])

# 3) differences between consecutive, extended to first=21
diffs = [nums[0]]
for i in range(1, len(nums)):
    diffs.append(nums[i] - nums[i-1])
results["cumdiff fwd"] = "".join(mod26_alpha(d) for d in diffs)
results["cumdiff rev"] = "".join(mod26_alpha(d) for d in [nums[0]] + [nums[i]-nums[i-1] for i in range(1,4)][::-1])

# 4) differences only (second..last)
secdiff = [nums[i]-nums[i-1] for i in range(1,4)]
results["diffs only"] = "".join(mod26_alpha(d) for d in secdiff)

# 5) 93.75x21..85 -> actual Hz -> ratio to 1968.75 (tones themselves)
hz = [93.75*v for v in nums]
results["hz"] = ",".join(str(h) for h in hz)

# 6) binary/ascii concatenations
def try_ascii(nums):
    out = []
    for v in nums:
        if 27 <= v <= 126:
            out.append(chr(v))
        else:
            out.append("?")
    return "".join(out)
results["ascii direct"] = try_ascii(nums)

# 7) golden ratio / phi-like: 21*phi=33.9, ... skip; test products of pairs mod26
pairs = []
for a, b in [(nums[0], nums[1]), (nums[2], nums[3]), (nums[0], nums[3]), (nums[1], nums[2])]:
    pairs.append(a*b)
results["pair products mod26"] = "".join(mod26_alpha(p) for p in pairs)

# 8) sums mod26
results["pair sums mod26"] = "".join(mod26_alpha(nums[i]+nums[i+1]) for i in (0,2))

# 9) differences of pairs (abs) mod26
results["pair diffs"] = "".join(mod26_alpha(abs(nums[i]-nums[i+1])) for i in (0,2))

# 10) all pairwise sums mod26 c3
allpair = []
for i in range(len(nums)):
    for j in range(i+1, len(nums)):
        allpair.append(nums[i]+nums[j])
results["all pairwise sums mod26"] = "".join(mod26_alpha(p) for p in sorted(allpair))

# 11) numbers as positions in the 16-char station code (wrap) -> letters of code
code = "q4v7nk2xr9tb6mhd"
idx = [nums[i] % len(code) for i in range(4)]
results["station code by idx"] = "".join(code[i] for i in idx)

# 12) factors / divisors as letters
results["factors"] = ";".join(str([d for d in range(1, v+1) if v % d == 0]) for v in nums)

# 13) prime index
primes = []
n = 2
while len(primes) < 90:
    if all(n % p for p in primes):
        primes.append(n)
    n += 1
pth = [primes[v-1] % 26 for v in nums]
results["prime# mod26"] = "".join(mod26_alpha(p) for p in pth)

# 14) as digits combined: 21446085 and splits
results["21446085 digits mod26"] = "".join(mod26_alpha(int(d)) for d in "21446085")

print("=== direct pass ===")
for k, v in results.items():
    print("%-32s %s" % (k, v))
    if len(v) >= 3 and v.isalpha():
        print("   rot13:", rot13(v.upper()), " atbash:", "".join(atbash_ch(c) for c in v))

# 15) semitone offsets from a reference: MIDI-style note names for numbers 21,44,60,85
def note(v):
    names = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]
    n = names[v % 12]
    octv = v // 12 - 1
    return "%s%d" % (n, octv)
print("MIDI notes:", [note(v) for v in nums])