#!/usr/bin/env python

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

'''Adding routes to your project is easy'''
import pylw.route_find
class Node(object):
    '''Implements basic class for url nodes.  These nodes contain child nodes,
       variable child nodes, and/or functions.  This allows us to walk through
       the requested URL path and get the most relevant result.'''

    def __init__(self,resource=None,name=None,isvar=False):
        self.children = {}
        self.resource = resource
        self.isvar = isvar
        self.name = name
        self.varchild = None

    def __repr__(self): # pragma: no cover
        return self.name

    def get_children(self):
        return self.children

    def get_varchild(self):
        return self.varchild

    def get_resource(self):
        return self.resource

    def get_name(self):
        return self.name

class DefaultRouter(object):
    '''This class implements the DefaultRouter.  DefaultRouter is meant to be
       used directly parse paths into callable resources, and to map requested
       urls from the client to our callable resources we mapped earlier.'''

    def __init__(self):
        self.root_node_dict = {}


    def parse_path(self, uri):
        '''Splits our path into sections using '/' as the separator.
           If the path = '/', then we map '/'.  Otherwise, we trim off the first
           item in the list as it would be blank and nondescriptive.

           The list is returned in reverse so we can pop it.'''
        if uri == '/':
            l = [uri]
        else:
            l = uri.split('/')
            if l[0] == '':
                l = l[1:]
            l.reverse()
        return l

    def add_path(self,uri,resource):
        '''takes in a path string and callable resource, calls parse_path,
           and maps that path to our callable resource.'''

        current_node = None
        root_node = None
        url = self.parse_path(uri)
        while url:
            a = url.pop()

            if root_node is None:
                if not a in self.root_node_dict:
                    root_node = Node(name=a)
                    self.root_node_dict[a] = root_node
                else:
                    root_node = self.root_node_dict[a]

                current_node = root_node

            else: #current_node is not None:
                if '}' not in a:
                    if not a in current_node.children:
                        new_node = Node(name=a)
                        current_node.children[a] = new_node
                    else:
                        new_node = current_node.children[a]
                else:
                    #we found a variable.
                    if not current_node.varchild:
                        new_node = Node(name=a)
                        new_node.isvar = True
                        current_node.varchild = new_node
                    else:
                        new_node = current_node.varchild

                current_node = new_node
        current_node.resource = resource

    def return_path_resource(self,uri,var_dict):
        '''Takes in a string path, and parses it.  It uses the parsed path to
           determine what resource to call.  Raises a 404 exception if a mappped
           resource is not found.

           Also takes in var_dict.  var_dict is an existing dictionary to place
           values of parts of the url that are variables.'''


        current_node = None
        root_node = None
        url = self.parse_path(uri)
        try:
            while url:
                a = url.pop()

                if root_node is None:
                    if not a in self.root_node_dict:
                        #perhaps we should allow a variable on the first node.
                        print "404: no root node: %s" % a
                        raise Exception()
                    else:
                        root_node = self.root_node_dict[a]

                    current_node = root_node

                else:

                    if not a in current_node.children:
                        #we didn't find a defined path, let's try varchild.
                            current_node = current_node.varchild
                    else:
                        current_node = current_node.children[a]

                if current_node.isvar is True:
                    var_dict[current_node.name] = a

            return current_node.resource
        except:
            body = "404: no path found for: %s" % uri
            code = '404 Not Found'
            raise Exception(code, body)

class CRouter(DefaultRouter):

    def parse_path2(self, uri):
        '''Splits our path into sections using '/' as the separator.
           If the path = '/', then we map '/'.  Otherwise, we trim off the first
           item in the list as it would be blank and nondescriptive.

           The list is not returned in reverse'''
        if uri == '/':
            l = [uri]
        else:
            l = uri.split('/')
            if l[0] == '':
                l = l[1:]
        #if the last item is blank due to trailing slash, we must trim it or
        #C will segfault, yay.
        if l[len(l)-1] == '':
            l = l[0:len(l)-2]
        return l

    def return_path_resource(self,uri,var_dict):
        #url = self.parse_path2(uri)
        return pylw.route_find.find_route(uri,self.root_node_dict,var_dict)
