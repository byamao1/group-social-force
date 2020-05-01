# -*-coding:utf-8-*-
# Author: WP and SS
# Email: wp2204@126.com

import pygame
import pygame.draw
import numpy as np
from math import *
# from config import *
import random
import csv

from PreEvac2.readCSV import readCSV
from preEvac.math_func import normalize
from twoPath.agent_model import Agent
from twoPath.math_func import vectorAngleCos

SCREENSIZE = [800, 400]
RESOLUTION = 180
BACKGROUNDCOLOR = [255, 255, 255]
AGENTCOLOR = [0, 0, 255]
LINECOLOR = [255, 0, 0]
LINESICKNESS = 4
AGENTSIZE = 6
AGENTSICKNESS = 3
# WALLSFILE = "walls.csv"
# AGENTSNUM = 8
ZOOMFACTOR = 10
DT = 0.3

pygame.init()
screen = pygame.display.set_mode(SCREENSIZE)
pygame.display.set_caption('Modified Social Force Model')
clock = pygame.time.Clock()
f = open("out.txt", "w+")

# initialize walls
# walls = []
# for line in open(WALLSFILE):
#    coords = line.split(',')
#    wall = []
#    wall.append(float(coords[0]))
#    wall.append(float(coords[1]))
#    wall.append(float(coords[2]))
#    wall.append(float(coords[3]))
#    walls.append(wall)


# initialize agents
# agentFeatures = []
# for line in open("pedTest.txt"):
#    coords = line.split(',')
#    agentFeature = []
#    agentFeature.append(float(coords[0]))
#    agentFeature.append(float(coords[1]))
#    agentFeature.append(float(coords[2]))
#    agentFeature.append(float(coords[3]))
#    agentFeatures.append(agentFeature)


agentFeatures = readCSV("Agent_Data2018.csv")
[Num_Agents, Num_Features] = np.shape(agentFeatures)
print('Number of Agents:', Num_Agents, '\n', file=f)

agents = []
for agentFeature in agentFeatures:
    agent = Agent()
    agent.pos = np.array([agentFeature[0], agentFeature[1]])
    agent.dest = np.array([agentFeature[2], agentFeature[3]])
    agents.append(agent)

walls = readCSV("Wall_Data2018.csv")

# walls = [[3.33, 3.33, 23.97, 3.33],
# [3.33, 3.33, 3.33, 30.31],
# [3.33, 30.31, 23.97, 30.31]]
# [23.31, 3.33, 33.31, 10.02],
# [33.31, 16.92, 23.31, 23.31]]

# walls = [[3.33, 3.33, 29.97, 3.33],
# [3.33, 3.33, 3.33, 33.31],
# [3.33, 33.31, 29.97, 33.31],
# [23.31, 3.33, 33.31, 14.02],
# [33.31, 20.92, 23.31, 33.31]]


# Initialize Desired Interpersonal Distance

DFactor_Init = readCSV("D_Data2018.csv")
AFactor_Init = readCSV("A_Data2018.csv")
BFactor_Init = readCSV("B_Data2018.csv")

# print walls
# print DFactor_Init
# print AFactor_Init
# print BFactor_Init

print("Wall Matrix\n", walls, "\n", file=f)
print("D Matrix\n", DFactor_Init, "\n", file=f)
print("A Matrix\n", AFactor_Init, "\n", file=f)
print("B Matrix\n", BFactor_Init, "\n", file=f)

# DFactor_Init = np.array(
# [[0.0, 0.3, 0.9, 1.3, 1.6, 1.0],
# [0.3, 0.0, 0.3, 1.6, 1.0, 1.2],
# [0.9, 0.3, 0.0, 1.3, 1.3, 1.3],
# [1.3, 0.6, 1.3, 0.0, 1.7, 1.1],
# [1.6, 1.0, 1.3, 1.7, 0.0, 1.8],
# [1.0, 1.2, 0.3, 2.1, 1.8, 0.0]])

