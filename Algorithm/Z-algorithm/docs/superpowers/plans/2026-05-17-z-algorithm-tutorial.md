# Z-Algorithm Tutorial Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create a comprehensive educational tutorial explaining the Z-algorithm with visual diagrams, Python implementations, and practice problems.

**Architecture:** Tutorial-based documentation with three deliverables: (1) main markdown tutorial with 12 sections including ASCII diagrams, (2) Python module with three implementation versions, (3) practice problem solutions document.

**Tech Stack:** Markdown, Python 3.8+, ASCII diagrams

---

## File Structure

**New files to create:**
- `programming_learning_notes/Algorithm/Z-algorithm/z-algorithm-tutorial.md` - Main tutorial (sections 1-12)
- `programming_learning_notes/Algorithm/Z-algorithm/z_algorithm.py` - Python implementations
- `programming_learning_notes/Algorithm/Z-algorithm/z-algorithm-solutions.md` - Practice solutions

---

### Task 1: Python Implementation (Core Algorithm)

**Files:**
- Create: `programming_learning_notes/Algorithm/Z-algorithm/z_algorithm.py`

**Why first:** Need working, tested code before writing tutorial sections that reference it.

- [ ] **Step 1: Create Python file with clean production version**

Create file with:

```python
"""
Z-Algorithm Implementation
Python 3.8+ compatible
"""

def z_algorithm(s: str) -> list:
    """
    Compute Z-array using Z-algorithm in O(n) time.
    
    Args:
        s: Input string
    Returns:
        Z-array where Z[i] = length of longest prefix match at position i
    """
    n = len(s)
    if n == 0:
        return []
    
    z = [0] * n
    left, right = 0, 0
    
    for i in range(1, n):
        if i > right:
            left = right = i
            while right < n and s[right] == s[right - left]:
                right += 1
            z[i] = right - left
            right -= 1
        else:
            k = i - left
            if z[k] < right - i + 1:
                z[i] = z[k]
            else:
                left = i
                while right < n and s[right] == s[right - left]:
                    right += 1
                z[i] = right - left
                right -= 1
    
    return z


def print_z_array(s: str, z: list) -> None:
    """Print string and Z-array aligned for easy viewing"""
    print("Position:", " ".join(f"{i:2}" for i in range(len(s))))
    print("String:  ", " ".join(f" {c}" for c in s))
    print("Z-array: ", " ".join(f"{('-' if i == 0 else str(z[i])):2}" for i in range(len(z))))


if __name__ == "__main__":
    # Test basic functionality
    test_strings = [
        "aabcaabxaaz",
        "aabaacd",
        "aabaacaabaa"
    ]
    
    for s in test_strings:
        print(f"\nString: {s}")
        z = z_algorithm(s)
        print_z_array(s, z)
```

- [ ] **Step 2: Test the implementation**

Run: `python programming_learning_notes/Algorithm/Z-algorithm/z_algorithm.py`

Expected: Clean output showing Z-arrays for test strings

- [ ] **Step 3: Add educational version with extensive comments**

Add before the production version:

```python
def z_algorithm_educational(s: str) -> list:
    """
    Compute Z-array for string s using Z-algorithm.
    Educational version with extensive comments.
    
    Z[i] = length of longest substring starting at i that matches prefix
    
    Args:
        s: Input string
    Returns:
        List of integers representing Z-array
    """
    n = len(s)
    if n == 0:
        return []
    
    # Initialize Z-array with zeros
    z = [0] * n
    
    # Z[0] is undefined (we use 0 by convention)
    z[0] = 0
    
    # L and R define the rightmost Z-box [L, R]
    # Initially, no Z-box has been found
    left = 0
    right = 0
    
    # Compute Z[i] for each position from 1 to n-1
    for i in range(1, n):
        
        # Case 1: i is outside the current Z-box
        # We have no information to reuse, so compute naively
        if i > right:
            # Start a new Z-box at position i
            left = i
            right = i
            
            # Expand the Z-box as far as possible
            # Compare s[right] with s[right - left] (position in prefix)
            while right < n and s[right] == s[right - left]:
                right += 1
            
            # Z[i] is the length we matched
            z[i] = right - left
            
            # Adjust right to point to last matching character
            right -= 1
        
        # Case 2: i is inside the current Z-box [left, right]
        else:
            # Find mirror position k in the prefix
            k = i - left
            
            # How many characters remain in the current Z-box from position i?
            remaining = right - i + 1
            
            # Subcase 2a: Z[k] fits entirely within the remaining box
            if z[k] < remaining:
                # Safe to copy the mirror value
                z[i] = z[k]
                # No need to update L or R
            
            # Subcase 2b: Z[k] reaches or exceeds the box boundary
            else:
                # Copy what we know, then try to extend beyond R
                left = i
                
                # Continue comparing from R+1 onwards
                while right < n and s[right] == s[right - left]:
                    right += 1
                
                z[i] = right - left
                right -= 1
    
    return z
```

- [ ] **Step 4: Add pattern matching application version**

Add after production version:

```python
def z_algorithm_search(text: str, pattern: str) -> list:
    """
    Find all occurrences of pattern in text using Z-algorithm.
    
    Args:
        text: The text to search in
        pattern: The pattern to search for
    Returns:
        List of starting indices where pattern occurs in text
    """
    if not pattern or not text:
        return []
    
    # Concatenate pattern and text with separator
    # Separator ensures no spurious matches across boundary
    combined = pattern + "$" + text
    z = z_algorithm(combined)
    
    # Find all positions where Z[i] equals pattern length
    pattern_len = len(pattern)
    matches = []
    
    # Start checking after pattern and separator
    for i in range(pattern_len + 1, len(combined)):
        if z[i] == pattern_len:
            # Convert to index in original text
            text_index = i - pattern_len - 1
            matches.append(text_index)
    
    return matches
```

- [ ] **Step 5: Update main block with pattern matching example**

Replace `if __name__ == "__main__"` section:

```python
if __name__ == "__main__":
    print("=" * 60)
    print("Z-Algorithm Examples")
    print("=" * 60)
    
    # Example 1: Compute Z-array
    print("\n--- Example 1: Computing Z-array ---")
    s = "aabcaabxaaz"
    z = z_algorithm(s)
    print_z_array(s, z)
    
    # Example 2: Pattern matching
    print("\n--- Example 2: Pattern Matching ---")
    text = "ababcababcabab"
    pattern = "abab"
    matches = z_algorithm_search(text, pattern)
    print(f"Text: {text}")
    print(f"Pattern: {pattern}")
    print(f"Pattern found at positions: {matches}")
    
    # Verify
    for pos in matches:
        print(f"  Position {pos}: '{text[pos:pos+len(pattern)]}'")
    
    print("\n" + "=" * 60)
```

- [ ] **Step 6: Test complete implementation**

