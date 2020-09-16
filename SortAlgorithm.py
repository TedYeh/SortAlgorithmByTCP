import argparse, socket, pickle, random
import time
from bs4 import BeautifulSoup
import requests
from tkinter import *
from tkinter import ttk
import threading

#顯示各種排序在維基的資訊
t = [None]*6
t[0]= BeautifulSoup(requests.get("https://en.wikipedia.org/wiki/Bubble_sort").text,"html.parser").p.text
t[1]= BeautifulSoup(requests.get("https://en.wikipedia.org/wiki/Selection_sort").text,"html.parser").p.text
t[2]= BeautifulSoup(requests.get("https://en.wikipedia.org/wiki/Insertion_sort").text,"html.parser").p.text
t[3]= BeautifulSoup(requests.get("https://zh.wikipedia.org/wiki/%E5%BF%AB%E9%80%9F%E6%8E%92%E5%BA%8F").text,"html.parser").p.text.replace('\n','')
t[4]= BeautifulSoup(requests.get("https://zh.wikipedia.org/wiki/%E5%A0%86%E6%8E%92%E5%BA%8F").text,"html.parser").p.text.replace('\n','')
t[5]= BeautifulSoup(requests.get("https://en.wikipedia.org/wiki/Radix_sort").text,"html.parser").p.text
sort = {"bubbleSort":t[0],"selectionSort":t[1],"insertionSort":t[2],"quickSort":t[3],"heapSort":t[4],"radixSort":t[5]}



class Client:
    def __init__(self,host,port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))
        self.client()
        self.min_idx = 0
        self.sort_type = ["bubbleSort","selectionSort","insertionSort","quickSort","heapSort","radixSort"]#"mergeSort",
        self.bgcolor = "#ADD8E6"
        
        self.root = Tk()
        self.root.title("Sort Algorithm")
        
        self.f1 = LabelFrame(self.root,text="結果畫面",relief=SOLID,background = self.bgcolor)
        self.f2 = LabelFrame(self.root,text="選項＆介紹",relief=SOLID,background = self.bgcolor)
        
        self.canvas = Canvas(self.f1,width = 580,height = 540,background = self.bgcolor)
        self.canvas.pack(pady=5,padx=5)
        
        self.f1.grid(row = 0,column = 0,pady=5,padx=5)
        
        self.lb = Listbox(self.f2,width=23,font="Arial")
        
        for i in self.sort_type:
            self.lb.insert(END,i)
        self.lb.pack(padx=5)
        self.lb.bind("<<ListboxSelect>>",self.itemSelect)
        
        self.f2.grid(row = 0,column = 1)
        
        self.intro = Text(self.f2,width=23,height=18,font="Arial",wrap=WORD)
        self.intro.pack(pady=5)
        self.intro.insert(END,"Please select the sort algorithm. We will show the algorithm and introduction to you.")
        
        self.root.configure(background = self.bgcolor)
        self.root.mainloop()    
        
    def drawData(self,arr):
        x0,y0,width = 4,520,4
        n = len(arr)
        self.canvas.delete(ALL)    
        for i in range(n):
            self.canvas.create_rectangle(x0*(i+1),y0,(x0*(i+1))+width,y0-(arr[i]*3.7),fill='black',outline='white')
        self.root.update()
    
    def showPos(self,arr,now):
        x0,y0,width = 4,520,4
        self.canvas.create_rectangle(x0*(now+1),y0,(x0*(now+1))+width,y0-(arr[now]*3.7),fill='red',outline='white')
        self.root.update()
        time.sleep(0.001)   
    
    def client(self):
        reply = self.sock.recv(65536)
        data = pickle.loads(reply)
        
    def itemSelect(self,event):
        self.intro.delete('1.0',END)
        arr = [i for i in range(1,141)]
        random.shuffle(arr)
        print(arr)
        obj = event.widget
        index = obj.curselection()
        if(obj.get(index) == "bubbleSort"):
            self.intro.insert(END,str(t[0]))
            self.intro.config(state=DISABLED)
            self.bubbleSort(arr)
        elif(obj.get(index) == "selectionSort"):
            self.intro.insert(END,str(t[1]))
            self.intro.config(state=DISABLED)
            self.selectionSort(arr)
        elif(obj.get(index) == "insertionSort"):
            self.intro.insert(END,str(t[2]))
            self.intro.config(state=DISABLED)
            self.insertionSort(arr)
        elif(obj.get(index) == "quickSort"):
            self.intro.insert(END,str(t[3]))
            self.intro.config(state=DISABLED)
            self.quickSort(arr,0,len(arr)-1)
        elif(obj.get(index) == "heapSort"):
            self.intro.insert(END,str(t[4]))
            self.intro.config(state=DISABLED)
            self.heapSort(arr)
        elif(obj.get(index) == "radixSort"):
            self.intro.insert(END,str(t[5]))
            self.intro.config(state=DISABLED)
            self.radixSort(arr)
        self.intro.config(state=NORMAL)
        
    def bubbleSort(self,arr):
        n = len(arr) 
        self.drawData(arr) 
        for i in range(n):        
            for j in range(0, n-i-1):
                if arr[j] > arr[j+1] :
                    arr[j], arr[j+1] = arr[j+1], arr[j]  
                self.showPos(arr,j)
                self.drawData(arr) 
                data=pickle.dumps(arr)
                self.sock.send(data)
        self.sock.send(pickle.dumps([-1]))

    def selectionSort(self,arr):
        self.drawData(arr)
        for i in range(len(arr)):         
            for j in range(i+1, len(arr)): 
                if arr[self.min_idx] > arr[j]: 
                    self.min_idx = j 
                    self.showPos(arr,j)
            arr[i],arr[self.min_idx] = arr[self.min_idx], arr[i] 
            self.drawData(arr)
            data=pickle.dumps(arr)
            self.sock.send(data)
        
    def insertionSort(self,arr): 
        self.drawData(arr)
        for i in range(1, len(arr)): 
            key = arr[i] 
            j = i-1
            while j >=0 and key < arr[j] : 
                    arr[j+1] = arr[j]
                    j -= 1
            self.showPos(arr,j)
            arr[j+1] = key 
            self.drawData(arr)
            data=pickle.dumps(arr)
            self.sock.send(data)
            
    def partition(self,arr,low,high):
        n = len(arr)
        i = ( low-1 )         
        pivot = arr[high]
        
        self.drawData(arr)
        
        for j in range(low , high): 
            if   arr[j] <= pivot: 
                i = i+1 
                arr[i],arr[j] = arr[j],arr[i] 
      
        arr[i+1],arr[high] = arr[high],arr[i+1] 
        
        self.drawData(arr)
        data=pickle.dumps(arr)
        self.sock.send(data)
        return ( i+1 ) 

    def quickSort(self,arr,low,high): 
            if low < high: 
                pi = self.partition(arr,low,high) 
                self.showPos(arr,pi)
                self.quickSort(arr, low, pi-1) 
                self.quickSort(arr, pi+1, high) 
    
    def heapify(self,arr, n, i): 
        largest = i
        l = 2 * i + 1    
        r = 2 * i + 2     
      
        if l < n and arr[i] < arr[l]: 
            largest = l 
      
        if r < n and arr[largest] < arr[r]: 
            largest = r 
      
        
        if largest != i: 
            arr[i],arr[largest] = arr[largest],arr[i] 
            self.heapify(arr, n, largest)
            
    def heapSort(self,arr): 
            n = len(arr) 
            # Build a maxheap. 
            for i in range(n, -1, -1): 
                self.heapify(arr, n, i) 
            self.drawData(arr)
            for i in range(n-1, 0, -1): 
                arr[i], arr[0] = arr[0], arr[i] 
                self.showPos(arr,i)
                self.drawData(arr)
                data=pickle.dumps(arr)
                self.sock.send(data)
                self.heapify(arr, i, 0)
                
    def countingSort(self,arr, exp1): 
            n = len(arr)  
            output = [0] * (n) 
            count = [0] * (10) 
          
            for i in range(0, n): 
                index = int(arr[i]/exp1) 
                count[ (index)%10 ] += 1
            for i in range(1,10): 
                count[i] += count[i-1] 
            i = n-1
            while i>=0: 
                index = int(arr[i]/exp1) 
                output[ count[ (index)%10 ] - 1] = arr[i] 
                count[ (index)%10 ] -= 1
                i -= 1
          
            i = 0
            for i in range(0,len(arr)): 
                arr[i] = output[i] 
                self.showPos(arr,i)
                self.drawData(arr)
                data=pickle.dumps(arr)
                self.sock.send(data)
            
    def radixSort(self,arr): 
            max1 = max(arr) 
            self.drawData(arr)
            exp = 1
            while int(max1/exp) > 0: 
                self.countingSort(arr,exp)
                exp *= 10    

