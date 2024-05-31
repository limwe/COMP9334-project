#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This program reads in an input argument (which is expected to be
a positive integer) and write some text to a file with name
dummy_*.txt where * is the input argument 


"""

import sys 
import os
import random
import numpy as np



def readfile(fn):
    with open(fn, 'r') as file:
        return file.readlines()

# Define the PDFs
def pdf1(t, a0, b0, e0, g0):
    if 0 <= t <= a0 or t >= b0:
        return 0
    else:
        return e0 / (g0 * t**(e0 + 1))

def pdf2(t, a1, e1, g1):
    if 0 <= t <= a1:
        return 0
    else:
        return e1 / (g1 * t**(e1 + 1))


def gg0(a0, b0, e0, g0):
    while True:
        t = np.random.uniform(a0, b0)
        u = np.random.uniform(0, 1)
        if u <= pdf1(t, a0, b0, e0, g0):
            return t

def gg1(a1, e1, g1):
    while True:
        t = np.random.exponential(scale=1/ (e1 / (g1 * a1 ** (e1 + 1))))
        u = np.random.uniform(0, 1)
        if u <= pdf2(t, a1, e1, g1):
            return t
"""
def gg0(a0, b0, e0, g0):
    density = (e0 / (g0 * a0 ** (e0 + 1)))
    while True:
        sample = np.random.uniform(a0, b0)
        pdf = (e0 / (g0 * sample ** (e0 + 1)))
        if np.random.uniform(0, density) <= pdf:
            return sample

def gg1(a1, e1, g1):
    density = (e1 / (g1 * a1 ** (e1 + 1)))
    while True:
        sample = np.random.exponential(scale=1/density)
        pdf = (e1 / (g1 * sample ** (e1 + 1)))
        if np.random.uniform(0, density) <= pdf:
            return sample