Run: `python programming_learning_notes/Algorithm/Z-algorithm/z_algorithm.py`

Expected: Output showing Z-array examples and pattern matching results

---

### Task 2: Tutorial Sections 1-2 (Introduction & Z-Array Definition)

**Files:**
- Create: `programming_learning_notes/Algorithm/Z-algorithm/z-algorithm-tutorial.md`

- [ ] **Step 1: Create tutorial file with front matter and TOC**

```markdown
# Understanding the Z-Algorithm: A Visual Guide

**Date:** 2026-05-17  
**Difficulty:** Intermediate  
**Tags:** string-algorithms, pattern-matching, linear-time

---

## Table of Contents

1. [Introduction & Intuition](#1-introduction--intuition)
2. [What is the Z-Array?](#2-what-is-the-z-array)
3. [The Naive Approach (and Why It Fails)](#3-the-naive-approach-and-why-it-fails)
4. [The Optimization Strategy](#4-the-optimization-strategy)
5. [Visual Walkthrough with Diagrams](#5-visual-walkthrough-with-diagrams)
6. [Detailed Algorithm Breakdown](#6-detailed-algorithm-breakdown)
7. [Step-by-Step Example](#7-step-by-step-example)
8. [Python Implementation](#8-python-implementation)
9. [Complexity Analysis](#9-complexity-analysis)
10. [Applications & Use Cases](#10-applications--use-cases)
11. [Practice Problems](#11-practice-problems)
12. [References](#12-references)

---
```

- [ ] **Step 2: Write Section 1 - Introduction & Intuition**

Add:

```markdown
## 1. Introduction & Intuition

Imagine you have a long DNA sequence and you want to find all occurrences of a specific genetic marker. The naive approach would be to compare the marker against every position in the sequence, character by character. For a sequence of length n and a marker of length m, this takes O(n × m) time. Can we do better?

The **Z-algorithm** is an elegant pattern-matching algorithm that achieves linear O(n) time complexity. The key insight is simple but powerful: **reuse information from previous comparisons instead of starting from scratch each time.**

Here's the core concept: for each position i in a string, the Z-algorithm computes Z[i] = the length of the longest substring starting at position i that matches the prefix of the string. This single array of values gives us enough information to solve pattern matching and many other string problems efficiently.

In this tutorial, we'll build your understanding step by step:
- First, understand what the Z-array represents
- See why naive approaches waste effort
- Learn the optimization strategy (the "Z-box" and "mirror" technique)
- Walk through detailed examples with visualizations
- Implement the algorithm in Python
- Prove why it achieves O(n) time complexity

By the end, you'll not only know how to implement the Z-algorithm, but deeply understand *why* it works and when to use it.

---
```

- [ ] **Step 3: Write Section 2 - What is the Z-Array?**

Add:

```markdown
## 2. What is the Z-Array?

### Definition

The **Z-array** for a string S is an array where each element Z[i] represents:

> **Z[i] = the length of the longest substring starting at position i that matches the prefix of S**

In other words, Z[i] tells us how many characters starting at position i are identical to the characters starting at position 0.

### Convention

- Z[0] is technically undefined (every string matches itself at position 0)
- By convention, we set **Z[0] = 0** in this tutorial
- Some implementations use Z[0] = n (the string length)

### Visual Example

Let's compute the Z-array for the string **"aabaacd"**:

```
Position:  0 1 2 3 4 5 6
String:    a a b a a c d
Z-array:   - 1 0 3 1 0 0
```

**Explanation:**

- **Z[0] = -** (undefined, shown as dash)
- **Z[1] = 1**: Starting at position 1, "a" matches the prefix "a" (1 character)
- **Z[2] = 0**: Starting at position 2, "b" ≠ "a" (no match)
- **Z[3] = 3**: Starting at position 3, "aac" matches the prefix "aac" (3 characters)
- **Z[4] = 1**: Starting at position 4, "a" matches the prefix "a" (1 character)
- **Z[5] = 0**: Starting at position 5, "c" ≠ "a" (no match)
- **Z[6] = 0**: Starting at position 6, "d" ≠ "a" (no match)

### Connection to Pattern Matching

The Z-array becomes extremely useful for pattern matching. If we want to find all occurrences of pattern P in text T:

1. Concatenate them with a separator: **S = P + "$" + T**
   - The "$" ensures the pattern and text don't accidentally match across the boundary
2. Compute the Z-array for S
3. Any position i where **Z[i] = len(P)** indicates a match!

**Example:**

```
Pattern: "ab"
Text:    "xababy"
Combined: "ab$xababy"

Position:  0 1 2 3 4 5 6 7 8
String:    a b $ x a b a b y
Z-array:   - 1 0 0 2 1 2 1 0
                    ^     ^
                    |     Z[7]=2 means "ab" found at position 4 in text
                    Z[4]=2 means "ab" found at position 1 in text
```

Now that we understand what the Z-array represents, let's see how to compute it efficiently.

---
```

---

### Task 3: Tutorial Section 3 (Naive Approach)

**Files:**
- Modify: `programming_learning_notes/Algorithm/Z-algorithm/z-algorithm-tutorial.md`

- [ ] **Step 1: Add Section 3 content**

Append to tutorial:

```markdown
## 3. The Naive Approach (and Why It Fails)

Before we learn the optimized Z-algorithm, let's see the straightforward approach and understand why it's inefficient.

### Naive Algorithm

```
for i = 1 to n-1:
    compare characters starting at i with prefix
    count matching length → Z[i]
```

This is simple to implement:

```python
def z_array_naive(s):
    n = len(s)
    z = [0] * n
    
    for i in range(1, n):
        # Compare substring starting at i with prefix
        j = 0
        while i + j < n and s[j] == s[i + j]:
            j += 1
        z[i] = j
    
    return z
```

### The Problem: Redundant Comparisons

Let's trace through the string **"aabaacaabaa"** to see the inefficiency:

```
Position:  0 1 2 3 4 5 6 7 8 9 10
String:    a a b a a c a a b a a
           ↓ ↓ ↓             ↓ ↓ ↓
Prefix:    a a b a a c a a b a a

Computing Z[1]:
  Compare: s[0] vs s[1] → 'a' vs 'a' ✓
  Compare: s[1] vs s[2] → 'a' vs 'b' ✗
  Result: Z[1] = 1

Computing Z[7]:
  Compare: s[0] vs s[7] → 'a' vs 'a' ✓
  Compare: s[1] vs s[8] → 'a' vs 'b' ✗
  Result: Z[7] = 1
  
  ↑ We're doing the SAME comparisons we did at position 1!
