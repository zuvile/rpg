import pytest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from dialogue.dialogue import Dialogue

@pytest.fixture
def dialogue():
    return Dialogue()


def check_node(node, text, speaker, num_children, rel_mods, jmp, render):
    assert node.text == text
    assert node.speaker == speaker
    assert len(node.children) == num_children
    assert node.rel_mods == rel_mods
    assert node.jmp == jmp
    assert node.render == render


def test_dialogue_tree(dialogue):
    trees = dialogue.load_dialogue_trees('dialogue/tests/dialogue_test.txt')
    tree1 = trees['introduction_cassius']
    tree2 = trees['cassius_ceremony_room']

    check_node(tree1, "Hello. I haven't seen you here before. My name is Cassius.", "Cassius", 1, {}, None, 'portrait_cassius.png')
    check_node(tree1.children[0], "I have no time to chat to newcomers. One thing though... It would be unwise to go outside until you're ready.", "Cassius", 2, {}, None, None)
    check_node(tree1.children[0].children[0], "-> Don't tell me what to do.", "Player", 1, {'Cassius': -10}, None, None)
    check_node(tree1.children[0].children[0].children[0], "Ah, I see how it is. Well, don't let me stand in the way of your untimely death.", "Cassius", 0, {}, None, None)
    check_node(tree1.children[0].children[1], "-> I see. Thank you.", "Player", 1, {'Cassius': 10}, None, None)
    check_node(tree1.children[0].children[1].children[0], "Did you get the chance to see the ceremony room?", "Cassius", 0, {}, 'cassius_ceremony_room', None)

    check_node(tree2, "It's a beautiful room, isn't it? I'm sure you'll be spending a lot of time there.", "Cassius", 0, {}, None, None)
