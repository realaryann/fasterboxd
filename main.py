from tkinter import *
import requests
from bs4 import BeautifulSoup
from PIL import ImageTk, Image
global dfindmovieimg,dtvphoto
import time
import pickle

class Movie():
    
    def __init__(self,name):
        self.name = name
        self.similar_list = list()
    
    def insert_similar_movie(self, similar_movie):
        self.similar_list.append(similar_movie)
    
    def remove_similar(self,remove_this_movie):
        for i in range(0,len(self.similar_list)):
            if (self.similar_list[i] == remove_this_movie):
                self.similar_list.pop(i)
    
    def get_name(self):
        return self.name
    
    def get_similar(self):
        return self.similar_list
    
    def get_similar_size(self):
        return len(self.similar_list)

class Show():
    
    def __init__(self,show):
        self.name=show;
        self.similar_list = list()
    
    def insert_similar_show(self,similar_show):
        self.similar_list.append(similar_show)
    
    def remove_similar(self,remove_this_show):
        for i in range(0, len(self.similar_list)):
            if (self.similar_list[i] == remove_this_show):
                self.similar_list.pop(i)
                
    def get_name(self):
        return self.name
    
    def get_similar_size(self):
        return len(self.similar_list)
    
    def get_similar(self):
        return self.similar_list

def image_reducer(x,y, image):
    newimg = image.resize((x,y),Image.LANCZOS)
    return newimg

def check_if_show_exists(showname):
    with open("show.pickle","rb") as sfile:
        while True:
            try:
                showob = pickle.load(sfile)
                if (showob.get_name()==showname):
                    return showob
            except EOFError:
                break
        return 0
    
def check_if_movie_exists(moviename):
    with open("movie.pickle","rb") as mfile:
        while True:
            try:
                movieob = pickle.load(mfile)
                if (movieob.get_name()==moviename):
                    return movieob
            except EOFError:
                break
        return 0
    
def behindthemovie(moviename, limit,frame):
    tempobj=check_if_movie_exists(moviename)
    textlab = Text(frame,height=7,width=70,bg='grey24')
    textlab.grid(row=0,column=0)
    if(tempobj != 0):
        if (tempobj.get_similar_size() < int(limit)):
            for i in range(0,tempobj.get_similar_size()):
                textlab.insert(END, tempobj.get_similar()[i]+'\n')
            textlab.configure(font=("Segoe UI Semibold",12),state=DISABLED,fg="white")
        else:
            for i in range(0,int(limit)):
                textlab.insert(END, tempobj.get_similar()[i]+'\n')
            textlab.configure(font=("Segoe UI Semibold",12),state=DISABLED,fg="white")
    else:
        movieobj = Movie(moviename)
        correctedmovie = ''
        for i in moviename:
            if i == ' ':
                correctedmovie+='-'
            else:
                correctedmovie+=i.lower()
        url = f'https://letterboxd.com/film/{correctedmovie}/similar/'
        moviepage = requests.get(url).text
        moviesoup = BeautifulSoup(moviepage, 'html.parser')
        ul = moviesoup.find('ul',class_="poster-list -p125 -grid film-list")
        posters= ul.find_all('img')
        j=0
        recolist = []
        if (int(limit) > len(posters)):
            for i in posters:
                recolist.append(i['alt'])
                movieobj.insert_similar_movie(i['alt'])
        else:
            for i in posters:
                if (j<int(limit)):
                    recolist.append(i['alt'])
                    movieobj.insert_similar_movie(i['alt'])
                    j+=1
                else:
                    break
        with open("movie.pickle","ab") as moviefile:
            pickle.dump(movieobj,moviefile)
        for i in recolist:
            textlab.insert(END, i+'\n')
        textlab.configure(font=("Segoe UI Semibold",12),state=DISABLED,fg="white")

    