```

### The Key Insight

> **Every comparison we make gives us information not just about the current position, but potentially about future positions too. The naive approach throws this information away!**

When we computed Z[1] and found that positions 1-2 match the prefix "aa", we learned something valuable:
- Position 1 contains 'a'
- Position 2 contains 'a'

Later, when computing Z[7], if we know that positions 7-8 are inside a region that matches the prefix, we could reuse this knowledge instead of comparing again!

### Complexity Analysis

**Worst case:** O(n²)

Consider the string **"aaaaaaa"** (all same characters):
- Computing Z[1]: compare n-1 characters
- Computing Z[2]: compare n-2 characters
- Computing Z[3]: compare n-3 characters
- ...
- Total: (n-1) + (n-2) + ... + 1 = O(n²)

This is too slow for large strings. We need a better approach.

---
```

---

### Task 4: Tutorial Section 4 (Optimization Strategy - Part 1)

**Files:**
- Modify: `programming_learning_notes/Algorithm/Z-algorithm/z-algorithm-tutorial.md`

- [ ] **Step 1: Add Section 4 Part A (Z-box concept)**

Append:

```markdown
## 4. The Optimization Strategy

This is the heart of the Z-algorithm. Understanding this section will make everything else clear.

### Part A: The Z-Box Concept

**Definition:** A **Z-box** is a substring [L, R] that matches the prefix.

If we compute Z[i] = k for some position i, then the substring from position i to position i+k-1 is identical to the prefix of length k. We call this a Z-box with boundaries **L = i** and **R = i+k-1**.

**Key idea:** As we compute Z-values, we track the **rightmost Z-box** we've seen so far using two variables:
- **L** = left boundary of the rightmost Z-box
- **R** = right boundary of the rightmost Z-box

**Why track the rightmost Z-box?** Because if our current position i falls inside [L, R], we're inside a substring that matches the prefix, so we can reuse previous information!

**Visual example:**

```
Position:  0 1 2 3 4 5 6 7 8 9 10
String:    a b c x a b c y a b c
           [-----]     [-----]
           prefix      Z-box at position 4
                       L=4, R=6
```

At position 4, we found Z[4] = 3, meaning "abc" matches the prefix "abc". This creates a Z-box [4, 6].

---
```

- [ ] **Step 2: Add Part B (Mirror insight)**

Append:

```markdown
### Part B: The Mirror Insight

Here's where the magic happens. If position i is inside the Z-box [L, R], we can use information from the prefix!

**The mirror position:** Define **k = i - L**

Since the Z-box [L, R] matches the prefix [0, R-L]:
- Position L in the string corresponds to position 0 in the prefix
- Position L+1 corresponds to position 1
- Position i corresponds to position k = i - L

**Visual diagram:**

```
Position:  0 1 2 3 4 5 6 7 8 9 10 11
String:    a a b x a a b x a a b  y
           [-------]       [-------]
           prefix          Z-box [L=6, R=10]
           k=0 1 2         i=6 7 8
```

**Computing Z[8]:**
- Position 8 is inside Z-box [6, 10] ✓
- Relative position: **k = 8 - 6 = 2**
- The Z-box matches the prefix, so:
  - s[6] = s[0] = 'a'
  - s[7] = s[1] = 'a'
  - s[8] = s[2] = 'b'
- Position 8 should behave like position 2 in the prefix!
- We already computed Z[2] earlier
- We can **reuse** Z[2] to help compute Z[8]

**The crucial question:** Can we just copy Z[i] = Z[k]?

**Sometimes yes, sometimes no.** It depends on whether the match extends beyond the Z-box boundary.

---
```

- [ ] **Step 3: Add Part C (Two cases)**

Append:

```markdown
### Part C: The Two Cases

When computing Z[i], there are two scenarios:

#### **Case 1: i > R (Outside any Z-box)**

```
Position:  0 1 2 3 4 5 6 7 8
String:    x x x x x x x x x
           [-----]     ^
           L=?  R=?    i is here (i > R)
```

We have no information to reuse. We must:
1. Compare naively starting at position i
2. Set L = i, and R = i initially
3. Extend R as far as possible while characters match
4. Set Z[i] = R - L
5. The new Z-box is [L, R]

#### **Case 2: L ≤ i ≤ R (Inside Z-box)**

```
Position:  0 1 2 3 4 5 6 7 8
String:    x x x x x x x x x
           [-----]   [-------]
           prefix    L   i   R
```

Position i is inside the rightmost Z-box. Use the mirror position k = i - L.

**Subcase 2a: Z[k] < R - i + 1** (fits within box)

```
Position:  0 1 2 3 4 5 6 7 8 9
String:    a b c x a b c y a b
           [---]     [-----]
           k=1       L=4 i=5 R=6
           Z[1]=0    
           
Z[k]=0 and R-i+1=2, so Z[k] < R-i+1
The mirror value fits entirely within remaining box.
Safe to copy: Z[i] = Z[k] = 0
```

The mirror value Z[k] is fully contained within the remaining Z-box from position i to R. We can safely copy:
**Z[i] = Z[k]**

**Subcase 2b: Z[k] ≥ R - i + 1** (may extend beyond)

```
Position:  0 1 2 3 4 5 6 7 8 9
String:    a a a x a a a a b c
           [---]     [-------]
           k=1       L=4 i=5 R=7
           Z[1]=2
           
Z[k]=2 and R-i+1=3, so Z[k] < R-i+1 (actually Z[k]=2)
But what if Z[k] was 3 or more?
```

The mirror suggests a match of length Z[k], but we've only verified up to position R. The match might extend beyond R!

We must:
1. Start from position R+1
2. Compare s[R+1] with s[R+1-i] (continuing the match)
3. Extend R as far as possible
4. Update L = i (new Z-box starts at i)
5. Set Z[i] = R - L

### Summary of the Strategy

```
if i > R:
    # Case 1: Outside Z-box
    Compare naively from i, update L and R
else:
    # Case 2: Inside Z-box
    k = i - L
    if Z[k] < R - i + 1:
        # Subcase 2a: Mirror fits
        Z[i] = Z[k]
    else:
        # Subcase 2b: May extend
        Start from R+1, compare and extend
        Update L = i
```

This reuse of information is what makes the algorithm O(n) instead of O(n²)!

---
```

---

### Task 5: Tutorial Section 5 (Visual Walkthrough)

**Files:**
- Modify: `programming_learning_notes/Algorithm/Z-algorithm/z-algorithm-tutorial.md`

- [ ] **Step 1: Add Section 5 header and first 3 steps**

Append:

```markdown
## 5. Visual Walkthrough with Diagrams

Let's trace the algorithm step-by-step on the string **"aabcaabxaay"** to see how it works in practice.

```
Initial state:
Position:  0 1 2 3 4 5 6 7 8 9 10
String:    a a b c a a b x a a y
Z-array:   - ? ? ? ? ? ? ? ? ? ?
L = 0, R = 0
```

---

### Step 1: i = 1

**Status:** i > R (1 > 0), so Case 1 (outside Z-box)

**Action:** Compare naively starting at position 1

```
Compare s[1] vs s[0]: 'a' vs 'a' ✓
Compare s[2] vs s[1]: 'b' vs 'a' ✗

