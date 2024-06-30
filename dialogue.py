import re

# this class builds the dialogue tree.
# The dialogue tree is a tree structure that represents the dialogue in the game.
# if children == 1 it means the speaker will continue to talk
# if children == 0 it means the conversation is over
# if children > 1, it means there's a choice for the player to make

class DialogueTree:
    def __init__(self, text, speaker, children=None):
        if children is None:
            children = []
        self.text = text
        self.speaker = speaker
        self.children = children
        self.parent = None
        self.rel_mod = 0
        self.jmp = None


class Dialogue:
    def load_dialogue_trees(self, file_name='dialogue.txt'):
        file = open(file_name, 'r')
        lines = file.readlines()
        dict = {}
        self.read_dialogue_chunks(lines, 0, dict, [])
        trees = {}
        for key, chunk in dict.items():
            tree = self.create_tree(0, chunk, None)
            trees[key] = tree
        return trees

    def create_tree(self, idx, lines, prev, root=None):
        if idx >= len(lines):
            return root if root is not None else prev
        line = lines[idx].strip('\n').strip()
        if re.match('title: .*', line):
            return self.create_tree(idx + 1, lines, prev, root)
        if line == 'end_choices':
            return self.create_tree(idx + 1, lines, prev.parent.parent, root)
        if re.match("(.*): (.*)", line):
            speaker, dialogue = line.split(': ')
            new_node = DialogueTree(dialogue, speaker)
            if prev is not None:
                prev.children.append(new_node)
                new_node.parent = prev
            if root is None:
                root = new_node
            return self.create_tree(idx + 1, lines, new_node, root)
        if re.match("(\$rel_mod\s.*)", line):
            _, modifier = line.split('=')
            prev.rel_mod = int(modifier)
            return self.create_tree(idx + 1, lines, prev, root)
        if re.match("(jmp=.*)", line):
            _, jmp = line.split('=')
            prev.jmp = jmp
            return self.create_tree(idx + 1, lines, prev, root)
        if re.match("(->.*)", line.strip()):
            new_node = DialogueTree(line, "Player")
            new_node.parent = prev
            prev.children.append(new_node)
            return self.create_tree(idx + 1, lines, new_node, root)
        return self.create_tree(idx + 1, lines, prev, root)

    def read_dialogue_chunks(self, lines, idx, dict, curr_title):
        if idx >= len(lines):
            return
        line = lines[idx].strip('\n').strip()
        if re.match('title: .*', line):
            _, title = line.split(': ')
            curr_title = title
            dict[curr_title] = []
            self.read_dialogue_chunks(lines, idx + 1, dict, curr_title)
        else:
            dict[curr_title].append(line)
            self.read_dialogue_chunks(lines, idx + 1, dict, curr_title)


def main():
    d = Dialogue()
    d.load_dialogue_trees()


if __name__ == '__main__':
    main()