class Server:
    def __init__(self,host,port):
        self.stop = False
        self.listeningSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listeningSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.listeningSock.bind((host,port))
        self.listeningSock.listen(1)
        self.sock, self.sockname = self.listeningSock.accept()
        self.orgin = self.sendarr()
        self.root = Tk()
        self.root.title('Server')
        self.root.geometry("250x600")
        self.tree = ttk.Treeview(self.root,columns=["data1","data2","data3","data4","data5"],show='headings')
        for i in range(5):
            self.tree.column("data%d"%(i+1), width=50, anchor='center') 
            
        for i in range(5):
            self.tree.heading("data%d"%(i+1), text="data%d"%(i+1))
            
        self.tree.pack(side=LEFT,fill=BOTH)
        
        t = threading.Timer(2, self.server)
        t.start()
        
        self.root.mainloop()
    
    def sendarr(self):
        arr = [i for i in range(1,141)]
        a = arr
        random.shuffle(arr)
        data=pickle.dumps(arr)
        self.sock.send(data)
        return a
        
    def server(self):
        try:
            while True:
                reply = self.sock.recv(65536)
                data = pickle.loads(reply)
                for i in range(28):
                    self.tree.insert('',i,values=(data[i],data[i+28],data[i+56],data[i+84],data[i+112]))
                self.root.update()
                time.sleep(0.1)
                if not(data == self.orgin):
                    x=self.tree.get_children()
                    for item in x:
                        self.tree.delete(item)
            self.root.update()
        except EOFError:
            for i in range(0,28):
                self.tree.insert('',i,values=(data[i],data[i+28],data[i+56],data[i+84],data[i+112]))
            self.root.update() 
            
            

if __name__ == '__main__':
    choices = {'client': Client, 'server': Server}
    parser = argparse.ArgumentParser(description='Send and receive over TCP')
    parser.add_argument('role', choices=choices, help='which role to play')
    parser.add_argument('host', help='interface the server listens at;'
                        ' host the client sends to')
    parser.add_argument('-p', metavar='PORT', type=int, default=1060,
                        help='TCP port (default 1060)')
    args = parser.parse_args()
    function = choices[args.role]
    function(args.host, args.p)