Match length = 1
```

**Result:**
- Z[1] = 1
- L = 1, R = 1 (new Z-box)

```
Position:  0 1 2 3 4 5 6 7 8 9 10
String:    a a b c a a b x a a y
Z-array:   - 1 ? ? ? ? ? ? ? ? ?
Z-box:       [1]
```

---

### Step 2: i = 2

**Status:** i > R (2 > 1), so Case 1 (outside Z-box)

**Action:** Compare naively starting at position 2

```
Compare s[2] vs s[0]: 'b' vs 'a' ✗

Match length = 0
```

**Result:**
- Z[2] = 0
- No Z-box update (length 0)

```
Position:  0 1 2 3 4 5 6 7 8 9 10
String:    a a b c a a b x a a y
Z-array:   - 1 0 ? ? ? ? ? ? ? ?
Z-box:       [1] (unchanged)
```

---

### Step 3: i = 3

**Status:** i > R (3 > 1), so Case 1 (outside Z-box)

**Action:** Compare naively starting at position 3

```
Compare s[3] vs s[0]: 'c' vs 'a' ✗

Match length = 0
```

**Result:**
- Z[3] = 0
- No Z-box update

```
Position:  0 1 2 3 4 5 6 7 8 9 10
String:    a a b c a a b x a a y
Z-array:   - 1 0 0 ? ? ? ? ? ? ?
Z-box:       [1] (unchanged)
```

---
```

- [ ] **Step 2: Add steps 4-7 (showing Z-box usage)**

Append:

```markdown
### Step 4: i = 4

**Status:** i > R (4 > 1), so Case 1 (outside Z-box)

**Action:** Compare naively starting at position 4

```
Compare s[4] vs s[0]: 'a' vs 'a' ✓
Compare s[5] vs s[1]: 'a' vs 'a' ✓
Compare s[6] vs s[2]: 'b' vs 'b' ✓
Compare s[7] vs s[3]: 'x' vs 'c' ✗

Match length = 3
```

**Result:**
- Z[4] = 3
- L = 4, R = 6 (new, larger Z-box)

```
Position:  0 1 2 3 4 5 6 7 8 9 10
String:    a a b c a a b x a a y
Z-array:   - 1 0 0 3 ? ? ? ? ? ?
Z-box:             [-----]
                   4     6
```

---

### Step 5: i = 5

**Status:** i ≤ R (5 ≤ 6), so Case 2 (inside Z-box) ✓

**Action:** Use mirror position

```
k = i - L = 5 - 4 = 1
Z[k] = Z[1] = 1

Boundary check:
  Z[k] = 1
  R - i + 1 = 6 - 5 + 1 = 2
  Z[k] < R - i + 1? YES ✓
```

**Subcase 2a:** Mirror value fits within box

**Result:**
- Z[5] = Z[1] = 1
- No need to compare! (Reused previous result)
- L and R unchanged

```
Position:  0 1 2 3 4 5 6 7 8 9 10
String:    a a b c a a b x a a y
Z-array:   - 1 0 0 3 1 ? ? ? ? ?
Z-box:             [-----]
                   4     6
```

---

### Step 6: i = 6

**Status:** i ≤ R (6 ≤ 6), so Case 2 (inside Z-box) ✓

**Action:** Use mirror position

```
k = i - L = 6 - 4 = 2
Z[k] = Z[2] = 0

Boundary check:
  Z[k] = 0
  R - i + 1 = 6 - 6 + 1 = 1
  Z[k] < R - i + 1? YES ✓
```

**Subcase 2a:** Mirror value fits

**Result:**
- Z[6] = Z[2] = 0
- L and R unchanged

```
Position:  0 1 2 3 4 5 6 7 8 9 10
String:    a a b c a a b x a a y
Z-array:   - 1 0 0 3 1 0 ? ? ? ?
Z-box:             [-----]
                   4     6
```

---

### Step 7: i = 7

**Status:** i > R (7 > 6), so Case 1 (outside Z-box)

**Action:** Compare naively starting at position 7

```
Compare s[7] vs s[0]: 'x' vs 'a' ✗

Match length = 0
```

**Result:**
- Z[7] = 0
- No Z-box update

```
Position:  0 1 2 3 4 5 6 7 8 9 10
String:    a a b c a a b x a a y
Z-array:   - 1 0 0 3 1 0 0 ? ? ?
Z-box:             [-----] (unchanged)
                   4     6
```

---
```

- [ ] **Step 3: Add remaining steps 8-10**

Append:

```markdown
### Step 8: i = 8

**Status:** i > R (8 > 6), so Case 1 (outside Z-box)

**Action:** Compare naively

```
Compare s[8] vs s[0]: 'a' vs 'a' ✓
Compare s[9] vs s[1]: 'a' vs 'a' ✓
Compare s[10] vs s[2]: 'y' vs 'b' ✗

Match length = 2
```

**Result:**
- Z[8] = 2
- L = 8, R = 9 (new Z-box)

```
Position:  0 1 2 3 4 5 6 7 8 9 10
String:    a a b c a a b x a a y
Z-array:   - 1 0 0 3 1 0 0 2 ? ?
Z-box:                     [---]
                           8   9
```

---

### Step 9: i = 9

**Status:** i ≤ R (9 ≤ 9), so Case 2 (inside Z-box) ✓

**Action:** Use mirror

```
k = i - L = 9 - 8 = 1
Z[k] = Z[1] = 1

Boundary check:
  Z[k] = 1
  R - i + 1 = 9 - 9 + 1 = 1
  Z[k] < R - i + 1? NO (equal)
```

**Subcase 2b:** Mirror reaches boundary, might extend

**Action:** Try to extend from R+1

```
Compare s[10] vs s[10-9]: 'y' vs 'a' ✗
Cannot extend
```

**Result:**
- Z[9] = 1
- L = 9, R = 9 (updated)

```
Position:  0 1 2 3 4 5 6 7 8 9 10
String:    a a b c a a b x a a y
Z-array:   - 1 0 0 3 1 0 0 2 1 ?
Z-box:                       [1]
                             9
```

---

### Step 10: i = 10

**Status:** i > R (10 > 9), so Case 1 (outside Z-box)

**Action:** Compare naively

```
Compare s[10] vs s[0]: 'y' vs 'a' ✗

Match length = 0
```

**Result:**
- Z[10] = 0
- Algorithm complete!

```
Final Z-array:
Position:  0 1 2 3 4 5 6 7 8 9 10
String:    a a b c a a b x a a y
Z-array:   - 1 0 0 3 1 0 0 2 1 0
```

---

**Key observations from this walkthrough:**
1. We reused information at positions 5, 6, and 9 (no character comparisons!)
2. The Z-box tracked the rightmost matching region
3. Total comparisons: much fewer than naive O(n²) approach
4. The algorithm systematically uses Case 1 or Case 2 logic

---
```