def findmovie():
    global dfindmovieimg
    moviegui = Toplevel()
    moviegui.configure(bg="gray44")
    mtopbar= LabelFrame(moviegui,bg= "gray24",padx=230,pady=50)
    mtopbar.grid(row=0,column=0)
    findmovieimg = Image.open("images\clapper.png")
    dfindmovieimg = ImageTk.PhotoImage(image_reducer(150,150,findmovieimg))
    lfindmovieimg=Label(mtopbar, image=dfindmovieimg)
    lfindmovieimg.grid(row=0,column=1)
    mhead = Label(mtopbar,text="Discover Film",padx=20,bg="gray24",fg="white")
    mhead.configure(font=("Segoe UI Semibold",30))
    mhead.grid(row=0,column=0)
    entermov=Label(moviegui,text="Enter a movie you have already seen",bg="gray24",pady=20,fg="white")
    entermov.configure(font=("Segoe UI Semibold",30))
    entermov.grid(row=1,column=0,pady=20)
    movent= Entry(moviegui,borderwidth=4, width=110)
    movent.grid(row=2,column=0)
    mmaxrec = Label(moviegui,text="Enter max number of recommendations",bg="gray24",fg="white")
    mmaxrec.configure(font=("Segoe UI Semibold",27))
    mmaxrec.grid(row=3,column=0,pady=20)
    recentry = Entry(moviegui, borderwidth=4,width=109)
    recentry.grid(row=4,column=0)
    mgetmore = Button(moviegui, text="Get More",bg="gray24",fg="white",command = lambda: behindthemovie(movent.get(), recentry.get(),textframe))
    mgetmore.configure(font=("Segoe UI Semibold",20))
    mgetmore.grid(row=5,column=0,pady=10)
    textframe = LabelFrame(moviegui, bg = "gray44")
    textframe.grid(row=6,column=0,pady=10)
    moviegui.resizable(FALSE,FALSE)

def behindthetv(show, limit,frame):
    tempsh= check_if_show_exists(show)
    tvtextlab = Text(frame,height=7,width=70,bg='grey24')
    tvtextlab.grid(row=0,column=0)
    if(tempsh != 0):
        if (tempsh.get_similar_size() < int(limit)):
            for i in range(0,tempsh.get_similar_size()):
                tvtextlab.insert(END, tempsh.get_similar()[i]+'\n')
            tvtextlab.configure(font=("Segoe UI Semibold",12),state=DISABLED,fg="white")
        else:
            for i in range(0,int(limit)):
                tvtextlab.insert(END, tempsh.get_similar()[i]+'\n')
            tvtextlab.configure(font=("Segoe UI Semibold",12),state=DISABLED,fg="white")
    else:
        showobj = Show(show)
        correctedshow = ''
        for i in show:
            if i == ' ':
                correctedshow+='_'
            else:
                correctedshow+=i.lower()
        url = f'https://www.rottentomatoes.com/tv/{correctedshow}'
        presoup = requests.get(url).text
        tvsoup = BeautifulSoup(presoup, 'html.parser')
        soup1 = tvsoup.find('tiles-carousel-responsive')
        soup2 = soup1.find_all('span')
        k = 0
        tvrecos = []
        if (int(limit) > len(soup2)):
            for i in soup2:
                tvrecos.append(i.text)
                showobj.insert_similar_show(i.text)
        else:
            for i in soup2:
                if (k < int(limit)):
                    tvrecos.append(i.text)
                    showobj.insert_similar_show(i.text)
                    k+=1
                else:
                    break
        with open("show.pickle","ab") as showfile:
            pickle.dump(showobj,showfile)
        for i in tvrecos:
            tvtextlab.insert(END, i+'\n')
        tvtextlab.configure(font=("Segoe UI Semibold",12),state=DISABLED,fg="white")

def findtv():
    global dtvphoto
    tvgui = Toplevel()
    tvgui.configure(bg="grey44")
    ttopbar= LabelFrame(tvgui,bg= "grey24",padx=244,pady=50)
    ttopbar.grid(row=0,column=0)
    tvphoto = Image.open("images/tv.png")
    dtvphoto = ImageTk.PhotoImage(image_reducer(150,150,tvphoto))
    ltvphoto = Label(ttopbar, image=dtvphoto)
    ltvphoto.grid(row=0,column=1)
    thead = Label(ttopbar,text="Discover TV",padx=20,bg="grey24",fg="white")
    thead.configure(font=("Segoe UI Semibold",30))
    thead.grid(row=0,column=0)
    entertv=Label(tvgui,text="Enter a show you have already seen",bg="grey24",fg="white",pady=20)
    entertv.configure(font=("Segoe UI Semibold",30))
    entertv.grid(row=1,column=0,pady=20)
    tovent= Entry(tvgui,borderwidth=4, width=110)
    tovent.grid(row=2,column=0)
    tmaxrec = Label(tvgui,text="Enter max number of recommendations",fg="white",bg="grey24")
    tmaxrec.configure(font=("Segoe UI Semibold",27))
    tmaxrec.grid(row=3,column=0,pady=20)
    trecentry = Entry(tvgui, borderwidth=4,width=109)
    trecentry.grid(row=4,column=0)
    tgetmore = Button(tvgui, text="Get More",fg="white",bg="grey24",command=lambda:behindthetv(tovent.get(),trecentry.get(),tvtextframe))
    tgetmore.configure(font=("Segoe UI Semibold",20))
    tgetmore.grid(row=5,column=0,pady=10) 
    tvtextframe = LabelFrame(tvgui, bg = "gray44")
    tvtextframe.grid(row=6,column=0,pady=10)
    tvgui.resizable(FALSE,FALSE)

