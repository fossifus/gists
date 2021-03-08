# USAGE: python bgg-compare.py $USER1 $STATUS1 $USER2 $STATUS2
# Optionally, the --not flag will "invert" the cross-reference result.

# TO DO: allow for filtering by custom comments (check if library has in stock)

# Examples:
# Find the intersection of the two lists.
# python bgg-compare.py fossifus wishlist GreatGamesLibrary owned
# Find games in my wishlist that are not owned by the library.
# python bgg-compare.py fossifus wishlist --not GreatGamesLibrary owned
# Note: the above set is not the complement of the intersection, since that is less useful far as I can see.

import sys
import boardgamegeek
bgg = boardgamegeek.BGGClient()

# filter and cross-reference two BGG lists
def compare(users, statuses):
    master_list = []
    for i, user in enumerate(users):
        status = statuses[i]
        collection = bgg.collection(user_name=user)
        if status == 'all':
            master_list.append([item.name for item in collection.items])
        else:
            master_list.append([item.name for item in collection.items if getattr(item, status)])
    if NOT_FLAG:
        return [val for val in master_list[0] if val not in master_list[1]]
    else:
        return [val for val in master_list[0] if val in master_list[1]]

# hardcoding BGG list options
if __name__ == '__main__':
    options = [
    'all',
    'for_trade',
    'owned',
    'prev_owned',
    'want',
    'wishlist',
    ]

# search for not flag
if '--not' in sys.argv:
    NOT_FLAG=True
    sys.argv.remove('--not')
else:
    NOT_FLAG=False

# check CLI pos params
if not (len(sys.argv) == 5 and sys.argv[2] in options and sys.argv[4] in options):
    print("Bad positional parameters.  Require exactly four params to cross-reference: $USER1 $STATUS1 $USER2 $STATUS2")
    exit()
else:
    users = [sys.argv[1], sys.argv[3]]
    statuses = [sys.argv[2], sys.argv[4]]

# cross-reference the two lists
try:
    result = compare(users, statuses)
    print(len(result), ":", result)
except e:
    print("An error occurred, please try again.")