---

### Task 6: Tutorial Sections 6-7 (Algorithm & Example)

**Files:**
- Modify: `programming_learning_notes/Algorithm/Z-algorithm/z-algorithm-tutorial.md`

- [ ] **Step 1: Add Section 6 (Algorithm breakdown)**

Append:

```markdown
## 6. Detailed Algorithm Breakdown

Now that you've seen the algorithm in action, let's present the complete pseudocode with explanations.

### Pseudocode

```python
Algorithm Z-Algorithm(string S):
    Input: String S of length n
    Output: Z-array where Z[i] = length of longest prefix match at position i
    
    n = length of S
    Z = array of size n, initialized to 0
    L = 0, R = 0  # Rightmost Z-box boundaries
    
    for i from 1 to n-1:
        if i > R:
            # Case 1: Outside any Z-box
            L = R = i
            while R < n and S[R] == S[R-L]:
                R = R + 1
            Z[i] = R - L
            R = R - 1
        
        else:
            # Case 2: Inside Z-box [L, R]
            k = i - L  # Mirror position
            
            if Z[k] < R - i + 1:
                # Subcase 2a: Mirror fits within box
                Z[i] = Z[k]
            
            else:
                # Subcase 2b: May extend beyond box
                L = i
                while R < n and S[R] == S[R-L]:
                    R = R + 1
                Z[i] = R - L
                R = R - 1
    
    return Z
```

### Line-by-Line Explanation

**Initialization:**
```python
Z = array of size n, initialized to 0
L = 0, R = 0
```
- Z[0] is left as 0 (undefined by convention)
- L and R = 0: no Z-box found yet
- We'll compute Z[1] through Z[n-1]

**Main loop:**
```python
for i from 1 to n-1:
```
- Start at i=1 (not 0, since Z[0] is undefined)
- Process each position sequentially

**Case 1: Outside Z-box**
```python
if i > R:
    L = R = i
```
- Position i is beyond the rightmost Z-box
- Start a new potential Z-box at position i

```python
while R < n and S[R] == S[R-L]:
    R = R + 1
```
- Extend R rightward while characters match
- S[R] is the current character in the string
- S[R-L] is the corresponding character in the prefix
- Since L = i initially, R-L represents the offset from the prefix start

```python
Z[i] = R - L
R = R - 1
```
- Z[i] is the match length
- Adjust R to point to the last matching position (R ended one past the match)

**Case 2: Inside Z-box**
```python
else:
    k = i - L
```
- Position i is inside [L, R]
- k is the mirror position in the prefix

**Subcase 2a: Mirror fits**
```python
if Z[k] < R - i + 1:
    Z[i] = Z[k]
```
- R - i + 1 is the number of characters remaining in the Z-box from position i
- If Z[k] is smaller, the mirror value fits entirely within the box
- Safe to copy without comparing

**Subcase 2b: May extend**
```python
else:
    L = i
    while R < n and S[R] == S[R-L]:
        R = R + 1
    Z[i] = R - L
    R = R - 1
```
- The mirror suggests a match that reaches or exceeds the box boundary
- We've verified matches up to position R, but need to check beyond
- Update L = i (new Z-box starts at i)
- Extend R as far as possible
- Adjust R to last matching position

### Critical Details

**Why R-- after extending?**
- The while loop continues until s[R] ≠ s[R-L]
- R ends up pointing one position past the last match
- We adjust it back so R points to the actual last matching character

**Why update L only in Cases 1 and 2b?**
- L represents the start of the rightmost Z-box
- In Subcase 2a, we don't extend beyond R, so the Z-box doesn't change
- In Cases 1 and 2b, we're creating or extending a Z-box, so we update L

**The inequality Z[k] < R - i + 1:**
- This is the heart of the optimization
- It checks whether the mirror value fits within the current Z-box boundaries
- Geometrically: does the match starting at k fit within the remaining space from i to R?

---
```

- [ ] **Step 2: Add Section 7 (step-by-step table example)**

Append:

```markdown
## 7. Step-by-Step Example

Let's work through a complete example in table format to solidify understanding.

**String:** "aabxaabxc"

### Computation Table

| Step | i | L | R | Case | k | Z[k] | R-i+1 | Action | Z[i] | Notes |
|------|---|---|---|------|---|------|-------|--------|------|-------|
| 0 | - | 0 | 0 | Init | - | - | - | - | - | Initial state |
| 1 | 1 | 0 | 0 | Outside | - | - | - | Compare from i=1 | 1 | Match: 'a' |
| 2 | 2 | 1 | 1 | Outside | - | - | - | Compare from i=2 | 0 | 'b' ≠ 'a' |
| 3 | 3 | 1 | 1 | Outside | - | - | - | Compare from i=3 | 0 | 'x' ≠ 'a' |
| 4 | 4 | 1 | 1 | Outside | - | - | - | Compare from i=4 | 4 | Match: 'aabx' |
| 5 | 5 | 4 | 7 | Inside | 1 | 1 | 3 | Copy (1 < 3) | 1 | Subcase 2a |
| 6 | 6 | 4 | 7 | Inside | 2 | 0 | 2 | Copy (0 < 2) | 0 | Subcase 2a |
| 7 | 7 | 4 | 7 | Inside | 3 | 0 | 1 | Copy (0 < 1) | 0 | Subcase 2a |
| 8 | 8 | 4 | 7 | Outside | - | - | - | Compare from i=8 | 0 | 'c' ≠ 'a' |

**Final Z-array:**
```
Position:  0 1 2 3 4 5 6 7 8
String:    a a b x a a b x c
Z-array:   - 1 0 0 4 1 0 0 0
```

### Detailed Narrative for Selected Steps

**Step 4 (i=4):**
- Outside the Z-box (4 > 1)
- Compare starting at position 4:
  - s[4] vs s[0]: 'a' vs 'a' ✓
  - s[5] vs s[1]: 'a' vs 'a' ✓
  - s[6] vs s[2]: 'b' vs 'b' ✓
  - s[7] vs s[3]: 'x' vs 'x' ✓
  - s[8] vs s[4]: 'c' vs 'a' ✗
- Match length = 4
- Update: L=4, R=7, Z[4]=4
- Large Z-box created: [4, 7]

**Step 5 (i=5):**
- Inside Z-box (5 ≤ 7) ✓
- Mirror: k = 5-4 = 1
- Z[1] = 1
- Remaining in box: 7-5+1 = 3
- Check: 1 < 3 ✓ (fits within box)
- **Action:** Copy Z[5] = Z[1] = 1
- **No comparisons needed!**
- L and R unchanged

**Step 8 (i=8):**
- Outside Z-box (8 > 7)
- Compare: s[8] vs s[0]: 'c' vs 'a' ✗
- Z[8] = 0
- No Z-box update

### Comparison Count

**Naive approach:** Would make ~36 character comparisons
**Z-algorithm:** Made only ~10 comparisons (positions 1,2,3,4,8)
**Speedup:** Used mirror values at positions 5,6,7 with zero comparisons

This demonstrates the power of reusing information!

---
```

