'''
---------------------------------

-----------Definitions-----------

This sequence is defined by the function a(n), which for a given positive integer n outputs the size of the set B_n, defined as follows.

A sequence of integers S is in the set B_n if it satisfies these conditions:
for i : 2 <= i <= n-2,
CN0. Elements of S are indexed from 2 to n-2, inclusive.
CN1. Elements of S are unique integers between 2 and n-2, inclusive.
CN2. S[i] + S[n-i] = n    Also stated as "elements in opposite positions sum to n"
CN3. S[S[i]] = i
CN4. For all k : 1 <= k <= n-3, the sum of any subsequence of S with length k is not congruent to k (mod n-1)
CN5. Let m_i be equal to "the sum of all elements preceding S[i]" plus "the sum of all elements preceding S[S[i]]" mod (n-1). Then
    CN5a. m_i = m is constant for all i
    CN5b. m and n are not both odd. 


Note that all members of B_n have length n-3

a(n) starts at n=4, since cases n <= 3 are degenerate

------------Examples-------------

The sequence S = [3, 2, 4, 6, 5] is in B_8
CN0. S[2] = 3 (2-indexed)
CN1. trivially verifiable
CN2. S[2] + S[6] = S[3] + S[5] = S[4] + S[4] = 8
CN3. S[S[2]] = 2, S[S[3]] = 3, etc.
CN4. Note that the case k = 1 is trivially true. Otherwise, considering the case k = 2,
    The set of all subsequences of S with length 2 is as follows: { [3,2], [2,4], [4,6], [6,5] }
    The sum of these subsequences (mod n-1) are as follows: [5, 6, 3, 4] i.e. none are equal to 2
    The same holds for all k
CN5. given the case i=5, m_i = (3 + 2 + 4) + (3 + 2 + 4 + 6) = (9+15) = 3 (mod n-1)
    CN5a. m_i = 3 for all i
    CN5b. 3 and 8 are not both odd


The S', the reversal of S, is also in B_8, (though the reversal of a sequence in B_n is not necessarily in B_n)
S and S' are the only members of B_8, thus a(8) = 2


The sequence T = [3, 2, 5, 4] is not in B_7, as it fails condition 5b. In fact, B_7 contains no members (i.e. a(7) = 0).


--------------Code---------------


We will iterate over all sequences which satisfy CN0-3, and verify CN4-5 with separate algorithms
To construct all such sequences, we start with a candidate list (CL) of invalid values (all 0) which we update until all values are valid, and fill it with a list of choices (from 2 to n-2). 

ITERATOR(CL, RC): Iterate over the remaining choices (RC), selecting each to be the next in the list. 
	1. Fill the next 0 element in the CL with the selected.
	2. Copy RC into RCC and remove the selected element from RCC.
	3. By CN2, we know the value of the element in the opposite position.
		if the opposite position is the same position (n-i == i), skip to step 5
		else if the opposite element is not in RCC, continue to next iteration step
		else, place the opposite element into the proper position and remove it from RCC
	4. By CN3, an element in any position either: 
		A. is equal to its index (or n minus the index)
			continue to step 5
		b. contains the index of the element which contains it. we can determine the identity of two more elements in the CL. 
			if they are not present in RCC, continue to next iteration step
			else, place them in CL and remove them from the RCC
	5. Now, filled members of CL satisfy CN0-3. 
		if RCC is empty, VALIDATOR(CL)
		else, ITERATOR(CL, RCC)
  		

VALIDATOR(CL): Perform the checks for CN4 and CN5:
	CN4: for k in range(1, n-3): 
		for i in range(2, n-k-2): 
			sub = CL[i:i+k]
			if sum(sub)%(n-1) == k:
				return false
	CN5: m_i = set()
	for i in CL[2:]: 
		m_i.add( (sum(CL[2:i]) + sum(CL[2:CL[i]]))%(n-1) )
	m=m_i.pop()
	if m_i:
		return false
	if (m*n)%2 == 1:
		return false
	solutions.append(CL[2:])
	return true
		
	
--------------Notes--------------

It appears that if a(n) is non-zero, n is a prime or prime power; n=7 appears to be the only prime power for which a(n) = 0

Extending the range from "2 to n-2" to "1 to n-1" fails to find any sequences satisfying all conditions

The constraint CN1 on its own has (n-3)! solutions, so the fact that solutions to CN0-5 are rare but existent is perhaps interesting


---------------------------------

'''
# Python forces us to 0-index arrays, so in some places notation like sample_list[2:] is used to get the "important" part of the list.
# If true 2-indexing was possible this would be redundant
# We'll fill the 0 and 1 indices with None (will usually raise an error if we try to do math with None)

from copy import copy

solutions = []

# Generates the sequence A from 4 to n
def A(n):
	return [a(i) for i in range(4,n+1)]


# a(n)
def a(n):
	return len(b_n(n))


# Returns a list containing all members of B_n for some n
def b_n(n):
	if n<4:
		return []
	solutions.clear()
	cl = [0]*(n-1)
	cl[0] = None
	cl[1] = None
	rc = list(range(2,n-1))
	iter(cl, rc)
	return solutions


# ITERATOR, described above
def iter(cl_, rc):
	n = len(cl_[2:])+3

	index = cl_.index(0)
	for sel in rc:	
		cl = copy(cl_)
		cl[index] = sel
		rcc = copy(rc)
		rcc.remove(sel)

		# CN2
		opp = n - sel
		if sel != opp:
			if opp not in rcc:
				continue
			cl[n-index] = opp
			rcc.remove(opp)

		# CN3
		if index != sel and index != opp:
			if index not in rcc or (n-index) not in rcc:
				continue
			if cl[sel] != 0 or cl[opp] != 0:
				continue
			cl[sel] = index
			cl[opp] = n-index
			rcc.remove(index)
			rcc.remove(n-index)

		
		if len(rcc) == 0:
			# CN4 & CN5
			validator(cl)
		else:
			iter(cl, rcc)


# VALIDATOR, described above
def validator(cl):
	n = len(cl[2:])+3

	# CN5
	m_i = set()
	for i in cl[2:]:
		m_i.add( (sum(cl[2:i]) + sum(cl[2:cl[i]])) % (n-1) )	
	# CN5a
	m=m_i.pop()
	if m_i:
		return False
	# CN5b
	if (m*n)%2 == 1:
		return False

	# CN4
	for k in range(1, n-3):
		for i in range(2, n-k-2):
			sub = cl[i:i+k]
			if sum(sub)%(n-1) == k:
				return False

	# CL satisfies all conditions
	solutions.append(cl[2:])
	return True
