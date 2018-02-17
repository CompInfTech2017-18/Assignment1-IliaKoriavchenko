import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import matplotlib.lines as lines

    
class ploter:    
    def __init__(self):
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)
        
    def plot(self, x, y, colour):
        return self.ax.plot(x, y, colour)
    
    def show(self):
        plt.show()
        
        
class tt:
    def __init__(self, m, Vx, Vy, g, plot, colour):
        self.Vx = Vx
        self.Vy = Vy
        self.mass = m
        self.gforce = g
        self.plot = plot
        self.colour = colour
       
    def getX(self, t):
        return self.Vx*t
    
    def getY(self, t):
        return self.Vy*t - self.gforce*t**2/(2.0*self.mass)
    
    def position(self):
        t = np.linspace(0, 10, 20)
        x = self.getX(t)
        y = self.getY(t)
        plot.plot(x,y,'black')
    
    
class rotate(tt):
    def __init__(self, m, Vx, Vy, g, plot, colour, r, phi, w):
        tt.__init__(self, m, Vx, Vy, g, plot, colour)
        self.rad = r
        self.angl = phi
        self.rotw = w

    def getXrot(self, t, n):
        return self.getX(t) + ((-1)**n)*self.rad*np.cos(t*self.rotw+self.angl)
    
    def getYrot(self, t, n):
        return self.getY(t) + ((-1)**n)*self.rad*np.sin(t*self.rotw+self.angl)
    
    def position_rot(self):      
        t = np.linspace(0, 10, 20)
        x1 = self.getXrot(t,0)
        y1 = self.getYrot(t,0)
        
        l1 = plot.plot(x1,y1,'ro')
        plt.setp(l1, markersize=10)
        plt.setp(l1, markerfacecolor='r')
        plt.setp(l1, markeredgecolor='r')
        
        x2 = self.getXrot(t,1)
        y2 = self.getYrot(t,1)
        
        l2 = plot.plot(x2,y2,'ro')
        plt.setp(l2, markersize=10)
        plt.setp(l2, markerfacecolor='g')
        plt.setp(l2, markeredgecolor='g')
        
        for i in range(0,20):
            l3 = lines.Line2D([x1[i],x2[i]], [y1[i],y2[i]],  lw=2, color='black')
            plot.ax.add_line(l3)
        
plot = ploter()

rot = rotate(1.0, 1.5, 1.0, 0.5, plot, 'g', 1.0, 1.0, 0.5) 
rot.position()
rot.position_rot()

class EMrotate(rotate):
    def __init__(self, m, Vx, Vy, g, plot, colour, r, phi, w, q, E):
        rotate.__init__(self, m, Vx, Vy, g, plot, colour, r, phi, w)
        self.q = q
        self.E = E
        
    def getXEM(self, t, n, omega):
        return self.getX(t) + ((-1)**n)*self.rad*np.cos(omega)
    
    def getYEM(self, t, n, omega):
        return self.getY(t) + ((-1)**n)*self.rad*np.sin(omega)
        
    def position_EM(self):
        t = np.linspace(0, 10, 20)
        def func(y,t):
            phi, w = y
            return [w, (self.mass*self.rad)/(self.q*self.E)*np.sin(w)]
        omega = odeint(func,[0,self.rotw],t)[:,0]
        
        t = np.linspace(0,10,20)
        x1 = self.getXEM(t,0,omega)
        y1 = self.getYEM(t,0,omega)
        l1 = plot.plot(x1,y1,'ro')
        plt.setp(l1, markersize=10)
        plt.setp(l1, markerfacecolor='r')
        plt.setp(l1, markeredgecolor='r')
            
        x2 = self.getXEM(t,1,omega)
        y2 = self.getYEM(t,1,omega)
        l2 = plot.plot(x2,y2,'ro')
        plt.setp(l2, markersize=10)
        plt.setp(l2, markerfacecolor='g')
        plt.setp(l2, markeredgecolor='g')
        #plt.xlim((140,175))
        #plt.ylim((-2500,-2300))
        
        for i in range(0,20):
            l3 = lines.Line2D([x1[i],x2[i]], [y1[i],y2[i]], lw=2, color='black')
            plot.ax.add_line(l3)
        
plot = ploter()

rot1 = EMrotate(1.0, 1.5, 1.0, 0.5, plot, 'g', 1.0, 1.0, 0.1, 1.0, 1.0)
rot1.position_EM()