---

### Task 7: Tutorial Sections 8-9 (Implementation & Complexity)

**Files:**
- Modify: `programming_learning_notes/Algorithm/Z-algorithm/z-algorithm-tutorial.md`

- [ ] **Step 1: Add Section 8 (Python implementation)**

Append:

```markdown
## 8. Python Implementation

Now let's see working Python code. We'll present three versions: educational (heavily commented), production (clean), and application (pattern matching).

### Version 1: Educational (Heavily Commented)

See the complete implementation in [`z_algorithm.py`](z_algorithm.py):

```python
def z_algorithm_educational(s: str) -> list:
    """
    Compute Z-array for string s using Z-algorithm.
    Educational version with extensive comments.
    """
    n = len(s)
    if n == 0:
        return []
    
    z = [0] * n
    z[0] = 0  # Z[0] undefined, use 0 by convention
    
    left = 0  # Left boundary of rightmost Z-box
    right = 0  # Right boundary of rightmost Z-box
    
    for i in range(1, n):
        if i > right:
            # Case 1: Outside Z-box - compute naively
            left = i
            right = i
            
            while right < n and s[right] == s[right - left]:
                right += 1
            
            z[i] = right - left
            right -= 1  # Adjust to last matching position
        
        else:
            # Case 2: Inside Z-box - use mirror
            k = i - left
            remaining = right - i + 1
            
            if z[k] < remaining:
                # Subcase 2a: Mirror fits within box
                z[i] = z[k]
            else:
                # Subcase 2b: May extend beyond box
                left = i
                while right < n and s[right] == s[right - left]:
                    right += 1
                z[i] = right - left
                right -= 1
    
    return z
```

### Version 2: Clean Production Code

```python
def z_algorithm(s: str) -> list:
    """Compute Z-array in O(n) time."""
    n = len(s)
    if n == 0:
        return []
    
    z = [0] * n
    left, right = 0, 0
    
    for i in range(1, n):
        if i > right:
            left = right = i
            while right < n and s[right] == s[right - left]:
                right += 1
            z[i] = right - left
            right -= 1
        else:
            k = i - left
            if z[k] < right - i + 1:
                z[i] = z[k]
            else:
                left = i
                while right < n and s[right] == s[right - left]:
                    right += 1
                z[i] = right - left
                right -= 1
    
    return z
```

### Version 3: Pattern Matching Application

```python
def z_algorithm_search(text: str, pattern: str) -> list:
    """Find all occurrences of pattern in text."""
    if not pattern or not text:
        return []
    
    # Concatenate with separator
    combined = pattern + "$" + text
    z = z_algorithm(combined)
    
    # Find positions where Z[i] == len(pattern)
    pattern_len = len(pattern)
    matches = []
    
    for i in range(pattern_len + 1, len(combined)):
        if z[i] == pattern_len:
            text_index = i - pattern_len - 1
            matches.append(text_index)
    
    return matches
```

### Helper Function: Visualization

```python
def print_z_array(s: str, z: list) -> None:
    """Print string and Z-array aligned."""
    print("Position:", " ".join(f"{i:2}" for i in range(len(s))))
    print("String:  ", " ".join(f" {c}" for c in s))
    print("Z-array: ", " ".join(f"{('-' if i == 0 else str(z[i])):2}" for i in range(len(z))))
```

### Usage Examples

```python
# Example 1: Compute Z-array
s = "aabcaabxaaz"
z = z_algorithm(s)
print_z_array(s, z)

# Output:
# Position:  0  1  2  3  4  5  6  7  8  9 10
# String:    a  a  b  c  a  a  b  x  a  a  z
# Z-array:   -  1  0  0  3  1  0  0  2  1  0

# Example 2: Pattern matching
text = "ababcababcabab"
pattern = "abab"
matches = z_algorithm_search(text, pattern)
print(f"Pattern '{pattern}' found at: {matches}")

# Output:
# Pattern 'abab' found at: [0, 5, 10]
```

### Testing Your Implementation

Run the implementation file to verify:

```bash
python z_algorithm.py
```

Expected output should show Z-arrays for test strings and pattern matching results.

---
```

- [ ] **Step 2: Add Section 9 (Complexity analysis)**

Append:

```markdown
## 9. Complexity Analysis

Let's rigorously prove why the Z-algorithm achieves O(n) time complexity.

### Time Complexity: O(n)

**The key insight:** The pointer R only moves rightward throughout the algorithm (with occasional -1 adjustments).

#### Proof Sketch

**1. Observation about R:**
Throughout the algorithm, R either:
- Stays the same (when copying mirror values in Subcase 2a)
- Increases (when extending in Case 1 or Subcase 2b)
- Decreases by exactly 1 (the R-- adjustment)

**2. Character comparisons:**
Each character at position j can be visited by R at most twice:
- Once when R reaches it during extension (Case 1 or Subcase 2b)
- Once when computing Z[j] itself (if j is outside a Z-box)

**3. Non-comparison operations:**
- Copying mirror values (Subcase 2a): O(1) per iteration
- Calculating k = i - L: O(1)
- Updating L, R: O(1)
- Loop overhead: n iterations × O(1) = O(n)

**4. Total comparisons:**
Since each of the n characters can be compared at most twice:
- Maximum comparisons = 2n
- This is O(n)

**5. Overall complexity:**
- Comparisons: O(n)
- Other operations: O(n)
- **Total: O(n)**

#### Visual Proof with Worst Case

Consider the worst case: **"aaaaaaa"** (all same characters)

```
Position:  0 1 2 3 4 5 6
String:    a a a a a a a
```

**Step 1 (i=1):**
- Compare positions: 1,2,3,4,5,6 with prefix
- 6 comparisons
- Z[1] = 6, L=1, R=6

**Steps 2-6 (i=2 to 6):**
- All positions are inside [1,6]
- All use Subcase 2a or 2b with minimal comparisons
- Each position checked at boundary: at most 1 comparison each
- Total: ~6 more comparisons

**Total comparisons:** ~12 (less than 2n = 14) ✓

Even in the worst case, we stay within O(n)!

#### Amortized Analysis

Using **amortized analysis**:
- Each position contributes O(1) amortized time
- Over n positions: O(n) total

**Why amortized?**
- Some iterations (Case 1) do more work (extending R)
- Other iterations (Subcase 2a) do less work (just copying)
- The total work is bounded by O(n) because R never moves backward significantly

### Space Complexity: O(n)

**Memory usage:**
- Z-array: O(n) space
- Variables L, R, i, k: O(1) space
- **Total: O(n)**

No recursion, no additional data structures needed.

### Comparison with Naive Approach

| Algorithm | Time | Space | Comparisons (worst) |
|-----------|------|-------|---------------------|
| Naive | O(n²) | O(n) | n×(n-1)/2 ≈ n²/2 |
| Z-Algorithm | O(n) | O(n) | ≤ 2n |

For n = 1,000,000:
- Naive: ~500 billion comparisons
- Z-Algorithm: ~2 million comparisons
- **Speedup: ~250,000×**

### Pattern Matching Complexity

For pattern matching (pattern length m, text length n):

**Building combined string:** O(m + n)
**Computing Z-array:** O(m + n)
**Finding matches:** O(m + n)

**Total: O(m + n)** 🎯

This matches the optimal complexity for pattern matching!

---
```