def multilogbehind(filename, moviename):
    if (len(filename)==0):
        filen = f'uniquefile{int(time.time())}.txt'
        with open(filen,'a') as file:
            file.append(filename);
       
def multilog():
    multiloggui = Toplevel()
    multiloggui.configure(bg="gray44")
    mltopbar = LabelFrame(multiloggui,bg="gray24",padx=244,pady=50)
    header= Label(mltopbar,text="Multi-Logger",padx=20,bg="grey24",fg="white")
    header.configure(font=("Segoe UI Semibold",30))
    header.grid(row=0,column=0)
    mltopbar.grid(row=0,column=0)
    enterfile = Label(multiloggui,text="Enter Unique File Name (blank if first use)",padx=20,bg="grey24",fg="white")
    enterfile.grid(row=1,column=0,pady=10)
    enterfile.configure(font=("Segoe UI Semibold",25))
    fileentry = Entry(multiloggui,borderwidth=4,width=110)
    fileentry.grid(row=2,column=0)
    entermovie = Label(multiloggui,text="Enter Movie Name",padx=20,bg="grey24",fg="white")   
    entermovie.configure(font=("Segoe UI Semibold",25))
    entermovie.grid(row=3,column=0,pady=10)
    movielogentry = Entry(multiloggui,width=110,borderwidth=4)
    movielogentry.grid(row=4,column=0)
    logbutton =Button(multiloggui,text="Log",bg="grey24",fg="white",command=lambda: multilogbehind(fileentry.get(),movielogentry.get()))
    logbutton.configure(font=("Segoe UI Semibold",17))
    logbutton.grid(row=5,column=0,pady=10)
    
    
main = Tk()
main.title("FastrBoxd") 
main.configure(bg="gray44")
topbar = LabelFrame(main,bg="gray24",padx=200)
topbar.grid(row=0,column=0)
mainhead = Label(topbar,text="FastrBoxd",fg="white",bg="gray24")
mainhead.configure(font=("Segoe UI Semibold",40))
mainhead.grid(row=0,column=0,padx=50)
newimg = Image.open("images\clapper.png")
displaythis=ImageTk.PhotoImage(image_reducer(150,150,newimg))
imglab = Label(topbar,image=displaythis)
imglab.grid(row=0,column=1)
discmovie = LabelFrame(main,bg="gray24")
discmovie.grid(row = 1, column = 0,pady=3)
movieimg = Image.open("images\interstellar.jpg")
displayit = ImageTk.PhotoImage(image_reducer(350,120,movieimg))
movielabel = Label(discmovie,image=displayit)
movielabel.grid(row=1,column=0)
moviebutton= Button(discmovie,text="Discover Film", fg="white",bg="gray24",padx=150,command=findmovie)
moviebutton.configure(font=("Segoe UI Semibold",20))
moviebutton.grid(row=0,column=0)
discshow = LabelFrame(main, bg="gray24")
discshow.grid(row=2,column=0,pady=20)
showimg = Image.open("images/breakingbad.jpg")
displayshow=ImageTk.PhotoImage(image_reducer(350,120,showimg))
showlabel = Label(discshow,image=displayshow)
showlabel.grid(row=1,column=0)
showbutton = Button(discshow, text="Discover TV",fg="white",bg= "gray24",padx=160,command=findtv)
showbutton.configure(font=("Segoe UI Semibold",20))
showbutton.grid(row=0,column=0)
multishow = LabelFrame(main,bg="gray24")
multishow.grid(row=3, column=0)
multiimage = Image.open("images/shutterisland.jpg")
displaymulti = ImageTk.PhotoImage(image_reducer(350,85,multiimage))
multilabel = Label(multishow,image=displaymulti)
multilabel.grid(row=1,column=0)
multibutton = Button(multishow,text="Multi-Logger",padx=155,bg= "gray24",fg="white",command=multilog)
multibutton.configure(font=("Segoe UI Semibold",20))
multibutton.grid(row=0,column=0)
main.resizable(FALSE,FALSE)
main.mainloop()
