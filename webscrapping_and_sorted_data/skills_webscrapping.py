import sys
from bs4 import BeautifulSoup
import aiohttp
import requests
import asyncio
import math
import re
import time


class Node:
    def __init__(self, my_list):
        self.__entry = my_list
        self.__next = None
        self.__pervious = None

    def get_data(self):
        return self.__entry

    def set_next(self, new_next):
        self.__next = new_next

    def set_pervious(self, new_pervious):
        self.__pervious = new_pervious

    def get_next(self):
        return self.__next

    def get_pervious(self):
        return self.__pervious


class LinkedList:
    def __init__(self):
        self.head = None
        self.current = None
        self.currentpos = 0
        self.size = 0

    def insert(self, my_list, pos):
        temp = Node(my_list)
        if(pos == 0):
            temp.set_next(self.head)
            self.head = temp
            self.current = self.head
        else:
            if pos <= self.currentpos:
                while(self.currentpos != pos-1):
                    self.currentpos -= 1
                    self.current = self.current.get_pervious()
            else:
                while(self.currentpos != pos-1):
                    self.currentpos += 1
                    self.current = self.current.get_next()
            if pos == self.size:
                temp.set_next(self.head)
                self.head.set_pervious(temp)
            else:
                temp.set_next(self.current.get_next())
            self.current.set_next(temp)
            temp.set_pervious(self.current)
        self.size += 1

    def RetriveList(self, pos):
        if pos == 0:
            self.current = self.head
            self.currentpos = 0
            return self.head.get_data()
        else:
            if pos < self.currentpos:
                if(self.currentpos - pos) > (self.size - self.currentpos + pos):
                    self.move_next(pos)
                else:
                    self.move_pervious(pos)
            else:
                if(pos - self.currentpos) > (self.size - pos + self.currentpos):
                    self.move_next(pos)
                else:
                    self.move_pervious(pos)

            return self.current.get_data()

    def move_next(self, pos):
        while(self.currentpos != pos):
            self.currentpos = (self.currentpos + 1) % self.size
            self.current = self.current.get_next()
            # print(f"--->>>{self.currentpos}......{self.current.get_data()}")

    def move_pervious(self, pos):
        while(self.currentpos != pos):
            self.currentpos = (self.currentpos - 1) % self.size
            self.current = self.current.get_pervious()
            # print(f"--->>>{self.currentpos}......{self.current.get_data()}")

    def delete(self, pos):
        if(pos == 0):
            self.current = self.head.get_next()
            self.head = self.current
            self.currentpos = 0
            self.current.set_pervious(None)
        else:
            if pos <= self.currentpos:
                while(self.currentpos != pos-1):
                    self.currentpos -= 1
                    self.current = self.current.get_pervious()
            else:
                while(self.currentpos != pos-1):
                    self.currentpos += 1
                    self.current = self.current.get_next()
            temp = self.current.get_next().get_next()
            if(temp):
                self.current.set_next(temp)
                temp.set_pervious(self.current)
            else:
                self.current.set_next(self.head)
                self.head.set_pervious(self.current)
        self.size -= 1


class QuickSort:
    def quicksort(self, my_list):
        if len(my_list) <= 1:
            return my_list
        piviot = 0
        while(my_list[piviot] == None):
            piviot += 1

        left = [x for x in my_list[piviot+1:] if x !=
                None and x.getfrequency() < my_list[piviot].getfrequency()]
        right = [x for x in my_list[piviot+1:] if x !=
                 None and x.getfrequency() >= my_list[piviot].getfrequency()]

        return self.quicksort(right) + [my_list[piviot]] + self.quicksort(left)


class Skill_object:
    def __init__(self, string):
        self.__name = string
        self.__frequency = 1
        self.__list_of_frequency = []

    def getname(self):
        return self.__name

    def setname(self, new_name):
        self.__name = new_name

    def getfrequency(self):
        return self.__frequency

    def setfrequency(self, new_frequency):
        self.__frequency = new_frequency

    def get_list_of_frequency(self):
        return self.__list_of_frequency

    def append_list_of_frequency(self, new_list):
        self.__list_of_frequency.append(new_list)

# -----------------------------------------


