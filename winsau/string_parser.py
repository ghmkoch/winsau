import collections
import itertools
import copy


class Packed(object):
    @classmethod
    def unpack_zip_line(cls, value, *args, **kwargs):
        return list(itertools.product(*[Packed(value=i, *args, **kwargs).unpacked() for i in value]))

    @classmethod
    def unpack_zip_lines(cls, value, *args, **kwargs):
        res = []
        for i in value:
            for j in cls.unpack_zip_line(value=i, *args, **kwargs):
                res.append(j)
        return res
        #[cls.unpack_zip_line(value=i, *args, **kwargs) for i in value]

    def __init__(self, value, *args, **kwargs):
        self._value = value
        self._args = (args, kwargs)

    def unpacked(self):
        res = []
        value = self._value
        args, kwargs = self._args

        if isinstance(value, basestring):
            res += [i for i in Parser(text=value, *args, **kwargs).compiled_str()]
        elif hasattr(value, '__iter__'):
            for i in value:
                for j in Packed(i, *args, **kwargs).unpacked():
                    res.append(j)
        else:
            res.append(value)
        return res

    def iunpacked(self):
        value = self._value
        args, kwargs = self._args

        if isinstance(value, basestring):
            for i in Parser(text=value, *args, **kwargs).compiled_str():
                yield i
        elif hasattr(value, '__iter__'):
            for i in value:
                for j in Packed(i, *args, **kwargs).iunpacked():
                    yield j
        else:
            yield value

    def nest_unpacked(self):
        value = self._value
        args, kwargs = self._args

        if isinstance(value, basestring):
            return list(Parser(text=value, *args, **kwargs).compiled_str())
        elif hasattr(value, '__iter__'):
            return [Packed(i, *args, **kwargs).nest_unpacked() for i in value]
        else:
            return value

    def inest_unpacked(self):
        value = self._value
        args, kwargs = self._args

        if isinstance(value, basestring):
            return Parser(text=value, *args, **kwargs).compiled_str()
        elif hasattr(value, '__iter__'):
            return (Packed(i, *args, **kwargs).inest_unpacked() for i in value)
        else:
            return value


class Parser(object):
    def __init__(self, text, open_tag='($', close_tag=')', separator='|'):
        self.text = text
        self.open_tag = open_tag
        self.close_tag = close_tag
        self.separator = separator

    def nested(self):
        lvl = 0
        nest = []
        for i, par0 in enumerate(self.text.split(self.open_tag)):
            for j, par1 in enumerate(par0.split(self.close_tag)):
                if j == 0 and i > 0:
                    lvl += 1
                if j in (1, 2):
                    lvl -= 1
                if par1:
                    lvl_count = 0
                    lvl_item = nest
                    if len(lvl_item):
                        while (isinstance(lvl_item[-1], collections.Iterable)
                               and not isinstance(lvl_item[-1], basestring)
                               ) and lvl_count < lvl:
                            lvl_count += 1
                            lvl_item = lvl_item[-1]

                    new_val = par1
                    for j in range(lvl - lvl_count):
                        new_val = [new_val]

                    lvl_item.append(new_val)

        return nest

    def node(self):
        root = Node.from_nested(self.nested())

        def convert(node):
            if isinstance(node, Node):
                for child in node:
                    if isinstance(child, basestring) and child.find(self.separator) > -1:
                        node.replace(NodeSwitch(child.split('|')))

        root.recursive_function(convert)
        return root

    def compiled_str(self):
        for i in NodeSwitch.expand_nodes(self.node()):
            yield "".join(i.sub_family)


class Node(collections.MutableSequence):
    @property
    def index_tree(self):
        if not self.is_root():
            for i in self.parent.index_tree:
                yield i
            yield self.parent.index(self)

    @property
    def parent(self):
        return self._parent

    @property
    def root(self):
        if self.is_root():
            return self
        else:
            return self.parent.root

    @property
    def sub_family(self):
        return self.get_sub_family_object(False)

    def get_sub_family_object(self, cls):
        for child in self.elements:
            if cls is not False and isinstance(child, cls):
                yield child
            elif isinstance(child, Node):
                for i in child.get_sub_family_object(cls):
                    yield i
            else:
                yield child

    def recursive_function(self, function):
        for child in self.elements:
            if isinstance(child, Node):
                child.recursive_function(function)
        function(self)

    def copy(self):
        return copy.deepcopy(self)

    def insert(self, index, value):
        if isinstance(value, Node):
            value._parent = self
        self.elements.insert(index, value)

    def is_root(self):
        return self.parent is None

    def remove(self, value):
        self.elements.remove(value)

    def replace(self, value):
        self.parent.insert(self.parent.index(self), value)
        self.parent.remove(self)

    def __init__(self, iterable=[]):
        self._parent = None
        self.elements = []
        for value in iterable:
            self.append(value)

    def __contains__(self, value):
        return value in self.elements

    def __delitem__(self, key):
        del self.elements[key]

    def __getitem__(self, item):
        if isinstance(item, collections.Iterable):
            tup = tuple(item)
            if len(tup) > 1:
                ci, ci_args = tup[0], tup[1:]
                return self.elements[ci][ci_args]
            else:
                return self.elements[tup[0]]
        return self.elements[item]

    def __iter__(self):
        return iter(self.elements)

    def __len__(self):
        return len(self.elements)

    def __setitem__(self, key, value):
        if isinstance(value, Node):
            value._parent = self
        self.elements[key] = value

    def __str__(self):
        return '<{}:: {}>'.format(self.__class__.__name__, ', '.join([str(i) for i in self]))

    @classmethod
    def from_nested(cls, nest):
        node = Node()
        for i in nest:
            if isinstance(i, collections.Iterable) and not isinstance(i, basestring):
                node.append(cls.from_nested(i))
            else:
                node.append(i)
        return node


class NodeSwitch(Node):
    def convert(self):
        index = tuple(self.index_tree)

        for child in self:
            new_root = self.root.copy()
            old_node = new_root[index]
            old_node.replace(child)
            yield new_root

    @classmethod
    def expand_nodes(cls, node):
        def get_nodeswitch(tree):
            for child in tree.get_sub_family_object(NodeSwitch):
                if isinstance(child, NodeSwitch):
                    return child
            return None

        child1 = get_nodeswitch(node.root)
        if child1 is None:
            yield node.root
        else:
            for new_child in child1.convert():
                for i in cls.expand_nodes(new_child):
                    yield i
