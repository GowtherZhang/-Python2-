# 第一章 Python数据模型

[[_TOC_]]

​	python 是一种面向对象语言，本书中习惯将“对象”称为“模型”（笔者更习惯成为 数据对象）。可以把 python 视为一个框架，而数据模型就是对框架的描述，规范语言自身各个组成部分的接口，确立序列、函数、迭代器、协成、类、上下文管理器等部分的行为。简单来说，我们可以从数据模型以小窥大，来看整个 python 的框架。就像使用框架要编写大量的方法义工调用，python 模型构建新类也是这样，需要构建特殊方法（魔术方法）。

# 1. 通过纸牌对象认识 python

```python
# 使用 collections.namedtuple 建立一个简单的类，这个类有两个属性rank, suit
Card = collections.namedtuple('Card', ['rank', 'suit'])

class FrenchDeck:
    ranks = [str(n) for n in range(2,11)] + list('JKQA')
    suits = 'spades diamonds clubs hearts'.split()

    def __init__(self):
        self._cards = [Card(rank, suit) for suit in self.suits for rank in self.ranks]
    
    def __len__(self):
        return len(self._cards)
    
    def __getitem__(self, position):
        return self._cards[position]
   
deck = FrenchDeck()
```

这里建立了一个 FrenchDeck 类，与标准的 python 容器一样，我们可以通过这个模拟序列来观察 python 对象的一些基本方法：

1.  长度

 FrenchDeck 能够响应 len() 函数返回一摞牌有多少张，即 len(deck)

2. 特殊方法

   这里的 getitem 就是我们的特殊方法，也叫魔法方法。可以利用 getitem 方法从这摞牌中抽取一张，比如 deck[0]、deck[-1]、choice(deck)等。

可以看到利用特殊方法利用 python 数据模型有两个优点（对于暂时还没有 python 特性的笔者来说，或者说特点）：

* 类的用户不需要记住标准操作的方法名称，比如 对象.size()，对象.length() 或者其他方法
* 重复利用 python 的标准库，比如 random.choice() 函数

对于这么一个对象，除了基本的迭代外，我们也是可以进行自定义的排序。

3. 切片与迭代

   由于 FrenchDeck() 这个类中的方法 \__getitem__ 实际上就是利用了 [] 运算符，那这个对象自然也就可以实现切片和迭代，如：

   ```python
   # 切片
   deck[-3] # 前三张牌
   deck[12::13] # 从第12位开始，每隔13张取一张，最后是4张A
   
   # 反向迭代
   for i in reversed(deck):
       print(i)
   ```

4. 包含(contains)

   由于本例中没有实现 \__contains__ 方法，但本身是可迭代的，那么 in 运算符，就会做一次顺序扫描，当输入 Card('2', 'hearts') in deck 时，会返回布尔值 True.

5. 排序

   我们可以通过给花色赋值，将纸牌按照指定的顺序进行排序，脚本如下：

   ```python
   suit_values = dic(spades=3, hearts=2, diamonds=1, clubs=0)
   
   def spades_high(card):
       rank_value=  FrenchDeck.ranks.index(card.rank)
       return rank_value * len(suit_values) + suit_values[card.suit]
   
   for card in sorted(deck, key=spades_high):
       print(card)
   ```

通过以上示例可以看出，FrenchDeck 的行为就像 python 标准序列一样，受益于语言的核心特性与标准库。就像 \__len__ 和 \__getitem__ 的实现，就是把所有工作委托给一个 List 对象。

# 2. 特殊方法的调用

特殊方法的是供 python 解释器调用的， 而不是你自己。比如我们很少会写 object.\_\_len\_\___() 这种特殊方法，而是写为 len(object)， 除非说这个 object 是你自己写的类的实例，才会调用你自己写的实现方法 \_\_len\_\_。

在处理内置的数据类型（如 list、str、Numpy 数据等）中，python 底层的 C 语言实现中有一个字段 ob_size 会保存着这个对象的长度，python 解释器会利用 len(object) 直接读取这个数值，比调用方法快的多。

特殊方法一般都是隐式调用的，比如 for i in x: 语句其实背后就是在调用 iter(x)，不会直接调用。唯一的例外是 \_\_init\_\_方法，会为自定义的类调取超类初始化时而使用。

特殊方法最重要的用途分为以下几种，这里仅举例，因为一般不太会用到，后期有机会再具体说明：

* 模拟数值类型
* 对象的字符串表示形式
* 对象的布尔值
* 实现容器