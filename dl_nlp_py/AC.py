from queue import Queue
import re


def convert_str_to_list(string):
    return re.findall('(\[.*?\])(\d*)', string)


class TrieNode(object):
    def __init__(self):
        self.one_byte = {}
        self.include_sid = set()
        self.match_sid = set()
        self.length = 0
        self.fail = None
        self.word = ''


class Trie256(object):
    def __init__(self, case_insensitvie=False):
        self.root = TrieNode()
        self.case_insensitive = case_insensitvie

    def get_utf8_string(self, string):
        if self.case_insensitive:
            return bytearray(string.lower().encode("utf-8"))
        else:
            return bytearray(string.encode("utf-8"))

    def insert(self, s, exact_match=False, sid=0):
        bytes_array = self.get_utf8_string(s)
        node = self.root
        for byte in bytes_array:
            child = node.one_byte.get(byte)
            if child is None:
                node.one_byte[byte] = TrieNode()
            node = node.one_byte[byte]
        node.word = s
        if exact_match is True:
            node.match_sid.add(sid)
        else:
            node.include_sid.add(sid)
        node.length = len(bytes_array)

    def build_ac_automation(self):
        q = Queue()
        self.root.fail = None
        q.put(self.root)
        while not q.empty():
            node = q.get()
            for k, v in node.one_byte.items():
                p = node.fail
                while p is not None:
                    if k in p.one_byte:
                        break
                    p = p.fail
                if p is not None:
                    v.fail = p.one_byte.get(k, self.root)
                else:
                    v.fail = self.root
                v.include_sid |= v.fail.include_sid
                q.put(v)

    def find(self, s):
        bytes_array = self.get_utf8_string(s)
        node = self.root
        result = set()
        for byte in bytes_array:
            while node != self.root and node.one_byte.get(byte, None) is None:
                node = node.fail
            node = node.one_byte.get(byte, self.root)
            result |= node.include_sid

        if node.length == len(bytes_array):
            result |= node.match_sid

        return list(result)

    def find_one(self, s):
        bytes_array = self.get_utf8_string(s)
        node = self.root
        result = set()
        for byte in bytes_array:
            while node != self.root and node.one_byte.get(byte, None) is None:
                node = node.fail
            node = node.one_byte.get(byte, self.root)
            if len(node.include_sid) > 0:
                word = node.word
                p = node
                while not word:
                    word = p.fail.word
                    p = p.fail
                result |= node.include_sid
                return list(result), word

        return [], ''


def main():
    sensitive_trie = Trie256()
    for i, item in enumerate(['her', 'say', 'she', 'shr']):
        sensitive_trie.insert(item, sid=i)
    sensitive_trie.build_ac_automation()
    print(sensitive_trie.find('yasherhshr'))


def test2():
    # AC 自动机库
    import ahocorasick
    pass


if __name__ == '__main__':
    main()
