import sys

class Stack:
    def __init__(self):
        self.items = []

    def Empty(self):
        if len(self.items) == 0:
            return True
        else:
            return False

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

def main():
    if len(sys.argv) != 2:
        print('Usage error: python editor.py string')
        sys.exit()

    if len(sys.argv[1]) > 100000 or len(sys.argv[1]) < 1:
        print('invalid string')
        sys.exit()

    text = sys.argv[1]
    print(editor(text))

def editor(text):
    stack = Stack()
    counter = 0
    character_count = 0
    for character in text:
        counter += 1
        if character in ['(', '{', '[']:
            stack.push(character)
            character_count = 0
        elif character in [')', '}', ']']:
            character_count = 0
            if stack.Empty():
                return counter
            top = stack.pop()
            if (top == '(' and character != ')') or (top == '{' and character != '}') or (top == '[' and character != ']'):
                return counter
        else:
            character_count += 1
    if stack.Empty():
        return 'Success'
    else:
        return counter - character_count

if __name__ == "__main__":
    main()
