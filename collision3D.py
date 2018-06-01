from visual import *
import random


#This function changes the spheres' velocity when they collision.
def collision(a):
    for u in range(len(a)):
        for m in range(u + 1, len(a)):
            if abs(Atoms[u].pos.x - Atoms[m].pos.x) < 2 * r:
                if abs(Atoms[u].pos.y - Atoms[m].pos.y) <= 2 * r:
                    if abs(Atoms[u].pos.z - Atoms[m].pos.x) <= 2 * r:
                        l = Atoms[u].pos - Atoms[m].pos
                        len_l = mag(l)
                        if len_l <= 2 * r and dot(Atoms[u].velocity, l) < 0:
                            nv1 = dot(Atoms[u].velocity, l) / len_l / len_l * l
                            nv2 = dot(Atoms[m].velocity, l) / len_l / len_l * l
                            Atoms[u].velocity = Atoms[u].velocity - nv1 + nv2
                            Atoms[m].velocity = Atoms[m].velocity - nv2 + nv1

def main(n):
    L=1
    #Creat a windows.
    scene = display(title="Gas", width=500, height=500, x=0, y=0,
                    range=L, center=(L/2.,L/2.,L/2.))
    global r
    r=0.03  # the spheres' radius.
    global Atoms
    Atoms = []

    scene.exit = False

    #This is the frequency.
    deltat=0.0001

    #About the color.
    gray = (0.7,0.7,0.7)
    colors = [color.red, color.green, color.blue,
          color.yellow, color.cyan, color.magenta]


    #Add the curve to make a cube.
    xaxis = curve(pos=[(0,0,0), (L,0,0)], color=gray, radius=0.001)
    yaxis = curve(pos=[(0,0,0), (0,L,0)], color=gray, radius=0.001)
    zaxis = curve(pos=[(0,0,0), (0,0,L)], color=gray, radius=0.001)
    xaxis2 = curve(pos=[(L,L,L), (0,L,L), (0,0,L), (L,0,L)], color=gray, radius=0.001)
    yaxis2 = curve(pos=[(L,L,L), (L,0,L), (L,0,0), (L,L,0)], color=gray, radius=0.001)
    zaxis2 = curve(pos=[(L,L,L), (L,L,0), (0,L,0), (0,L,L)], color=gray, radius=0.001)



    # Add the spheres.
    for i in range(n):
        px=random.random()
        py=random.random()
        pz=random.random()
        Atoms = Atoms + [sphere(pos=(px,py,pz), radius=r, color=colors[i % 6])]


    # Give a random velocity for each spheres.
    for i in range(n):
        vx=random.random()
        vy=random.random()
        vz=random.random()
        Atoms[i].velocity=vector(vx*100,vy*100,vz*100)

    while True:
        rate(30)
        # Devide the cube into nine sections so that decrease the computation.
        a1, a2, a3, a4, a5, a6, a7, a8, a9 = [], [], [], [], [], [], [], [], []
        for i in range(n):
            # Find the sphere whether out of the cube.
            if Atoms[i].pos.x >= 1 - r:
                Atoms[i].velocity.x = -abs(Atoms[i].velocity.x)
            if Atoms[i].pos.x <= 0 + r:
                Atoms[i].velocity.x = abs(Atoms[i].velocity.x)
            if Atoms[i].pos.y >= 1 - r:
                Atoms[i].velocity.y = -abs(Atoms[i].velocity.y)
            if Atoms[i].pos.y <= 0 + r:
                Atoms[i].velocity.y = abs(Atoms[i].velocity.y)
            if Atoms[i].pos.z >= 1 - r:
                Atoms[i].velocity.z = -abs(Atoms[i].velocity.z)
            if Atoms[i].pos.z <= 0 + r:
                Atoms[i].velocity.z = abs(Atoms[i].velocity.z)

            # Devide them into nine sections.
            if Atoms[i].pos.z < L / 2 - r and Atoms[i].pos.x < L / 2 - r and Atoms[i].pos.y < L / 2 - r:
                a1 = a1 + [Atoms[i]]
            elif Atoms[i].pos.z < L / 2 - r and Atoms[i].pos.x > L / 2 + r and Atoms[i].pos.y < L / 2 - r:
                a2 = a2 + [Atoms[i]]
            elif Atoms[i].pos.z < L / 2 - r and Atoms[i].pos.x < L / 2 - r and Atoms[i].pos.y > L / 2 + r:
                a3 = a3 + [Atoms[i]]
            elif Atoms[i].pos.z < L / 2 - r and Atoms[i].pos.x > L / 2 + r and Atoms[i].pos.y > L / 2 + r:
                a4 = a4 + [Atoms[i]]
            elif Atoms[i].pos.z > L / 2 + r and Atoms[i].pos.x < L / 2 - r and Atoms[i].pos.y < L / 2 - r:
                a5 = a5 + [Atoms[i]]
            elif Atoms[i].pos.z > L / 2 + r and Atoms[i].pos.x > L / 2 + r and Atoms[i].pos.y < L / 2 - r:
                a6 = a6 + [Atoms[i]]
            elif Atoms[i].pos.z > L / 2 + r and Atoms[i].pos.x < L / 2 - r and Atoms[i].pos.y > L / 2 + r:
                a7 = a7 + [Atoms[i]]
            elif Atoms[i].pos.z > L / 2 + r and Atoms[i].pos.x > L / 2 + r and Atoms[i].pos.y > L / 2 + r:
                a8 = a8 + [Atoms[i]]
            else:
                a9 = a9 + [Atoms[i]]

            # Find spheres in the ninth section and change their velocity.
            for u in range(len(a9)):
                l = Atoms[i].pos - Atoms[u].pos
                len_l = mag(l)
                if len_l <= 2 * r and dot(Atoms[i].velocity, l) < 0:
                    nv1 = dot(Atoms[i].velocity, l) / len_l / len_l * l
                    nv2 = dot(Atoms[u].velocity, l) / len_l / len_l * l
                    Atoms[i].velocity = Atoms[i].velocity - nv1 + nv2
                    Atoms[u].velocity = Atoms[u].velocity - nv2 + nv1

        # Collision
        collision(a1)
        collision(a2)
        collision(a3)
        collision(a4)
        collision(a5)
        collision(a6)
        collision(a7)
        collision(a8)

        for i in range(n):
            Atoms[i].pos = Atoms[i].pos + Atoms[i].velocity * deltat


if __name__ == "__main__":
    main(100)