"""
def main(s):
    def run_random():
        def gen():
            while True:
                a1k = np.random.exponential(1/lam)
                a2k = np.random.uniform(a2l, a2u)
                arrival = a1k * a2k
                group = 0 if np.random.uniform(0, 1) < p0 else 1
                time = gg0(a0, b0, e0, g0) if group == 0 else gg1(a1, e1, g1)
                yield {
                    'arrival': arrival,
                    'time': time,
                    'group': group,
                }
        run(gen())

    def run_trace():
        process = []
        t = 0
        for i in range(len(interarrivals)):
            obj = {
                'arrival': interarrivals[i],
                'time': service[i]['time'],
                'group': service[i]['group'],
            }
            process.append(obj)
        run(iter(process))

    def run(it):
        g0 = [None] * n0
        g1 = [None] * n1
        t = 0
        processes = []
        if mode == 'trace':
            processes = list(it)
        else:
            t = 0
            while True:
                q = next(it)
                t += q['arrival']
                if t > time_end:
                    break
                processes.append(q)

        for i, proc in enumerate(processes):
            t += proc['arrival']
            proc['arrival'] = t
            proc['index'] = i
            proc['start'] = False
            proc['end'] = None
            proc['assigned'] = False
            proc['done'] = False

        t = 0.0
        index = 0
        q0 = []
        q1 = []
        while True:
            if index == len(processes) and all([x is None for x in g0]) and all([x is None for x in g1]) and\
                q0 == [] and q1 == []:
                break


            nextArrival = processes[index]['arrival'] if index < len(processes) else float("inf")
            minEvent = nextArrival
            for g in g0:
                if g is not None:
                    if g['depart'] < minEvent:
                        minEvent = g['depart']

            for g in g1:
                if g is not None:
                        if g['depart'] < minEvent:
                            minEvent = g['depart']

            duration = minEvent - t
            t = minEvent
            # print(t, q0, q1, g0, g1, sep = '\n')

            for i in range(len(g0)):
                g = g0[i]
                if g is not None:
                    if g['depart'] <= t + 1e-6:
                        # print('h', g)
                        if t >= g['start'] + g['time'] - 1e-6:
                            g['end'] = t
                            g['done'] = True
                            g0[i] = None
                        elif t - g['start'] >= Tlimit - 1e-6:
                            g0[i] = None
                            g['reason'] = 'r0'
                            for j in range(len(g1)):
                                if g1[j] is None:
                                    g1[j] = g
                                    g['depart'] = t + g['time']
                                    g['start'] = t
                                    break
                            else:
                                q1.append(g)
                        if g0[i] is None:
                            if q0:
                               g0[i] = q0.pop(0)
                               g0[i]['start'] = t
                               g0[i]['depart'] =  min(t + g0[i]['time'], t + Tlimit)
            for i in range(len(g1)):
                g = g1[i]
                if g is not None:
                    if g['depart'] <= t + 1e-6:
                        g['end'] = t
                        g['done'] = True
                        g1[i] = None
                        if q1:
                            g1[i] = q1.pop(0)
                            g1[i]['start'] = t
                            g1[i]['depart'] = t + g1[i]['time']

            for proc in processes:
                if proc['arrival'] <= t and not proc['assigned']:
                    index = max(index, proc['index'] + 1)
                    proc['assigned'] = True
                    if proc['group'] == 0:
                        for i in range(len(g0)):
                            if g0[i] is None:
                                g0[i] = proc
                                proc['reason'] = '0'
                                proc['start'] = t
                                proc['depart'] = min(t + proc['time'], t + Tlimit)
                                break
                        else:
                            q0.append(proc)
                            proc['reason'] = '0'
                    else:
                        for i in range(len(g1)):
                            if g1[i] is None:
                                g1[i] = proc
                                proc['reason'] = '1'
                                proc['start'] = t
                                proc['depart'] = t + proc['time']
                                break
                        else:
                            q1.append(proc)
                            proc['reason'] = '1'
        t0 = []
        t1 = []
        with open('output/dep_' + s + '.txt', 'w') as f:
            for proc in sorted(processes, key = lambda x: x['end']):
                print(f"{proc['arrival']:.04f} {proc['end']:.04f} {proc['reason']}", file = f)
                if proc['reason'] == '0' :
                    if proc['end'] is not None:
                        t0.append(proc['end'] - proc['arrival'])
                elif proc['reason'] == '1':
                    if proc['end'] is not None:
                        t1.append(proc['end'] - proc['arrival'])

        with open('output/mrt_' + s + '.txt', 'w') as f:
            r0 = 0.0 if  len(t0) == 0 else np.mean(t0)
            r1 = 0.0 if  len(t1) == 0 else np.mean(t1)
            print(f"{r0:.04f} {r1:.04f}", file = f)












    mode = readfile(f'config/mode_{s}.txt')[0]
    paras =  list(readfile(f'config/para_{s}.txt'))
    if len(paras) == 3:
        n, n0, Tlimit = paras
        time_end = float("inf")
    else:
        n, n0, Tlimit, time_end = paras
    n = int(n)
    n0 = int(n0)
    Tlimit = float(Tlimit)
    time_end = float(time_end)
    n1 = n - n0
    if mode == 'trace':
        interarrivals = list(map(float, readfile(f'config/interarrival_{s}.txt')))
    else:
        for line in readfile(f'config/interarrival_{s}.txt'):
            lam, a2l, a2u = list(map(float, line.split()))
            break
    service = []
    if mode == 'trace':
        for line in readfile(f'config/service_{s}.txt'):
            time, group = line.split()
            service.append({
                'time': float(time),
                'group': int(group),
            })
    else:
        with open(f'config/service_{s}.txt', 'r') as file:
            p0 = float(file.readline())
            a0, b0, e0 = map(float, file.readline().split())
            a1, e1 = map(float, file.readline().split())

            g1 = a1**(-e1)
            g0 = a0**(-e0) - b0 **(-e0)
    if mode == 'random':
        run_random()
    else:
        run_trace()



if __name__ == "__main__":
   main(sys.argv[1])
