import random

def step_move_one_by_one(length, array):
    while length>0:
        length-=1
        array=array[1:] + array[:1]
    return array

def step_firstN_to_middle(firstN, array):
    if firstN < 0 or firstN > len(array):
        return "Error: firstN is out of range"    
    firstN_items = array[:firstN] # 移除前N项
    remaining_array = array[firstN:]
    if len(remaining_array) > 0: # 计算中间随机位置，这里的中间是指从1到剩余数组的长度之间的任意位置
        random_position = random.randint(1, len(remaining_array) - 1)
    else: # 如果移除后列表为空，则只能将元素放回原位
        random_position = 0
    array = remaining_array[:random_position] + firstN_items + remaining_array[random_position:] # 在随机位置插入之前移除的N项
    return array

def trier():
    array=["A","B","C","D"]
    random.shuffle(array)
    print(f"1. 打乱列表：{array}")
    array+=array
    print(f"2. 把列表复制成两份并拼接在一起：{array}")
    array=step_move_one_by_one(random.randint(2,99),array)
    print(f"3. 根据名字依次移动N项到末尾：{array}")
    array=step_firstN_to_middle(3, array)
    print(f"4. 取前3张卡片插入中间随机位置：{array}")
    star=array[0]; array=array[1:]
    print(f"5. 取出星星值：{star}，剩余的列表：{array}")
    array=step_firstN_to_middle(random.randint(1,3), array)#南方人1，北方人2，不确定3
    print(f"6. 取前N(1-3)张卡片插入中间随机位置：{array}")
    array=array[random.randint(1,2):]#男1，女2，加入即使有更多性别的情况下会出现问题，最多丢弃6张，在这一步之前，目标值每次都在列表最后一项
    print(f"7. 丢弃前N(1-2)张卡片后：{array}")
    #array=step_move_one_by_one(len("见证奇迹的时刻"),array)
    array=step_move_one_by_one(7,array)
    print(f"8. 依次移动首张到末张，重复7次后：{array}")
    while len(array)>1:
        array=array[1:] + array[:1]; print(f"9. 好运留下来：{array}")
        array.pop(0); print(f"9. 烦恼丢出去：{array}")
    print(f"10. 结果：之前存的牌：{star}, 现在剩的牌：{array[0]}")

trier()

"""
GPT的分析


### 关键点分析

1. **复制并拼接列表**：这步简单地将列表复制并拼接到自身的末尾，使其长度翻倍，但不改变元素的相对顺序。

2. **依次移动N项到末尾（`step_move_one_by_one`函数）**：这个函数通过循环，每次将第一个元素移动到列表的末尾。
    如果移动次数等于列表的长度，那么列表将恢复到原始状态。移动的次数如果是列表长度的整数倍，同样会恢复到原始状态。
    因此，这个操作不影响`star`和`array[0]`最终相等的结果，因为它只是改变了元素的位置，没有改变它们的相对顺序。

3. **取前N张卡片插入到中间随机位置**：不论这些元素插入到什么位置，它们的相对顺序保持不变。
    所以，尽管这改变了元素的绝对位置，但由于列表最终将只剩下一个元素，这个操作不直接影响最终结果。

4. **丢弃前N张卡片后的操作**、**依次移动首张到末张，重复7次后**、以及后续的**好运留下来**和**烦恼丢出去**操作，
    都是在不断地减少列表的长度，但这些操作不会改变最后留下来元素（即最初的`array[0]`）是谁的事实。

### 最终结果为什么相同

- 无论经过多少次的移动和删除，只要这些操作保持了列表中剩余元素的相对顺序不变（即没有通过某些操作交换任意两个元素的位置），
    最终留下的元素总是最开始的`array[0]`。
- 在最后的操作中，列表被缩减到只剩下一个元素。由于所有操作都没有改变元素的相对顺序，最后留下的元素必然是开始时的`array[0]`。
- `star`变量在步骤5被设置为这个初始的`array[0]`，因此在最后，`star`和列表中剩下的唯一元素相等。

这种结果的根本原因在于操作的性质：虽然改变了元素的位置，但没有改变它们的相对序列，特别是在不断删除元素的操作中，
    最终结果的确定性是由最初的`array[0]`元素的稳定位置决定的。
"""