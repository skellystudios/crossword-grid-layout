
`unchecked_letters :: grid -> [(letter, position)]`

`merge :: grid -> position -> grid -> position -> Maybe grid`
	- checks for overlap – only need to look at overlapping n x m portion of the grid
	- need to check for overlap and adjacency
		overlap is easy
		adjacency - produce the whole grid and check for that? not really possible, I think, unless we store something else
		maybe:
			- perform overlap check
			- label each black square NOT next to an overlap square but next to filled square as "reserved"
			- check no insertion into reserved

`words :: grid -> [words]`

check each current grid for compatability word-wise, and also for if the combo has been checked before 
(needs a hashing function?)


# can only rotate a single word, not a grid
# need to record if a particular grid has been checked for merges against any other grid

do depth first search, use # interections as criteria for which item to mutate


order by intersections/words used then by # intersections

search by currently generated grids for the words not yet used in this one ???

only allow grids with better than n-1 intersections vs words ???? v unsure

****

DFS etc. strategies

1. Naive DFS: Take one starting point, and iteratively add to it

- Pointless as it doesn't ever generate any sub-pieces


2. Naive BFS: For each subgrid that currently exists, try to create 
   all pieces based on merging that with any currently extant subgrids,
   perhaps adding the new subgrid to the end of a queue

- Definitely creates a bunch of subgrids, which is good, but doesn't pay 
  any attention to whether it's generating an efficient grid in terms of 
  intersection / intersection ratio


3. Always pick the piece with the best intersection/word ratio at the current time

- Feels a little better than DFS, but I worry we'll still get bogged down in a 
  local maximum for a long time and the search won't work


4. Some sort of recursion, where we ask for a piece to try picked from the subgrids 
   that can be generated from the currently missing words.

- Not sure how to implement recursive step, worry that it wouldn't be efficient / would 
  just be DFS but from the other end


Current favourite is number 3


@@@ Adding two subgrids together into one or more new subgrids should also spawn 
    each of the "constituent parts" of those successful grids (if they don't 
    already exist) so they can be used in future work (as long as they're contiguous)

maybe we want the concept of parents and children 


>> Can we do this whole thing genetically?


