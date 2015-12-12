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
find_route2(PyObject* self, PyObject* args) {
  char *url_string;
  char *url_copy;
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

  if (!PyArg_ParseTuple(args, "sOO", &url_string, &root_dict, &var_dict))
      return NULL;

  url_copy = strdup(url_string);

  //trim leading '/'
while (url_copy[0] == '/') {
  //  printf("url copy leading slash\n");
    url_copy++;
  }

// trim trailing '/'
  while (url_copy[strlen(url_copy)-1] == '/') {
      //printf("url copy trailing slash\n");
      url_copy[strlen(url_copy)-1] = 0;
  }
  //printf("urlcopy: %s\n", url_copy);
  while ((str_part = strsep(&url_copy, "/")) != NULL) {
    //  printf("urlcopy: %s\n", url_copy);
    //  printf("str_part: %s\n", str_part);

      //listitems = PyString_AsString(listitem);
      //printf("\n\nlistitems: %s", listitems);
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

//PyObject* PyDict_GetItem(PyObject *p, PyObject *key)
    //free(localqs);
  //  if (url_copy)
    //  free(url_copy);
    if (!myfun) {
      PyErr_SetString(PyExc_RuntimeError, "No resource found");
    }
    return myfun;
}

static PyObject*
find_route(PyObject* self, PyObject* args)
{
  PyListObject *url_list;
  PyDictObject *root_dict;
  PyDictObject *var_dict;
  PyObject *root_node;
  PyObject *temp_node;
  PyObject *temp_node2;
  PyObject *children_dict;
  PyObject *listitem;
  char *listitems;
  PyObject *myfun;
  root_node = NULL;
  temp_node = NULL;
  temp_node2 = NULL;
  myfun = NULL;
  if (!PyArg_ParseTuple(args, "OOO", &url_list, &root_dict, &var_dict))
      return NULL;

  for (Py_ssize_t i = 0; i < PyList_Size(url_list); i++) {
      listitem = PyList_GET_ITEM(url_list, i);
      listitems = PyString_AsString(listitem);
      //printf("\n\nlistitems: %s", listitems);
      children_dict = NULL;
      temp_node2 = NULL;
      myfun = NULL;
      if (!root_node) {
          temp_node = PyDict_GetItem(root_dict, listitem);
          if (!temp_node)
            break;
          root_node = temp_node;
          myfun = PyObject_CallMethodObjArgs(temp_node, PyString_FromString("get_resource"), NULL );
      }
      else {
          if (temp_node) {
            children_dict = PyObject_CallMethodObjArgs(temp_node, PyString_FromString("get_children"), NULL );
            if (children_dict) {
              temp_node2 = PyDict_GetItem(children_dict, listitem);
              if (!temp_node2) {
                temp_node2 = PyObject_CallMethodObjArgs(temp_node, PyString_FromString("get_varchild"), NULL );
                if (temp_node2) {
                  PyDict_SetItem(var_dict, PyObject_CallMethodObjArgs(temp_node2, PyString_FromString("get_name"), NULL ), listitem);
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

//PyObject* PyDict_GetItem(PyObject *p, PyObject *key)
    //free(localqs);
    if (!myfun) {
      PyErr_SetString(PyExc_RuntimeError, "No resource found");
    }
    return myfun;
}

static PyMethodDef QSMethods[] =
{
     {"find_route", find_route, METH_VARARGS, "Find a route"},
     {"find_route2", find_route2, METH_VARARGS, "Find a route"},
     {NULL, NULL, 0, NULL}
};

PyMODINIT_FUNC
initroute_find(void)
{
     (void) Py_InitModule("route_find", QSMethods);
}
