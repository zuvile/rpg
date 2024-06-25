class ListNode(object):
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Options:
    def get_options(self):
        attack = ListNode('attack')
        spell = ListNode('attack')
        run_away = ListNode('attack')