# AFactor_Init = np.array(
# [[0.0, 0.3, 0.9, 1.3, 1.6, 1.0],
# [0.3, 0.0, 0.3, 1.6, 1.0, 1.2],
# [0.9, 0.3, 0.0, 1.3, 1.3, 1.3],
# [1.3, 1.6, 1.3, 0.0, 1.7, 1.1],
# [1.6, 1.0, 1.3, 1.7, 0.0, 1.8],
# [1.0, 1.2, 1.2, 2.1, 1.8, 0.0]])

# BFactor_Init = np.array(
# [[0.0, 0.3, 0.9, 2.3, 2.6, 1.0],
# [1.3, 0.0, 3.3, 1.6, 3.0, 1.2],
# [0.9, 0.3, 0.0, 1.3, 1.3, 1.3],
# [1.3, 18.6, 1.3, 0.0, 1.7, 1.1],
# [1.6, 1.0, 1.3, 12.7, 0.0, 1.8],
# [1.0, 1.2, 18.8, 2.1, 1.8, 0.0]])


# Input Data Check
# [Num_D1, Num_D2]=np.shape(DFactor_Init)
# [Num_A1, Num_A2]=np.shape(AFactor_Init)
# [Num_B1, Num_B2]=np.shape(BFactor_Init)

if np.shape(DFactor_Init) != [Num_Agents, Num_Agents]:
    print('\nError on input data\n')

if np.shape(AFactor_Init) != [Num_Agents, Num_Agents]:
    print('\nError on input data\n')

if np.shape(BFactor_Init) != [Num_Agents, Num_Agents]:
    print('\nError on input data\n')

DFactor = DFactor_Init
AFactor = AFactor_Init
BFactor = BFactor_Init

comm = np.zeros((Num_Agents, Num_Agents))

# initialize agents
agents = []
for n in range(Num_Agents):
    agent = Agent()
    agents.append(agent)

# agents[1].pos = np.array([60, 8])
# agents[1].dest = np.array([20.0,10.0])
# agents[1].direction = normalize(agents[1].dest - agents[1].pos)
agents[1].desiredSpeed = 1.8
# agents[1].desiredV = agents[1].desiredSpeed*agents[1].direction
agents[1].p = 0.2

# agents[2].pos = np.array([60, 12])
# agents[2].dest = np.array([20.0,18.0])
# agents[2].direction = normalize(agents[2].dest - agents[2].pos)
agents[2].desiredSpeed = 1.8
# agents[2].desiredV = agents[2].desiredSpeed*agents[2].direction
# agents[2].B = 3.6
agents[2].p = 0.1