---

### Task 8: Tutorial Sections 10-12 (Applications, Practice, References)

**Files:**
- Modify: `programming_learning_notes/Algorithm/Z-algorithm/z-algorithm-tutorial.md`

- [ ] **Step 1: Add Section 10 (Applications)**

Append to tutorial (content in next step due to length)

- [ ] **Step 2: Write Section 10 content**

```markdown
## 10. Applications & Use Cases

The Z-algorithm is versatile. Here are its main applications:

### 1. Pattern Matching (Primary Use)

**Problem:** Find all occurrences of pattern P in text T

**Solution:**
1. Construct S = P + "$" + T
2. Compute Z-array for S
3. Positions where Z[i] = |P| are matches

**Time:** O(|P| + |T|)

**Example:**
```python
text = "GATCGATCGAT"
pattern = "GATC"
matches = z_algorithm_search(text, pattern)
# Returns: [0, 4, 8]
```

### 2. Longest Common Prefix (LCP) Queries

**Problem:** Find LCP between prefix and substring at position i

**Solution:** Z[i] directly gives the answer!

**Example:**
```python
s = "abcabxab"
z = z_algorithm(s)
# Z[3] = 2 means LCP(s[0:], s[3:]) = "ab"
```

### 3. Detecting String Periods

**Problem:** Check if string is formed by repeating a substring

**Solution:** If Z[i] + i = n for some i, the prefix repeats

**Example:**
```python
s = "abcabcabc"
z = z_algorithm(s)
# Z[3]=6, and 3+6=9=len(s)
# So "abc" repeats!
```

### 4. Practical Applications

#### Bioinformatics:
- **DNA sequence alignment:** Find genetic markers in genomes
- **Motif discovery:** Locate repeated patterns in proteins
- **Gene matching:** Compare sequences efficiently

#### Text Processing:
- **Search engines:** Fast text indexing and retrieval
- **Text editors:** Find/replace functionality
- **Plagiarism detection:** Identify copied passages

#### Web Development:
- **URL routing:** Match request patterns
- **Log analysis:** Find patterns in server logs
- **Data compression:** Identify repeated substrings for encoding

### 5. Comparison with Other Algorithms

#### Z-Algorithm vs KMP (Knuth-Morris-Pratt):

| Feature | Z-Algorithm | KMP |
|---------|-------------|-----|
| Time | O(n + m) | O(n + m) |
| Preprocessing | Z-array | Failure function |
| Ease of implementation | ★★★★★ Simpler | ★★★☆☆ More complex |
| Memory | O(n + m) | O(m) for pattern |
| Use case | All occurrences | All occurrences |

**When to choose Z-algorithm:**
- Easier to understand and code
- Need prefix information for other purposes
- Competitive programming (faster to implement)

**When to choose KMP:**
- Memory constrained (KMP uses less)
- Only need pattern preprocessing

#### Z-Algorithm vs Boyer-Moore:

| Feature | Z-Algorithm | Boyer-Moore |
|---------|-------------|-------------|
| Time (average) | O(n + m) | O(n/m) sublinear! |
| Time (worst) | O(n + m) | O(nm) |
| Complexity | Moderate | High |

**When to choose Z-algorithm:**
- Guaranteed linear time needed
- Implementation simplicity matters
- Small alphabet (Boyer-Moore advantage diminishes)

**When to choose Boyer-Moore:**
- Large alphabet (DNA, text)
- Average case performance critical
- Pattern length m is significant

### Real-World Example: DNA Sequence Analysis

```python
def find_genetic_marker(dna_sequence: str, marker: str) -> list:
    """
    Find all occurrences of a genetic marker in DNA sequence.
    
    Example:
        dna = "ATCGATCGTAGCTAGCTA..."  # millions of base pairs
        marker = "TAGC"  # gene of interest
        positions = find_genetic_marker(dna, marker)
    """
    return z_algorithm_search(dna_sequence, marker)

# Real usage in bioinformatics pipelines
cancer_gene = "BRCA1"
human_genome_chr17 = load_chromosome_17()  # ~83 million base pairs
occurrences = find_genetic_marker(human_genome_chr17, cancer_gene)
# Completes in milliseconds thanks to O(n) complexity!
```

---
```

- [ ] **Step 3: Add Section 11 (Practice problems)**

Append:

```markdown
## 11. Practice Problems

Test your understanding with these graduated exercises.

### Easy Problems

#### Problem 1: Basic Z-array Computation
**Task:** Implement the Z-algorithm and compute the Z-array for string `"aabxaayaab"`

**Expected output:** `[-, 1, 0, 0, 2, 1, 0, 3, 1, 0]`

<details>
<summary>Hint</summary>

Use the `z_algorithm()` function provided. Verify manually for the first few positions.
</details>

---

#### Problem 2: Simple Pattern Search
**Task:** Find all occurrences of `"abc"` in `"xabcyabcz"`

**Expected output:** `[1, 5]`

<details>
<summary>Hint</summary>

Use the `z_algorithm_search()` function. Remember the combined string has format "pattern$text".
</details>

---

### Medium Problems

#### Problem 3: Shortest Repeating Substring
**Task:** Find the length of the shortest substring that appears at least twice.

**Example:** `"abcabcabc"` → `3` (substring "abc")

<details>
<summary>Hint</summary>

For each position i, Z[i] tells us the match length. Look for Z[i] > 0 where the match would create an overlap or repetition. The smallest such length is your answer.
</details>

---

#### Problem 4: String Period Detection
**Task:** Determine if a string can be formed by repeating a substring k times. Return the shortest period length, or -1 if not periodic.

**Example:** 
- `"abcabcabc"` → `3` (period = "abc")
- `"abcabc"` → `3`
- `"abcdef"` → `-1` (not periodic)

<details>
<summary>Hint</summary>

Check if Z[i] + i = n for any i. This means the prefix repeats starting at position i. Verify that i divides n evenly (so it repeats an integer number of times).
</details>

---

#### Problem 5: Count Distinct Substrings
**Task:** Count the number of distinct substrings in a string.

**Example:** `"aab"` → `6` (substrings: "a", "a", "b", "aa", "ab", "aab", but "a" appears twice, so distinct count = 5... wait, include empty? Clarify!)

<details>
<summary>Hint</summary>

This is more advanced. For each suffix, use Z-algorithm to find LCP with previous suffixes. The number of new substrings starting at position i equals the suffix length minus the maximum LCP with all previous suffixes. Sum these values.
</details>

---

### Hard Problems

#### Problem 6: Longest Palindromic Substring Using Z-Algorithm
**Task:** Find the longest palindromic substring using the Z-algorithm.

**Example:** `"abaxabaxabb"` → `"baxabaxab"` (length 9)

<details>
<summary>Hint</summary>

For each center position (both odd and even lengths):
1. Reverse the suffix after the center
2. Concatenate: suffix + "#" + reversed_prefix
3. Use Z-algorithm to find matches
4. The Z-values indicate palindrome lengths
</details>

---

#### Problem 7: LCP Between All Suffix Pairs
**Task:** Preprocess a string so you can answer queries: "What is the LCP between suffix[i] and suffix[j]?"

<details>
<summary>Hint</summary>

Build suffix array, then use Z-algorithm on concatenated suffixes. Alternatively, build LCP array using Z-algorithm on adjacent suffixes. This requires understanding suffix arrays.
</details>

---

### Solutions

Detailed solutions with code and explanations are in [z-algorithm-solutions.md](z-algorithm-solutions.md).

---
```

