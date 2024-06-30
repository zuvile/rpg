import pytest
from dialogue import Dialogue

@pytest.fixture
def dialogue():
    return Dialogue()


def check_node(node, text, speaker, num_children, rel_mod, jmp):
    assert node.text == text
    assert node.speaker == speaker
    assert len(node.children) == num_children
    assert node.rel_mod == rel_mod
    assert node.jmp == jmp


def test_dialogue_tree(dialogue):
    trees = dialogue.load_dialogue_trees('dialogue_test.txt')
    tree1 = trees['introduction_cassius']
    tree2 = trees['cassius_ceremony_room']

    check_node(tree1, "Hello. I haven't seen you here before. My name is Cassius.", "Cassius", 1, 0, None)
    check_node(tree1.children[0], "I have no time to chat to newcomers. One thing though... It would be unwise to go outside until you're ready.", "Cassius", 2, 0, None)
    check_node(tree1.children[0].children[0], "-> Don't tell me what to do.", "Player", 1, -10, None)
    check_node(tree1.children[0].children[0].children[0], "Ah, I see how it is. Well, don't let me stand in the way of your untimely death.", "Cassius", 0, 0, None)
    check_node(tree1.children[0].children[1], "-> I see. Thank you.", "Player", 1, 10, None)
    check_node(tree1.children[0].children[1].children[0], "Did you get the chance to see the ceremony room?", "Cassius", 0, 0, 'cassius_ceremony_room')

    check_node(tree2, "It's a beautiful room, isn't it? I'm sure you'll be spending a lot of time there.", "Cassius", 0, 0, None)
