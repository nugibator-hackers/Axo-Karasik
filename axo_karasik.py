class AhoCorasick:
    class Node:
        def __init__(self):
            self.children = {}
            self.fail_link = None
            self.output = []

    def __init__(self, patterns):
        self.root = self.Node()
        self.build_trie(patterns)
        self.build_failure_links()

    def build_trie(self, patterns):
        for pattern in patterns:
            current_node = self.root
            for char in pattern:
                if char not in current_node.children:
                    current_node.children[char] = self.Node()
                current_node = current_node.children[char]
            current_node.output.append(pattern)

    def build_failure_links(self):
        from collections import deque

        queue = deque()
        for char, node in self.root.children.items():
            node.fail_link = self.root
            queue.append(node)

        while queue:
            current_node = queue.popleft()

            for char, child_node in current_node.children.items():
                queue.append(child_node)

                fail_node = current_node.fail_link
                while fail_node is not None and char not in fail_node.children:
                    fail_node = fail_node.fail_link
                child_node.fail_link = (fail_node.children[char] if fail_node else self.root)

                if fail_node:
                    child_node.output += fail_node.children[char].output if char in fail_node.children else []

    def search(self, text):
        current_node = self.root
        results = []

        for index, char in enumerate(text):
            while current_node is not None and char not in current_node.children:
                current_node = current_node.fail_link
            if current_node is None:
                current_node = self.root
                continue
            current_node = current_node.children[char]

            # Check for output patterns
            for pattern in current_node.output:
                results.append((index - len(pattern) + 1, pattern))

        return results


# Тест 1: Базовый случай
patterns = ["ab", "bc", "abc"]
ac = AhoCorasick(patterns)
text = "abcabc"
result = ac.search(text)
print("Результат:", result)

# Тест 2: Несколько вхождений
patterns1 = ["ab", "bc", "abc"]
ac1 = AhoCorasick(patterns1)
text1 = "abcabc"
result1 = ac1.search(text1)
print("Результат:", result1)

# Тест 3: Паттерны не найдены
patterns2 = ["xyz", "abc"]
ac2 = AhoCorasick(patterns2)
text2 = "defgh"
result2 = ac2.search(text2)
print("Результат:", result2)

# Тест 4: Паттерны с перекрытием
patterns3 = ["ana", "anana"]
ac3 = AhoCorasick(patterns3)
text3 =  "bananas"
result3= ac3.search(text3)
print("Результат:", result3)

# Тест 5: Повторяющиеся паттерны
patterns4 = ["aa", "a"]
ac4 = AhoCorasick(patterns4)
text4 =  "aaaaa"
result4 = ac4.search(text4)
print("Результат:", result4)

# Тест 6: Пустой текст
patterns5 = ["a", "b"]
ac5 = AhoCorasick(patterns5)
text5 = ""
result5 = ac5.search(text5)
print("Результат:", result5)

# Тест 7: Один символ
patterns6 = ["a", "b"]
ac6 = AhoCorasick(patterns6)
text6 = "abababa"
result6 = ac6.search(text6)
print("Результат:", result6)