class ReteiveItems_attached:
    def get_items_attached_with_skill(self, string):
        timeq = time.time()
        items_hash_table = HashTable_s()
        list1 = self.search(string).get_list_of_frequency()
        for l in list1:
            list_n = self.linked_list.RetriveList(l)
            items_hash_table.push(list_n)
        items_hash_table.data = self.q.quicksort(items_hash_table.data)
        print(f"quick sort : {(time.time()-timeq):.4f}")
        # dict_sort = {i.getname(): i.getfrequency()
        #              for i in items_hash_table.data}

        # return dict_sort
        return items_hash_table


class Traverse:
    def traverse(self):
        for i in self.data:
            if i == None:
                continue
            else:
                print(i.getname(), i.getfrequency())


class Sort:
    def sort(self):
        self.q = QuickSort()
        # timeq = time.time()
        self.sorted_data = self.q.quicksort(self.data)
        # print(f"quick sort : {(time.time()-timeq):.4f}")
        return self.sorted_data


class Search:
    def search(self, string):
        index = self.hash(string)
        position = index
        while self.data[position] != None:
            if self.data[position].getname() == string:
                return self.data[position]
            else:
                position = self.rehash(position)
                if(position == index):
                    return None
            print(position)
            print(self.data[position])
        return None


class HashTable_s(Search, Sort, Traverse, ReteiveItems_attached):
    def __init__(self):
        # self.size = (data_webscarp.numberOfLinks)*150*1.5
        self.size = 500
        self.data = [None]*self.size
        self.uniqueskills = 0
        self.num_push = -1

    def push(self, my_list):
        self.num_push += 1
        for s in range(len(my_list)):
            index = self.hash(my_list[s])

            if self.data[index] == None:
                obj = Skill_object(my_list[s])
                self.data[index] = obj
                self.data[index].append_list_of_frequency(self.num_push)
                self.uniqueskills += 1

            elif (self.data[index] != None):
                if self.data[index].getname() == my_list[s]:
                    self.data[index].setfrequency(
                        self.data[index].getfrequency()+1)
                    self.data[index].append_list_of_frequency(self.num_push)
                else:
                    new_index = self.rehash(index)
                    while(self.data[new_index] != None and self.data[new_index].getname() != my_list[s]):
                        new_index = self.rehash(new_index)

                    if self.data[new_index] == None:
                        obj = Skill_object(my_list[s])
                        self.data[new_index] = obj
                        self.uniqueskills += 1
                    else:
                        self.data[new_index].setfrequency(
                            self.data[new_index].getfrequency()+1)

                    self.data[new_index].append_list_of_frequency(
                        self.num_push)

    def hash(self, string):
        number_ofstring = 0
        for i in range(len(string)):
            number_ofstring += ord(string[i])*(i+1)
        return number_ofstring % self.size

    def rehash(self, number):
        return (number + 1) % self.size


class HashTable_L(HashTable_s):
    def __init__(self):
        super().__init__()
        self.linked_list = LinkedList()
        self.q = QuickSort()

    def push(self, my_list):
        super().push(my_list)
        self.linked_list.insert(my_list, self.linked_list.size)


# -----------------------------------------


class Data_web_scraping:
    nums = 0
    all_skills = {}
    numberOfLinks = 0

    def __init__(self, hushTable):
        self.hash_table = hushTable
        self.n = 0
        self.time = 0

    def get_num_links(self, url):
        src = requests.get(url)
        soup = BeautifulSoup(src.text, 'lxml')
        skills = (soup.select_one("strong")).text

        self.numberOfLinks = math.ceil(int(skills)/15)
        print(math.ceil(int(skills)/15))
        return math.ceil(int(skills)/15)
