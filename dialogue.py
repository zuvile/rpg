import re


class DialogueTree:
    def __init__(self, text, speaker, children=None):
        if children is None:
            children = []
        self.text = text
        self.speaker = speaker
        self.children = children
        self.parent = None


class Dialogue:
    def load_dialogue_tree(self):
        file = open('dialogue.txt', 'r')

        tree = self.create_tree(0, file.readlines(), None)
        return tree

    def create_tree(self, idx, lines, prev):
        if idx >= len(lines):
            #not sure why this is needed
            return prev.parent
        line = lines[idx].strip('\n')
        line = line.strip()
        if re.match('title: .*', line):
            return self.create_tree(idx + 1, lines, prev)
        if line == 'end_choices':
            return self.create_tree(idx + 1, lines, prev.parent.parent)
        if re.match("(.*): (.*)", line):
            speaker, dialogue = line.split(': ')
            new_node = DialogueTree(dialogue, speaker)
            if prev is not None:
                prev.children.append(new_node)
                new_node.parent = prev
            return self.create_tree(idx + 1, lines, new_node)

        if re.match("(->.*)", line.strip()):
            new_node = DialogueTree(line, "Player")
            new_node.parent = prev
            prev.children.append(new_node)
            return self.create_tree(idx + 1, lines, new_node)
        return self.create_tree(idx + 1, lines, prev)


def main():
    d = Dialogue()
    d.load_dialogue_tree()


if __name__ == '__main__':
    main()
