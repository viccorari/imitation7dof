from visual import *
import numpy as np
import math

def distancia_euclides (a,b):
    return math.sqrt(math.pow(a.x-b.x,2)+math.pow(a.y-b.y,2)+math.pow(a.z-b.z,2)) 

def rotacion_eje (v,o,t):
    m = np.matrix([
        [np.cos(t)+((v.x**2)*(1-np.cos(t))),
         (v.x*v.y*(1-np.cos(t)))-(v.z*np.sin(t)),
         (v.x*v.z*(1-np.cos(t)))+(v.y*np.sin(t))],
        [(v.y*v.x*(1-np.cos(t)))+(v.z*np.sin(t)),
         np.cos(t)+((v.y**2)*(1-np.cos(t))),
         (v.y*v.z*(1-np.cos(t)))-(v.x*np.sin(t))],
        [(v.z*v.x*(1-np.cos(t)))-(v.y*np.sin(t)),
         (v.z*v.y*(1-np.cos(t)))+(v.x*np.sin(t)),
         np.cos(t)+((v.z**2)*(1-np.cos(t)))]
        ])
    origen = np.matrix([[o.x],[o.y],[o.z]])
    r = m*origen
    return vector(r[0,0],r[1,0],r[2,0])

class o_direccion:
    def __init__(self,a,l,ancho):
        self.origen = vector(a)
        self.longitud = l
        self.a = ancho
        self.px = arrow(pos=self.origen,axis=vector(l,0,0),shaftwidth=ancho,color=color.green)
        self.py = arrow(pos=self.origen,axis=vector(0,l,0),shaftwidth=ancho,color=color.red)
        self.pz = arrow(pos=self.origen,axis=vector(0,0,l),shaftwidth=ancho,color=color.blue)
        self.o  = sphere(pos=self.origen,color=color.orange,radius=ancho)

class segmento:
    def __init__(self,a,b,d,_ancho,textura):
        direccion = norm(vector(b)-vector(a))
        distancia = distancia_euclides(a,b)
        self.ancho = _ancho
        self.obj = box( pos=a+(direccion*(distancia/2)), 
                        axis=direccion, 
                        up=d, 
                        width=self.ancho, 
                        height=self.ancho, 
                        length=distancia, 
                        color=textura)
        self.c1 = sphere(pos=a,radius=(self.ancho*1.75),color=color.green)
        self.c2 = sphere(pos=b,radius=(self.ancho*1.75),color=color.green)

    def actualizar(self,a,b,d):
        direccion = norm(vector(b)-vector(a))
        distancia = distancia_euclides(a,b)
        self.obj.pos=a+(direccion*(distancia/2))
        self.obj.axis = direccion
        self.obj.up=d
        self.obj.length=distancia
        self.c1.pos=a
        self.c1.radius=(self.ancho*1.75)
        self.c2.pos=b
        self.c2.radius=(self.ancho*1.75)

class escenario:
    def __init__ (self,dis,_title,ancho,largo):
        self.title = _title
        self.width = ancho
        self.height= largo
        dis.title=_title
        dis.width=ancho
        dis.height=largo
        dis.autocenter=True
        dis.autoscale=True
        dis.background=(1,1,1)
        userzoom=True

class circulo:
    def __init__ (self,_p,_d,_r,_grosor,_color):
        self.p = _p
        self.d = _d
        self.r = _r
        self.grosor = _grosor
        self.color = _color
        self.obj = ring(pos=_p,axis=_d,
                        radius=_r,
                        thickness=_grosor,
                        color=_color)

    def actualizar (self,_p,_d,_r):
        self.p = _p
        self.d = _d
        self.r = _r
        self.obj.pos = _p
        self.obj.axis= _d
        self.obj.radius=_r

