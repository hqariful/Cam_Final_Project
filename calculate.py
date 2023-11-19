import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk

# OS = OutStroke,
# DW = Dwell
# RS = Return Stroke
# rB = Base Circle
# rF = Offset Distance
# F_Stroke = Follower Stroke

OS_info = {
    "type" : "Const Velocity",
    "Ang" : 60
}
DW_Ang = 30
RS_info = {
    "type" : "Const Velocity",
    "Ang" : 60
}

rB = 50 # Base Circle
F_Stroke = 40 # Follower Stroke
rF = 20 # Offset Distance
plot_rad_cam = True


def calculate():
    # create angle variable from 0 to 360 degree
    global theta, r
    theta = np.linspace(0,360,360)

    # similarly create radius variable with 0 unit
    r = np.zeros(np.shape(theta))

    # Extracting individual angle and shortening varibale names
    dOS = OS_info["Ang"]
    dRW = RS_info["Ang"]
    dDw = DW_Ang

    r[dOS:dOS+dDw] = F_Stroke # Dwell formula is same for every cam

    # Below formula are for linear constant velocity
    if OS_info["type"] == "Const Velocity":
        r[:dOS] = theta[:dOS]/dOS*F_Stroke
    if RS_info["type"] == "Const Velocity":
        r[dOS+dDw:dOS+dDw+dRW] = F_Stroke - theta[:dRW]/dRW*F_Stroke

    # Below formula are for simple harmonic motion
    if OS_info["type"] == "shm":
        r[:dOS] = F_Stroke/2-(F_Stroke/2)*np.cos(theta[:dOS]/dOS*np.pi)
    if RS_info["type"] == "shm":
        r[dOS+dDw:dOS+dDw+dRW] = F_Stroke/2 + (F_Stroke/2)*np.cos(theta[:dRW]/dRW*np.pi)

    # Below formula are for linear acceleration motion
    if OS_info["type"] == "const acc":
        m = 2*F_Stroke/dOS**2
        r[:int(dOS/2)] = m*theta[:int(dOS/2)]**2
        r[int(dOS/2):dOS] = F_Stroke - m*(theta[int(dOS/2):dOS]-dOS)**2
    if RS_info["type"] == "const acc":
        m = 2*F_Stroke/dRW**2
        r[dOS+dDw:dOS+dDw+int(dRW/2)] = F_Stroke-m*theta[:int(dRW/2)]**2
        r[dOS+dDw+int(dRW/2):dOS+dDw+dRW] = m*(theta[int(dRW/2):dRW]-dRW)**2

    # Below formula for cycloidal motion
    rG = F_Stroke/(2*np.pi) # Generating circle radius
    if OS_info["type"] == "cyc":
        r[:dOS] = theta[:dOS]/dOS*F_Stroke - rG*np.sin(theta[:dOS]/dOS*2*np.pi)
    if RS_info["type"] == "cyc":
        r[dOS+dDw:dOS+dDw+dRW] = F_Stroke - theta[:dRW]/dRW*F_Stroke + rG*np.sin(theta[:dRW]/dRW*2*np.pi)


def disp_diag():
    fig = plt.figure()
    ax = fig.add_subplot()
    ax.plot(theta, r)
    ax.grid(True)
    plt.xlabel('theta')
    plt.ylabel('displacement')

def radial_plot():
    fig = plt.figure()
    rtheta = np.pi/180 * theta
    ax_r = fig.add_subplot(projection='polar')

    # below are the calculation for the radial plot and offset
    op_sid = (rB**2-rF**2)**0.5
    rad = (r**2 + 2*r*op_sid+rB**2)**0.5
    if rF==0: alpha=0 
    else: alpha = np.arctan((r+op_sid)/rF)
    if rF == 0 : phi = 0
    else: phi = np.arctan(op_sid/rF) # angle between op_sid and rF
    ax_r.plot(rtheta-np.arcsin(rF/rB)+(alpha-phi), rad)
    ax_r.grid(True)
    ax_r.set_theta_offset(np.pi/2)

def run():
    calculate()
    # saving the figure and showing
    if plot_rad_cam == True : radial_plot() 
    else: disp_diag()
    plt.savefig('filename.png', dpi=200)
    plt.show()

class CamGui:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.geometry('500x400')
        self.root.title('Cam profile generator')
        font = ("Ariel",12)
        dist = 230
        motion = ['Const Velocity','const acc','shm','cyc']
        self.chOut = tk.StringVar(self.root)
        self.chOut.set("Type of motion")
        self.chRtn = tk.StringVar(self.root)
        self.chRtn.set("Type of motion")

        lbOut = tk.Label(self.root,text='Outstroke',font=font)
        lbOut.place(x=20,y=20)
        self.enOut = tk.Entry(self.root)
        self.enOut.place(x=dist,y=20)
        self.Outch = tk.OptionMenu(self.root,self.chOut,*motion)
        self.Outch.place(x=370,y=15)

        lbDw = tk.Label(self.root,text="Dwell",font=font)
        lbDw.place(x=20,y=60)
        self.enDw = tk.Entry(self.root)
        self.enDw.place(x=dist,y=60)

        lbRtn = tk.Label(self.root,text="Return Stroke",font=font)
        lbRtn.place(x=20,y=100)
        self.enRtn = tk.Entry(self.root)
        self.enRtn.place(x=dist,y=100)
        self.Rtnch = tk.OptionMenu(self.root,self.chRtn,*motion)
        self.Rtnch.place(x=370,y=95)

        lbrB = tk.Label(self.root,text="Base circle radius", font=font)
        lbrB.place(x=20,y=140)
        self.enrB = tk.Entry(self.root)
        self.enrB.place(x=dist,y=140)

        lbLf = tk.Label(self.root,text="Max follower displacement", font=font)
        lbLf.place(x=20,y=180)
        self.enLf = tk.Entry(self.root)
        self.enLf.place(x=dist,y=180)

        lbrf = tk.Label(self.root,text='Offset Distance',font=font)
        lbrf.place(x=20,y=220)
        self.enrf = tk.Entry(self.root)
        self.enrf.place(x=dist,y=220)

        self.cam_or_disp = tk.BooleanVar()
        chDisp = tk.Label(self.root,text="Display: ",font=font)
        chDisp.place(x=20,y=260)
        chplt = tk.Radiobutton(self.root,text="Radial plot",value=True,variable=self.cam_or_disp,font=font)
        chplt.place(x=dist,y=260)
        chplt2 = tk.Radiobutton(self.root,text="Displacement Diagram",value=False,variable=self.cam_or_disp,font=font)
        chplt2.place(x=dist,y=300)

        submitbtn = tk.Button(self.root,text="Submit",font=font,command=self.submit)
        submitbtn.place(x=200,y=340)

        self.root.mainloop()
    
    def submit(self):
        global OS_info, DW_Ang, RS_info, rB, F_Stroke, rF, plot_rad_cam
        OS_info["Ang"] = int(self.enOut.get())
        OS_info["type"] = self.chOut.get()
        DW_Ang = int(self.enDw.get())
        RS_info["Ang"] = int(self.enRtn.get())
        RS_info["type"] = self.chRtn.get()
        rB = int(self.enrB.get())
        F_Stroke = int(self.enLf.get())
        rF = int(self.enrf.get())
        plot_rad_cam = self.cam_or_disp.get()
        self.root.destroy()
        run()
        
CamGui()
# run()
