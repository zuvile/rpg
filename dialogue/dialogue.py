import re

# this class builds the dialogue tree.
# The dialogue tree is a tree structure that represents the dialogue in the game.
# if children == 1, it means the conversation is linear
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
        self.rel_mods = {}
        self.jmp = None
        self.render = None
        self.init_fight = False
        self.auto_choice = False


class Dialogue:
    def load_dialogue_trees(self, file_name):
        file = open(file_name, 'r')
        lines = file.readlines()
        dict = {}
        self.read_dialogue_chunks(lines, 0, dict, [])
        trees = {}
        for key, chunk in dict.items():
            tree = self.create_tree(0, chunk, None)
            trees[key] = tree
        return trees

    def create_tree(self, idx, lines, prev, root=None, choice_root=None):
        if idx >= len(lines):
            return root if root is not None else prev
        line = lines[idx].strip('\n').strip()
        if re.match('title: .*', line):
            return self.handle_title(idx, lines, prev, root, choice_root)
        if line == 'end_choices':
            return self.handle_end_choices(idx, lines, root, choice_root)
        if re.match("(.*): (.*)", line):
            return self.handle_speaker_dialogue(idx, lines, prev, root, line, choice_root)
        if re.match("(\\$rel_mod.*)", line):
            return self.handle_rel_mod(idx, lines, prev, root, line, choice_root)
        if re.match("(\\$init_fight.*)", line):
            return self.handle_init_fight(idx, lines, prev, root, line, choice_root)
        if re.match("(\\$jmp=.*)", line):
            return self.handle_jmp(idx, lines, prev, root, line, choice_root)
        if re.match("(->.*)", line.strip()):
            return self.handle_choice(idx, lines, prev, root, line, choice_root)
        if re.match("(\\$render=.*)", line):
            return self.handle_render(idx, lines, prev, root, line, choice_root)
        return self.create_tree(idx + 1, lines, prev, root, choice_root)

    def handle_init_fight(self, idx, lines, prev, root, line, choice_root):
        prev.init_fight = True
        prev.auto_choice = True
        return self.create_tree(idx + 1, lines, prev, root, choice_root)

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

    def handle_title(self, idx, lines, prev, root, choice_root):
        return self.create_tree(idx + 1, lines, prev, root, choice_root)

    def handle_end_choices(self, idx, lines, root, choice_root):
        return self.create_tree(idx + 1, lines, choice_root, root, choice_root)

    def handle_speaker_dialogue(self, idx, lines, prev, root, line, choice_root):
        speaker, dialogue = line.split(': ')
        new_node = DialogueTree(dialogue, speaker)
        # the node had choices. Each choice now needs to point to the same next node
        if prev is not None and len(prev.children) > 1:
            choice_root = None
            self.update_children(prev, new_node)
        elif prev is not None:
            prev.children.append(new_node)
            new_node.parent = prev
        if root is None:
            root = new_node
        return self.create_tree(idx + 1, lines, new_node, root, choice_root)

    def update_children(self, prev, new_node):
        for child in prev.children:
            while len(child.children) > 0:
                child = child.children[0]
            child.children.append(new_node)

    def handle_rel_mod(self, idx, lines, prev, root, line, choice_root):
        match = re.search("\\((.*?)\\)=(-?\\d+)", line)
        char_name = match.group(1)
        modifier = match.group(2)
        prev.rel_mods[char_name] = int(modifier)
        return self.create_tree(idx + 1, lines, prev, root, choice_root)

    def handle_jmp(self, idx, lines, prev, root, line, choice_root):
        _, jmp = line.split('=')
        prev.jmp = jmp
        return self.create_tree(idx + 1, lines, prev, root, choice_root)

    def handle_choice(self, idx, lines, prev, root, line, choice_root):
        if choice_root is None:
            choice_root = prev
        new_node = DialogueTree(line, "Player")
        choice_root.children.append(new_node)
        new_node.parent = choice_root
        return self.create_tree(idx + 1, lines, new_node, root, choice_root)

    def handle_render(self, idx, lines, prev, root, line, choice_root):
        prev.render = line.split('=')[1]
        return self.create_tree(idx + 1, lines, prev, root, choice_root)