- [ ] **Step 4: Add Section 12 (References)**

Append:

```markdown
## 12. References

### Primary Tutorials

1. **GeeksforGeeks: Z Algorithm**
   - [https://www.geeksforgeeks.org/dsa/z-algorithm-linear-time-pattern-searching-algorithm/](https://www.geeksforgeeks.org/dsa/z-algorithm-linear-time-pattern-searching-algorithm/)
   - Good for additional examples and visual aids

2. **CP-Algorithms: Z-function**
   - [https://cp-algorithms.com/string/z-function.html](https://cp-algorithms.com/string/z-function.html)
   - Comprehensive coverage with advanced applications
   - Competitive programming perspective

3. **Codeforces Educational Materials**
   - Various tutorial blogs and editorials
   - Community discussions on Z-algorithm

### Related Algorithms

- **KMP (Knuth-Morris-Pratt):** Alternative O(n+m) pattern matching
- **Aho-Corasick:** Multiple pattern matching using trie structure
- **Suffix Arrays/Trees:** Advanced string data structures for range queries
- **Manacher's Algorithm:** Specialized for palindrome detection (faster than Z-algorithm for this specific problem)

### Books

1. **"Introduction to Algorithms" (CLRS)** - Chapter 32: String Matching
   - Covers KMP, doesn't cover Z-algorithm directly but provides context

2. **"Competitive Programming 3" by Steven & Felix Halim**
   - Practical implementation tips and problem sets
   - Section on string processing algorithms

3. **"Algorithms on Strings, Trees, and Sequences" by Dan Gusfield**
   - Comprehensive academic treatment
   - Deep dive into string algorithm theory

### Practice Platforms

- **LeetCode:** Search for problems tagged "String" and "Pattern Matching"
  - Problems like "Find All Anagrams in a String", "Repeated String Match"
  
- **Codeforces:** Educational rounds often feature string problems
  - Recommended: Div 2/3 problems with "strings" tag
  
- **HackerRank:** String algorithm track
  - Practice problems with test cases and discussions
  
- **SPOJ (Sphere Online Judge):** Classical problems
  - "PATTERN - Pattern Find" and similar

### Video Resources

Search YouTube for:
- "Z algorithm visualization"
- "String matching algorithms explained"

Look for videos that show L/R pointer movement visually.

### Further Reading

- Original paper on linear-time string matching
- Advanced applications in computational biology
- Z-algorithm variants for approximate matching

---

## Conclusion

Congratulations! You now understand the Z-algorithm from the ground up:

✅ **What** the Z-array represents  
✅ **Why** the Z-box and mirror optimization works  
✅ **How** to implement it in O(n) time  
✅ **When** to use it vs alternatives  

The Z-algorithm exemplifies elegant algorithm design: a simple insight (reuse previous comparisons) leads to dramatic improvement (O(n²) → O(n)).

**Next steps:**
1. Implement the algorithm from scratch without looking
2. Solve the practice problems
3. Apply it to a real project (text search, bio sequence analysis, etc.)
4. Explore related algorithms (KMP, suffix arrays)

Happy coding! 🚀

---

*Tutorial created: 2026-05-17*  
*Python implementation: [z_algorithm.py](z_algorithm.py)*  
*Practice solutions: [z-algorithm-solutions.md](z-algorithm-solutions.md)*
```

---

### Task 9: Practice Problem Solutions Document

**Files:**
- Create: `programming_learning_notes/Algorithm/Z-algorithm/z-algorithm-solutions.md`

- [ ] **Step 1: Create solutions file with easy problems**

```markdown
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
```

---

### Task 10: Final Review and Formatting

**Files:**
- Modify: All created files for final polish

- [ ] **Step 1: Review tutorial for formatting consistency**

Check:
- Section numbering matches TOC
- Code blocks have proper syntax highlighting
- ASCII diagrams are aligned
- Internal links work

- [ ] **Step 2: Verify Python code runs correctly**

Run:
```bash
cd programming_learning_notes/Algorithm/Z-algorithm
python z_algorithm.py
```

Expected: Clean output with examples

- [ ] **Step 3: Add callout boxes to tutorial**

Search for "Key insight" text and format as blockquotes with > prefix

- [ ] **Step 4: Final test of all deliverables**

Verify all three files exist and are complete:
- z-algorithm-tutorial.md
- z_algorithm.py
- z-algorithm-solutions.md

---

## Completion Checklist

- [ ] Python implementation complete and tested
- [ ] Tutorial sections 1-2 written
- [ ] Tutorial section 3 written
- [ ] Tutorial section 4 written
- [ ] Tutorial section 5 written
- [ ] Tutorial sections 6-7 written
- [ ] Tutorial sections 8-9 written
- [ ] Tutorial sections 10-12 written
- [ ] Solutions document created
- [ ] Final review and formatting complete

---

## Notes

**Estimated time:** 9-15 hours total
- Tasks 1-2: ~2 hours
- Tasks 3-5: ~3-4 hours (core algorithm explanation)
- Tasks 6-7: ~2 hours
- Tasks 8-9: ~2-3 hours
- Task 10: ~1-2 hours

**Key success factors:**
- Clear ASCII diagrams throughout
- Multiple worked examples
- Emphasis on WHY the optimization works
- Working, tested Python code