agents[3].changeAttr(32, 22, 0, 0)
agents[3].p = 0.3

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            (mouseX, mouseY) = pygame.mouse.get_pos()
        # elif event.type == pygame.MOUSEBUTTONUP:

    screen.fill(BACKGROUNDCOLOR)

    # draw walls
    for wall in walls:
        startPos = np.array([wall[0], wall[1]])
        endPos = np.array([wall[2], wall[3]])
        startPx = startPos * ZOOMFACTOR
        endPx = endPos * ZOOMFACTOR
        pygame.draw.line(screen, LINECOLOR, startPx, endPx, LINESICKNESS)

    # draw agents
    #   pygame.draw.circle(screen, AGENTCOLOR, (np.array(SCREENSIZE)/2).tolist(),
    #                      AGENTSIZE, AGENTSICKNESS)

    # 计算相互作用力
    for idai, ai in enumerate(agents):

        # Pre-evacuation Time Effect
        tt = pygame.time.get_ticks() / 1000
        if (tt < ai.tpre):
            ai.desiredSpeed = random.uniform(0.3, 0.6)
        else:
            ai.desiredSpeed = random.uniform(2.0, 3.0)

        ai.direction = normalize(ai.dest - ai.pos)
        ai.desiredV = ai.desiredSpeed * ai.direction
        # ai.desiredV = 0.3*ai.desiredV + 0.7*ai.desiredV_old
        peopleInter = 0.0
        wallInter = 0.0
        otherMovingDir = np.array([0.0, 0.0])
        otherMovingSpeed = 0.0
        otherMovingNum = 0

        ai.actualSpeed = np.linalg.norm(ai.actualV)
        ai.desiredSpeed = np.linalg.norm(ai.desiredV)

        # print >> f, "desired speed of agent i:", ai.desiredSpeed, "/n"
        # print >> f, "actual speed of agent i:", ai.actualSpeed, "/n"

        if ai.desiredSpeed != 0:
            ai.ratioV = ai.actualSpeed / ai.desiredSpeed
        else:
            ai.ratioV = 1

        ai.stressLevel = 1 - ai.ratioV
        ai.diw_desired = max(0.5, ai.ratioV) * 0.6
        # ai.A_WF = 30*max(0.5, ai.ratioV)
        ai.B_WF = 2.2 * max(min(0.5, ai.ratioV), 0.2)

        # There are two method:
        # 1. White Noise Method
        # 2. Stress Level Method (Helbing's Equation)
        ai.p = random.uniform(-0.3, 0.3)  # Method-1
        # ai.p = 1 - ai.ratioV  	# Method-2

        for idaj, aj in enumerate(agents):

            rij = ai.radius + aj.radius
            dij = np.linalg.norm(ai.pos - aj.pos)

            # Difference of current destinations
            dij_dest = np.linalg.norm(ai.dest - aj.dest)

            # Difference of desired velocities
            vij_desiredV = np.linalg.norm(ai.desiredV - aj.desiredV)

            # Difference of actual velocities
            vij_actualV = np.linalg.norm(ai.actualV - aj.actualV)

            phiij = vectorAngleCos(ai.actualV, (aj.pos - ai.pos))
            anisoF = ai.lamb + (1 - ai.lamb) * (1 + cos(phiij)) * 0.5

            # print >> f, "anisotropic factor", anisoF, "/n"

            if idai == idaj:
                # selfRepulsion = -ai.selfRepulsion(DFactor[idai, idai], AFactor[idai, idai], BFactor[idai, idai])*ai.direction
                # peopleInter += selfRepulsion
                continue

            peopleInter += ai.cohesiveForce(aj, DFactor[idai, idaj], AFactor[idai, idaj], BFactor[idai, idaj]) * anisoF

            peopleInter += ai.agentForce(aj) * anisoF

            if dij < ai.B_CF * BFactor[idai, idaj] + rij * DFactor[idai, idaj]:
                # if dij < ai.interactionRange:
                otherMovingDir += normalize(aj.actualV)  # /DFactor[idai, idaj]*AFactor[idai, idaj]
                otherMovingSpeed += np.linalg.norm(aj.actualV)  # /DFactor[idai, idaj]*AFactor[idai, idaj]
                otherMovingNum += 1
                comm[idai, idaj] = 1

                # DFactor[idai, idaj] = (1-ai.p)*DFactor[idai, idaj]+ai.p*DFactor[idaj, idai]
                # AFactor[idai, idaj] = (1-ai.p)*AFactor[idai, idaj]+ai.p*AFactor[idaj, idai]
                # BFactor[idai, idaj] = (1-ai.p)*BFactor[idai, idaj]+ai.p*BFactor[idaj, idai]
                # ai.desiredV = (1-ai.p)*ai.desiredV + ai.p*aj.desiredV

            else:
                comm[idai, idaj] = 0

                # ai.desiredV = ai.p*ai.desiredV + ai.peopleInterOpinion(aj)[0]
            # The Above Method is Not Correct

        if otherMovingNum != 0:
            ai.direction = (1 - ai.p) * ai.direction + ai.p * otherMovingDir
            ai.desiredSpeed = (1 - ai.p) * ai.desiredSpeed + ai.p * otherMovingSpeed / otherMovingNum
            ai.desiredV = ai.desiredSpeed * ai.direction

        # ai.desiredV = (1-ai.p)*ai.desiredV + ai.p*otherMovingDir

        # tt = pygame.time.get_ticks()/1000
        # if (tt < ai.Tpre):
        #    ai.desiredV = ai.direction*0.0
        #    ai.desiredSpeed = 0.0
        #    ai.dest = ai.pos

        # Calculate Forces
        motiveForce = ai.adaptVel()

        # ai.sumAdapt += motiveForce*0.2

        for wall in walls:
            wallInter += ai.wallForce(wall)

        # print('Forces from Walls:', wallInter)
        # print('Forces from people:', peopleInter)

        # tt = pygame.time.get_ticks()/1000
        if (tt < ai.tpre):
            motiveForce = np.array([0.0, 0.0])

        sumForce = motiveForce + peopleInter + wallInter + ai.diss * ai.actualV
        # + ai.sumAdapt
        # Compute acceleration
        accl = sumForce / ai.mass
        # Compute velocity
        ai.actualV = ai.actualV + accl * DT  # consider dt = 0.5

        ai.actualSpeed = np.linalg.norm(ai.actualV)
        if (ai.actualSpeed >= ai.maxSpeed):
            ai.actualV = ai.actualV * ai.maxSpeed / ai.actualSpeed
        # ai.actualV[0] = ai.actualV[0]*ai.maxSpeed/ai.actualSpeed
        # ai.actualV[1] = ai.actualV[1]*ai.maxSpeed/ai.actualSpeed

        # Calculate Positions
        ai.pos = ai.pos + ai.actualV * DT
        # print(ai.pos)
        # print(accl,ai.actualV,ai.pos)

        ai.desiredV_old = ai.desiredV
        ai.actualV_old = ai.actualV

        if (ai.pos[0] >= 35.0) & (ai.Goal == 0):
            print('test')
            ai.Goal = 1
            ai.timeOut = pygame.time.get_ticks()
            # ai.timeOut = clock.get_time()/1000.0
            print('Time to Reach the Goal:', ai.timeOut)
            print('Time to Reach the Goal:', ai.timeOut, file=f)

    ####################
    # Drawing the agents
    ####################
    # for agent in agents:
    for idai, agent in enumerate(agents):
        # scPos = np.array([0, 0])
        scPos = [0, 0]
        scPos[0] = int(agent.pos[0] * ZOOMFACTOR)
        scPos[1] = int(agent.pos[1] * ZOOMFACTOR)

        leftS = [0, 0]
        leftShoulder = agent.shoulders()[0]
        leftS[0] = int(leftShoulder[0] * ZOOMFACTOR)
        leftS[1] = int(leftShoulder[1] * ZOOMFACTOR)

        rightS = [0, 0]
        rightShoulder = agent.shoulders()[1]
        rightS[0] = int(rightShoulder[0] * ZOOMFACTOR)
        rightS[1] = int(rightShoulder[1] * ZOOMFACTOR)

        print('shoulders:', leftS, rightS)

        endPosV = [0, 0]
        endPosV[0] = int(agent.pos[0] * ZOOMFACTOR + agent.actualV[0] * ZOOMFACTOR)
        endPosV[1] = int(agent.pos[1] * ZOOMFACTOR + agent.actualV[1] * ZOOMFACTOR)

        endPosDV = [0, 0]
        endPosDV[0] = int(agent.pos[0] * ZOOMFACTOR + agent.desiredV[0] * ZOOMFACTOR)
        endPosDV[1] = int(agent.pos[1] * ZOOMFACTOR + agent.desiredV[1] * ZOOMFACTOR)

        # temp = int(100*agent.ratioV)
        # AGENTCOLOR = [0,0,temp]
        color_para = [0, 0, 0]
        color_para[0] = int(255 * min(1, agent.ratioV))
        pygame.draw.circle(screen, color_para, scPos, AGENTSIZE, AGENTSICKNESS)
        pygame.draw.circle(screen, color_para, leftS, AGENTSIZE // 2, 3)
        pygame.draw.circle(screen, color_para, rightS, AGENTSIZE // 2, 3)

        # stressShow = 0
        # stressShow = int(255*agent.ratioV)
        # pygame.draw.line(screen, AGENTCOLOR, leftS, rightS, 3)
        pygame.draw.line(screen, AGENTCOLOR, scPos, endPosV, 2)
        pygame.draw.line(screen, [255, 60, 0], scPos, endPosDV, 2)

        for idaj, agentOther in enumerate(agents):
            scPosOther = [0, 0]
            scPosOther[0] = int(agentOther.pos[0] * ZOOMFACTOR)
            scPosOther[1] = int(agentOther.pos[1] * ZOOMFACTOR)
            if comm[idai, idaj] == 1:
                pygame.draw.line(screen, AGENTCOLOR, scPos, scPosOther, 2)

            # print(scPos)

    pygame.display.flip()
    clock.tick(20)

f.close()
