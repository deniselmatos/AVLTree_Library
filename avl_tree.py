class Node:
    def __init__(self, value) -> None:
        self.value = value
        self.left = None
        self.right = None
        self.node_height = 1


class Book:
    def __init__(self, title: str, author: str, year: str, isbn: str) -> None:
        self.title: str = title
        self.author: str = author
        self.year: int = int(year)
        self.isbn: int = int(isbn)

    def __str__(self) -> str:
        return f"Title: {self.title}, Author: {self.author}, Year: {self.year}, ISBN: {self.isbn}"

    def __lt__(self, other: object) -> bool:
        if isinstance(other, Book):
            return self.title < other.title
        elif isinstance(other, str):
            return self.title < other
        return False

    def __gt__(self, other: object) -> bool:
        if isinstance(other, Book):
            return self.title > other.title
        elif isinstance(other, str):
            return self.title > other
        return False
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, Book):
            return self.title == other.title or self.isbn == other.isbn
        return False

    def __ne__(self, other: object) -> bool:
        if isinstance(other, Book):
            return self.title != other.title or self.isbn != other.isbn
        return False


class AVLTree_Library:
    def __init__(self) -> None:
        self.root = None

    def register_book(self) -> Book:
        title = input("Type the title of the book: ")
        author = input("Type the author's name: ")
        year = input("Type the year the book was released: ")
        isbn = input("Type the ISBN of the book: ")
        
        try:
            isbn_int = int(isbn)
        except ValueError:
            print("ISBN must be an integer.")
            return self.register_book()
        return Book(title, author, year, isbn_int)

    def bigger(self, a, b) -> int:
        return a if a > b else b

    def node_height(self, node: Node) -> int:
        if node is None:
            return 0
        return node.node_height

    def balance_factor(self, node: Node) -> int:
        if node is None:
            return 0
        return self.node_height(node.left) - self.node_height(node.right)

    def left_rotate(self, node: Node) -> Node:
        aux = node.right
        node.right = aux.left
        aux.left = node
        node.node_height = (
            self.bigger(self.node_height(node.left), self.node_height(node.right)) + 1
        )
        aux.node_height = (
            self.bigger(self.node_height(aux.left), self.node_height(aux.right)) + 1
        )
        return aux

    def right_rotate(self, node: Node) -> Node:
        aux = node.left
        node.left = aux.right
        aux.right = node
        node.node_height = (
            self.bigger(self.node_height(node.left), self.node_height(node.right)) + 1
        )
        aux.node_height = (
            self.bigger(self.node_height(aux.left), self.node_height(aux.right)) + 1
        )
        return aux

    def left_right_rotate(self, node: Node) -> Node:
        node.left = self.left_rotate(node.left)
        return self.right_rotate(node)

    def right_left_rotate(self, node: Node) -> Node:
        node.right = self.right_rotate(node.right)
        return self.left_rotate(node)

    def _insert(self, node: Node, value) -> Node:
        if node is None:
            return Node(value)
        if value < node.value:
            node.left = self._insert(node.left, value)
        elif value > node.value:
            node.right = self._insert(node.right, value)
        elif value == node.value:
            print("\nDuplicate value. Book not added.")
            return node
        else:
            return node

        node.node_height = (
            self.bigger(self.node_height(node.left), self.node_height(node.right)) + 1
        )

        return self.balance(node)

    def insert(self, value: Book) -> None:
        self.root = self._insert(self.root, value)

    def balance(self, node: Node) -> Node:
        bf = self.balance_factor(node)

        if bf > 1:
            if self.balance_factor(node.left) >= 0:
                return self.right_rotate(node)
            else:
                return self.left_right_rotate(node)
        elif bf < -1:
            if self.balance_factor(node.right) <= 0:
                return self.left_rotate(node)
            else:
                return self.right_left_rotate(node)
        return node

    def search(self, title: str) -> bool:
        current = self.root
        while current:
            if title < current.value:
                current = current.left
            elif title > current.value:
                current = current.right
            else:
                return True
        return False

    def successor_node(self, node: Node) -> Node:
        current = node.right
        while current and current.left:
            current = current.left
        return current

    def _remove(self, node: Node, title: str) -> Node:
        if node is None:
            return node

        if title < node.value:
            node.left = self._remove(node.left, title)
        elif title > node.value:
            node.right = self._remove(node.right, title)
        else:
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left

            successor = self.successor_node(node)
            node.value = successor.value
            node.right = self._remove(node.right, successor.value.title)

        node.node_height = (
            self.bigger(self.node_height(node.left), self.node_height(node.right)) + 1
        )
        return self.balance(node)

    def remove(self, title: str) -> None:
        if not self.search(title):
            print(f"Title {title} not found.")
            return
        self.root = self._remove(self.root, title)
        print(f"Title {title} successfully removed.")

    def _in_order(self, node: Node) -> None:
        if node is not None:
            self._in_order(node.left)
            print(node.value)
            self._in_order(node.right)

    def in_order(self) -> None:
        self._in_order(self.root)

    def _pre_order(self, node: Node) -> None:
        if node is not None:
            print(node.value)
            self._pre_order(node.left)
            self._pre_order(node.right)

    def pre_order(self) -> None:
        self._pre_order(self.root)

    def _post_order(self, node: Node) -> None:
        if node is not None:
            self._post_order(node.left)
            self._post_order(node.right)
            print(node.value)

    def post_order(self) -> None:
        self._post_order(self.root)

def menu() -> str:
    while True:
        print("\nArcadia Library Home Page\n")
        print("Select the desired option:")
        print("1 - Add a new book to the library")
        print("2 - Remove a specific book from the library")
        print("3 - Display traversal methods")
        print("0 - End")

        op = input("\nChoose an option: ")

        if op in ["1", "2", "3", "0"]:
            return op
        else:
            print("\nInvalid option. Please try again.")

library = AVLTree_Library()

while True:
    op = menu()

    if op == "1":
        add_book: Book = library.register_book()
        library.insert(add_book)

    elif op == "2":
        title_input = str(input("Type the title of the book to remove: "))
        library.remove(title_input)
  

    elif op == "3":
        while True:
            print("\nSelect the traversal method:")
            print("1 - In-Order")
            print("2 - Pre-Order")
            print("3 - Post-Order")
            op_repeat = input("Choose an option: ")

            if op_repeat in ["1", "2", "3"]:
                break
            else:
                print("\nInvalid option. Please try again.")

        if op_repeat == "1":
            print("\n--- In-Order Traversal ---")
            library.in_order()

        elif op_repeat == "2":
            print("\n--- Pre-Order Traversal ---")
            library.pre_order()

        elif op_repeat == "3":
            print("\n--- Post-Order Traversal ---")
            library.post_order()

    elif op == "0":
        print("Exiting the program.")
        break