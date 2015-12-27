// Copyright 2015 Michael Gugino
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

#include <Python.h>
#include <string.h>
#include <stddef.h>
#include <stdio.h>


char* get_str_part(char* url_string) {
  char *token;
  token = strsep(&url_string, "&");
  return token;
}

static PyObject*
find_route(PyObject* self, PyObject* args) {
  char *url_string;
  char *url_copy;
  char *freeurl;
  PyDictObject *root_dict;
  PyDictObject *var_dict;
  PyObject *root_node;
  PyObject *temp_node;
  PyObject *temp_node2;
  PyObject *children_dict;
  char *str_part;
  //char *listitems;
  PyObject *myfun;
  root_node = NULL;
  temp_node = NULL;
  temp_node2 = NULL;
  myfun = NULL;

  if (!PyArg_ParseTuple(args, "sOO", &url_string, &root_dict, &var_dict)) {
      PyErr_SetString(PyExc_RuntimeError, "Invalid Args");
      return NULL;
  }


  freeurl = url_copy = strdup(url_string);
  if (url_copy == NULL) {
    PyErr_SetString(PyExc_RuntimeError, "Unable to malloc");
    return NULL;
  }

  //trim leading '/'
while (url_copy[0] == '/') {
    url_copy++;
  }

// trim trailing '/'
  while (url_copy[strlen(url_copy)-1] == '/') {
      url_copy[strlen(url_copy)-1] = 0;
  }

  while ((str_part = strsep(&url_copy, "/")) != NULL) {
      children_dict = NULL;
      temp_node2 = NULL;
      myfun = NULL;
      if (!root_node) {
          temp_node = PyDict_GetItem(root_dict, PyString_FromString(str_part));
          if (!temp_node)
            break;
          root_node = temp_node;
          myfun = PyObject_CallMethodObjArgs(temp_node, PyString_FromString("get_resource"), NULL );
      }
      else {
          if (temp_node) {
            children_dict = PyObject_CallMethodObjArgs(temp_node, PyString_FromString("get_children"), NULL );
            if (children_dict) {
              temp_node2 = PyDict_GetItem(children_dict, PyString_FromString(str_part));
              if (!temp_node2) {
                temp_node2 = PyObject_CallMethodObjArgs(temp_node, PyString_FromString("get_varchild"), NULL );
                if (temp_node2) {
                  PyDict_SetItem(var_dict, PyObject_CallMethodObjArgs(temp_node2, PyString_FromString("get_name"), NULL ), PyString_FromString(str_part));
                  temp_node = temp_node2;
                }
                else {
                  myfun = NULL;
                  break;
                }
              }
              else
                temp_node = temp_node2;
            }
            myfun = PyObject_CallMethodObjArgs(temp_node, PyString_FromString("get_resource"), NULL );
          }
      }
  }

    free(freeurl);
    if (!myfun) {
      PyErr_SetString(PyExc_RuntimeError, "No resource found");
    }
    return myfun;
}


static PyMethodDef QSMethods[] =
{
     {"find_route", find_route, METH_VARARGS, "Find a route"},
     {NULL, NULL, 0, NULL}
};

PyMODINIT_FUNC
initroute_find(void)
{
     (void) Py_InitModule("route_find", QSMethods);
}