# Use CSS selectors instead of find_all method: Selecting elements with CSS selectors is generally faster than using the find_all method
# Use list comprehension instead of for loop: List comprehension is generally faster than using a for loop.

    async def get_response(self, url):
        print(url)
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    src = await response.text()
                time1 = time.time()
                self.n += 1
                print(f"-----------{self.n}")

                soup = BeautifulSoup(src, 'lxml')
                all_skills = soup.select(".css-y4udm8 div:nth-of-type(2)")
                for skills in all_skills:
                    s = [re.sub(r'·', '', i.text).strip().lower()
                         for i in skills.select("a")]
                    self.hash_table.push(s)
                print(f"{(time.time()-time1):.3f} .")
                self.time += time.time()-time1
        except Exception as e:
            print(f"Error in webscrap(): {e}")

    async def main(self, jop_name):
        time1 = time.time()
        url = f"https://wuzzuf.net/search/jobs/?a=hpb&q={jop_name}&start="
        num_links = self.get_num_links(url)
        # num_links = 1

        # tasks = []
        # for i in range(num_links):
        #     tasks.append(asyncio.create_task(self.get_response(f"{url}{i}")))
        # result = await asyncio.gather(*tasks)

        tasks = [asyncio.create_task(self.get_response(
            f"{url}{i}")) for i in range(num_links)]
        await asyncio.gather(*tasks)

        print(f"===>>>{self.time}")

        print(self.hash_table.num_push)
        print(self.hash_table.uniqueskills)

        # items = self.hash_table.get_items_attached_with_skill("python")
        # print(items.traverse())

        # print(time.time()-time1)


time1 = time.time()


def query_data(skill):
    h = HashTable_L()

    data_webscarp = Data_web_scraping(h)
    while True:
        try:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(data_webscarp.main(skill))
        except RuntimeError as e:
            if 'Event loop is closed' in str(e):
                continue
            else:
                raise
        else:
            break

    return h


# h = (query_data("backend"))
# h.sort()
# print(time.time()-time1)


# print(h.sort())
# x = h.sort()
# for i in range(20):
#     print(i, x[i].getname(), x[i].getfrequency())
# h.get_items_attached_with_skill("bootstrap").traverse()
# h.get_items_attached_with_skill("react").traverse()
# h.get_items_attached_with_skill("angular").traverse()
# h.get_items_attached_with_skill("vue.js").traverse()


# list1 = ['apython', 'mysql', 'sql', 'java script', 'experinced 3:5 years',
#          'software development', 'docker', 'html', 'bootstrap', 'css']
# for i in range(100):
#     h.push(list1)

#     h.push(['java script', 'experinced 3:5 years',
#             'software development', 'docker', 'html', 'bootstrap', 'css', 'python'])

#     h.push(['python', 'mysql', 'sql' 'java ', 'experinced 3:5 years',
#             'software development', 'docker', 'html', 'bootstrap', 'docker'])

#     h.push(['zpython', 'mysql', 'sql', 'java script', 'experinced 3:5 years',
#             'software development', 'docker', 'html', 'bootstrap', 'css', 'python'])

# print(h.uniqueskills)
# print(h.traverse())

# print("="*50)
# print(h.linked_list.head.get_pervious().get_data())
# print("="*50)

# items = h.get_items_attached_with_skill("sql")
# print(items.traverse())
# print(items.uniqueskills)
# print(h.num_push)

# print("*"*100)
# x = h.sort()
# for i in x:
#     print(i.getname(), i.getfrequency())


# print(f"{(time.time()-time1):.3f}")


def query_data2(skill):
    time1 = time.time()
    h = HashTable_L()
    list1 = ['apython', 'mysql', 'sql', 'java script', 'experinced 3:5 years',
             'software development', 'docker', 'html', 'bootstrap', 'css']
    for i in range(100):
        h.push(list1)

        h.push(['java script', 'experinced 3:5 years',
                'software development', 'docker', 'html', 'bootstrap', 'css', 'python'])

        h.push(['python', 'mysql', 'sql' 'java ', 'experinced 3:5 years',
                'software development', 'docker', 'html', 'bootstrap', 'docker'])

        h.push(['zpython', 'mysql', 'sql', 'java script', 'experinced 3:5 years',
                'software development', 'docker', 'html', 'bootstrap', 'css', 'python'])
    print(h.uniqueskills)
    print("="*50)
    print(h.linked_list.head.get_pervious().get_data())
    print("="*50)

    items = h.get_items_attached_with_skill(skill)
    print(items)

    print(f"{(time.time()-time1):.3f}")
    return h


# b = (query_data("sql"))
# for i in b:
#     print(i.getname())