class vbrazo:
    def __init__ (self,_p_d,_r_1,_r_2):
        #punto origen
        self.p_o=vector(0,0,0)
        #punto destino
        self.p_d=vector(_p_d)
        #longitud del brazo
        self.r_1 = _r_1
        #longitud del antebrazo
        self.r_2 = _r_2
        #distancia de punto origen a punto destino
        self.d_od = distancia_euclides(self.p_o,self.p_d)
        #distancia de origen a punto pivote de la circunferencia
        self.d_op = (math.pow(self.d_od,2)-math.pow(self.r_2,2)+math.pow(self.r_1,2))/(2*self.d_od)
        #radio de la circunferencia
        self.r_c = math.sqrt(math.pow(self.r_1,2)-math.pow(self.d_op,2))
        #vector direccion del plano de la circunferencia
        self.v_d = norm(self.p_d)
        #punto pivote de la circunferencia
        self.p_p = self.d_op*self.v_d
        #vector ortogonal aletorio de la circunferencia
        self.v_orto1 = norm(vector(1,(self.p_p.z-self.p_p.x)/(self.p_p.y),-1))
        #punto aletorio de la circunferencia
        self.p_orto1 = self.p_p+(self.r_c*self.v_orto1)
        self.c_1 = (self.v_d.y*self.v_d.x*self.p_orto1.x) + (self.v_d.y*self.v_d.z*self.p_orto1.z) + ((self.v_d.y**2)*self.p_orto1.y)
        self.c_2 = (self.v_d.z*self.p_orto1.x) - (self.v_d.x*self.p_orto1.z)
        self.c_3 = self.p_orto1.y
        self.tem_ang = math.atan((-self.c_2)/(self.c_1-self.c_3))
        if ((-self.c_2*np.sin(self.tem_ang)+self.c_1*np.cos(self.tem_ang)-self.c_3*np.cos(self.tem_ang))>0):
            self.ang = self.tem_ang
        else:
            self.ang = self.tem_ang+(np.pi)
    def actualizar (self,_p_d):
        #punto destino
        self.p_d=vector(_p_d)
        #distancia de punto origen a punto destino
        self.d_od = distancia_euclides(self.p_o,self.p_d)
        #distancia de origen a punto pivote de la circunferencia
        self.d_op = (math.pow(self.d_od,2)-math.pow(self.r_2,2)+math.pow(self.r_1,2))/(2*self.d_od)
        #radio de la circunferencia
        self.r_c = math.sqrt(math.pow(self.r_1,2)-math.pow(self.d_op,2))
        #vector direccion del plano de la circunferencia
        self.v_d = norm(self.p_d)
        #punto pivote de la circunferencia
        self.p_p = self.d_op*self.v_d
        #vector ortogonal aletorio de la circunferencia
        self.v_orto1 = norm(vector(1,(self.p_p.z-self.p_p.x)/(self.p_p.y),-1))
        #punto aletorio de la circunferencia
        self.p_orto1 = self.p_p+(self.r_c*self.v_orto1)
        self.c_1 = (self.v_d.y*self.v_d.x*self.p_orto1.x) + (self.v_d.y*self.v_d.z*self.p_orto1.z) + ((self.v_d.y**2)*self.p_orto1.y)
        self.c_2 = (self.v_d.z*self.p_orto1.x) - (self.v_d.x*self.p_orto1.z)
        self.c_3 = self.p_orto1.y
        self.tem_ang = math.atan((-self.c_2)/(self.c_1-self.c_3))
        if ((-self.c_2*np.sin(self.tem_ang)+self.c_1*np.cos(self.tem_ang)-self.c_3*np.cos(self.tem_ang))>0):
            self.ang = self.tem_ang
        else:
            self.ang = self.tem_ang+(np.pi)

fondo = escenario(scene,"Simulador Brazo Robotico", 1000,1000)

p_obj = vector(5.0,5.0,0.0)

arm = vbrazo(p_obj,8.,7.)

origen = o_direccion((0,0,0),2,0.2)

p_ci = rotacion_eje (arm.v_d,arm.p_orto1,0.)
seg1 = segmento(arm.p_o,p_ci,vector(0,1,0),0.3,color.blue)
seg2 = segmento(arm.p_d,p_ci,vector(0,1,0),0.3,color.red)
orto = segmento(arm.p_p,p_ci,vector(0,1,0),0.3,color.cyan)
aro  = circulo(arm.p_p,arm.v_d,arm.r_c,0.2,color.orange)

p_ci1 = rotacion_eje (arm.v_d,arm.p_orto1,arm.ang)
#seg11 = segmento(arm.p_o,p_ci1,vector(0,1,0),0.3,color.white)
#seg21 = segmento(arm.p_d,p_ci1,vector(0,1,0),0.3,color.white)
#orto1 = segmento(arm.p_p,p_ci1,vector(0,1,0),0.3,color.yellow)

vec_d_0 = segmento(arm.p_p,vector(0,0,0),vector(0,1,0),0.3,color.blue)
vec_d_p = segmento(arm.p_p,arm.p_d,vector(0,1,0),0.3,color.red)

sp1 = sphere(pos=arm.p_d,radius=7,color=(1,0,0),opacity=0.05)
sp2 = sphere(pos=arm.p_o,radius=8,color=(0,0,1),opacity=0.05)

def actualizar_data ():
    arm.actualizar(p_obj)
    p_ci = rotacion_eje (arm.v_d,arm.p_orto1,0.)
    seg1.actualizar(arm.p_o,p_ci,vector(0,1,0))
    seg2.actualizar(arm.p_d,p_ci,vector(0,1,0))
    orto.actualizar(arm.p_p,p_ci,vector(0,1,0))
    aro.actualizar(arm.p_p,arm.v_d,arm.r_c)
    
    p_ci1 = rotacion_eje (arm.v_d,arm.p_orto1,arm.ang)
    #seg11.actualizar(arm.p_o,p_ci1,vector(0,1,0))
    #seg21.actualizar(arm.p_d,p_ci1,vector(0,1,0))
    #orto1.actualizar(arm.p_p,p_ci1,vector(0,1,0))

    vec_d_0.actualizar(arm.p_p,vector(0,0,0),vector(0,1,0))
    vec_d_p.actualizar(arm.p_p,arm.p_d,vector(0,1,0))

    sp1.pos = arm.p_d
    sp2.pos = arm.p_o

while(1):
    key = scene.kb.getkey()
    if (key == 'q'):
        p_obj.x+=0.1
        actualizar_data()
    if (key == 'w'):
        p_obj.x-=0.1
        actualizar_data()
    if (key == 'a'):
        p_obj.y+=0.1
        actualizar_data()
    if (key == 's'):
        p_obj.y-=0.1
        actualizar_data()
    if (key == 'z'):
        p_obj.z+=0.1
        actualizar_data()
    if (key == 'x'):
        p_obj.z-=0.1
        actualizar_data()



