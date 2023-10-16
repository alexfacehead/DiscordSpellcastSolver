from english_words import get_english_words_set
from termcolor import colored

# Constants
GRID_SIZE = 5
LETTER_VALUES = {
    'a': 1, 'b': 4, 'c': 5, 'd': 3,
    'e': 1, 'f': 5, 'g': 3, 'h': 4,
    'i': 1, 'j': 7, 'k': 6, 'l': 3,
    'm': 4, 'n': 2, 'o': 1, 'p': 4,
    'q': 10, 'r': 2, 's': 2, 't': 3,
    'u': 4, 'v': 5, 'w': 5, 'x': 7,
    'y': 4, 'z': 8
}

# Load dictionary words
web2lowerset = get_english_words_set(['web2'], lower=True)

class TrieNode:
    """A node in the Trie data structure."""

    def __init__(self):
        self.children = {}
        self.is_word = False

class Trie:
    """A Trie data structure for efficient word search and insertion."""

    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        """Insert a word into the Trie."""
        node = self.root
        for letter in word:
            if letter not in node.children:
                node.children[letter] = TrieNode()
            node = node.children[letter]
        node.is_word = True

    def remove(self, word):
        """Remove a word from the Trie."""

        def _remove(node, idx):
            if idx == len(word):
                if node.is_word:
                    node.is_word = False
                    return len(node.children) == 0
                return False

            letter = word[idx]
            if letter not in node.children or not _remove(node.children[letter], idx + 1):
                return False

            if len(node.children[letter].children) == 0:
                del node.children[letter]

            return len(node.children) == 0

        _remove(self.root, 0)

    def search(self, word):
        """Search for a word in the Trie."""
        node = self.root
        for letter in word:
            if letter not in node.children:
                return False
            node = node.children[letter]
        return node.is_word


def build_trie(words):
    """Build a Trie from a list of words."""
    trie = Trie()
    for word in words:
        trie.insert(word)
    return trie


def dfs(grid, trie_node, i, j, current_word, words, path, special_index):
    """Depth-first search to generate words from the grid."""
    if i < 0 or i >= len(grid) or j < 0 or j >= len(grid[0]) or grid[i][j] == "#":
        return

    letter = grid[i][j]
    if letter not in trie_node.children:
        return

    current_word += letter
    trie_node = trie_node.children[letter]
    path.append((i, j))

    if trie_node.is_word:
        score = calculate_score(current_word, LETTER_VALUES, special_index, path)
        words.add((current_word, score))

    grid[i][j] = "#"  # Mark as visited
    for x, y in [(i-1, j), (i+1, j), (i, j-1), (i, j+1), (i-1, j-1), (i-1, j+1), (i+1, j-1), (i+1, j+1)]:
        dfs(grid, trie_node, x, y, current_word, words, path, special_index)
    grid[i][j] = letter  # Restore the letter
    path.pop()


def generate_words(grid, trie, special_index):
    """Generate all valid words from the grid."""
    words = set()
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            dfs(grid, trie.root, i, j, "", words, [], special_index)
    return words


def find_highest_scoring_word(grid, trie, special_index):
    """Find the highest-scoring word in the grid."""
    words = generate_words(grid, trie, special_index)
    highest_score = 0
    highest_scoring_word = ""

    for word, score in words:
        if score > highest_score:
            highest_score = score
            highest_scoring_word = word

    return highest_scoring_word, highest_score

def contains_special_character(word, special_index):
    """Check if the word contains the special character at the specified index."""
    return len(word) > special_index and word[special_index] == "e"


def calculate_score(word, letter_values, special_index, path):
    """Calculate the score of a word based on letter values and special character."""
    score = 0
    for idx, letter in enumerate(word):
        score += letter_values.get(letter, 4)
    if (special_index // GRID_SIZE, special_index % GRID_SIZE) in path:
        score *= 2
    return score

def get_user_input_grid(size):
    """Get the grid input from the user."""
    grid = []
    print(f"Enter all 25 letters for the {size}x{size} grid in a single line:")
    print()
    print(colored(f"ENTER LETTERS HERE: ", "magenta"))
    letters = input().strip().lower()
    if letters.lower() == "q" or letters.lower() == "quit" or letters.lower() == "exit":
        print(colored("User ended program.", "red"))
        exit(0)
    elif len(letters) != size * size:
        print(colored("Invalid input length. Please enter the correct number of letters.", "red"))
        get_user_input_grid(GRID_SIZE)
    for i in range(size):
        row = list(letters[i*size:(i+1)*size])
        grid.append(row)
    return grid

def main():
    # Build the trie with the dictionary words
    trie = build_trie(web2lowerset)

    # Get grid and special character index from the user
    original_grid = get_user_input_grid(GRID_SIZE)
    special_index = int(input("Enter the special character index (0-24): "))

    while True:
        user_grid = [row.copy() for row in original_grid]  # Create a copy of the original grid
        highest_scoring_word, highest_score = find_highest_scoring_word(user_grid, trie, special_index)
        print(f"The highest-scoring word is '{highest_scoring_word}' with a score of {highest_score}")

        # Remove the found word from the trie
        trie.remove(highest_scoring_word)

        # Ask the user if they want to continue generating words
        user_input = input("Do you want to continue generating words? (y/n): ").strip().lower()
        if user_input.lower() != "y":
            break

if __name__ == "__main__":
    main()