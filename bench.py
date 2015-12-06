#!/usr/bin/env python
import main
import timeit

import app

path1 = '/medium/path/length'

env = {
'REQUEST_METHOD' : 'GET',
'PATH_INFO' : path1
}

env2 = {
'REQUEST_METHOD' : 'GET',
'PATH_INFO' : path1
}


def start_response(headers, body):
    pass

a = app.App(secret_key='test')
b = app.App(secret_key='test')
a.router.add_path(path1,main.HelloWorld)
b.add_hard_coded_path(path1,main.HelloWorld)

def runa():
        a(env, start_response)


def runb():
        b(env2, start_response)

sum1 = 0
sum1 += timeit.timeit(runa,number=10000)
sum1 += timeit.timeit(runa,number=10000)
sum1 += timeit.timeit(runa,number=10000)

print 'hard code path'

sum2 = 0

sum2 += timeit.timeit(runb,number=10000)
sum2 += timeit.timeit(runb,number=10000)
sum2 += timeit.timeit(runb,number=10000)

av1 = sum1/3
av2 = sum2/3

print 'av1:', av1
print 'av2:', av2

diff = av1 - av2
print 'diff:', diff
print 'diff% :', diff/av1
#a(env, start_response)
