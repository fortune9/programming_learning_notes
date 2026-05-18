# Z-Algorithm Practice Problem Solutions

Solutions to practice problems from the Z-Algorithm tutorial.

---

## Easy Problems

### Solution 1: Basic Z-array Computation

**Problem:** Compute Z-array for `"aabxaayaab"`

**Solution:**

```python
from z_algorithm import z_algorithm, print_z_array

s = "aabxaayaab"
z = z_algorithm(s)
print_z_array(s, z)
```

**Output:**
```
Position:  0  1  2  3  4  5  6  7  8  9
String:    a  a  b  x  a  a  y  a  a  b
Z-array:   -  1  0  0  2  1  0  3  1  0
```

**Explanation:**
- Z[1]=1: "a" matches prefix
- Z[4]=2: "aa" matches prefix
- Z[7]=3: "aab" matches prefix

---

### Solution 2: Simple Pattern Search

**Problem:** Find "abc" in "xabcyabcz"

**Solution:**

```python
from z_algorithm import z_algorithm_search

text = "xabcyabcz"
pattern = "abc"
matches = z_algorithm_search(text, pattern)
print(f"Matches at positions: {matches}")
```

**Output:**
```
Matches at positions: [1, 5]
```

**Verification:**
- Position 1: "abc" ✓
- Position 5: "abc" ✓

---

## Medium Problems

### Solution 3: Shortest Repeating Substring

**Problem:** Find shortest substring appearing at least twice

**Approach:**
Look for the smallest Z[i] > 0, as it indicates a repeated prefix.

**Solution:**

```python
def shortest_repeating(s: str) -> int:
    z = z_algorithm(s)

    # Find minimum non-zero Z-value
    min_repeat = float('inf')
    for i in range(1, len(z)):
        if z[i] > 0:
            min_repeat = min(min_repeat, z[i])

    return min_repeat if min_repeat != float('inf') else -1

# Test
print(shortest_repeating("abcabcabc"))  # Output: 3 ("abc")
print(shortest_repeating("aab"))         # Output: 1 ("a")
```

**Complexity:** O(n)

---

### Solution 4: String Period Detection

**Problem:** Find shortest period or return -1

**Approach:**
Check if Z[i] + i = n for any i that divides n.

**Solution:**

```python
def find_period(s: str) -> int:
    n = len(s)
    z = z_algorithm(s)

    for i in range(1, n):
        if z[i] + i == n:
            # Found a potential period
            if n % i == 0:
                return i

    return -1  # Not periodic

# Test
print(find_period("abcabcabc"))  # Output: 3
print(find_period("abcabc"))     # Output: 3
print(find_period("abcdef"))     # Output: -1
```

**Explanation:**
- Z[i] + i = n means the prefix repeats from position i to end
- n % i == 0 ensures it repeats an integer number of times

---

## Hard Problems

### Solution 6: Longest Palindromic Substring

**Approach:**
For each potential center, use Z-algorithm to find palindrome length.

**Solution:**

```python
def longest_palindrome_z(s: str) -> str:
    n = len(s)
    if n == 0:
        return ""

    max_len = 1
    max_start = 0

    # Check odd-length palindromes (single center)
    for center in range(n):
        # Build: prefix + "#" + suffix_reversed
        left_part = s[:center+1][::-1]  # Reversed prefix including center
        right_part = s[center:]          # Suffix from center

        combined = right_part + "#" + left_part
        z = z_algorithm(combined)

        # Find maximum palindrome around this center
        for i in range(len(right_part) + 1, len(combined)):
            palindrome_len = 2 * z[i] - 1
            if palindrome_len > max_len:
                max_len = palindrome_len
                max_start = center - z[i] + 1

    return s[max_start:max_start + max_len]

# Test
print(longest_palindrome_z("abaxabaxabb"))  # Output: "baxabaxab"
```

**Note:** This is complex. Manacher's algorithm is simpler for palindromes.

---

*For additional problems or clarifications, refer to the main tutorial.*
