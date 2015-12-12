# Copyright 2015 Michael Gugino
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import pylw.routing


def myfun():
    print "myfun returned"

def myfun2():
    print "myfun2 returned"

r = pylw.routing.CRouter()

p = '/'
p2 = '/root'
p3 = '/root/child/{var1}'
p4 = 'root/child/{var1}/{var2}'

r.add_path(p, myfun)
r.add_path(p2, myfun)
r.add_path(p3, myfun2)
r.add_path(p4, myfun)
var_dict = {}

#a = r.return_path_resource(p,var_dict)
#a()

b = r.return_path_resource('/root/child/val1//',var_dict)
b()

c = r.return_path_resource('/root/child/val1/val2',var_dict)
c()

d = r.return_path_resource('root/child/val1/val2/',var_dict)
d()

print var_dict
