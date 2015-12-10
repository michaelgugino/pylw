#include <Python.h>
#include <string.h>
#include <stddef.h>
static PyObject*
say_hello(PyObject* self, PyObject* args)
{
    const char* name;

    if (!PyArg_ParseTuple(args, "s", &name))
        return NULL;

    printf("Hello %s!\n", name);

    Py_RETURN_NONE;
}

static PyObject*
parse_qs(PyObject* self, PyObject* args)
{
  char *qs;
  char *localqs;
  char *token;
  char *tokena;



  if (!PyArg_ParseTuple(args, "s", &qs))
      return NULL;
  localqs = strdup(qs);
  PyDictObject *d = PyDict_New();

  /*
    for (int i = 0; i < 2; i++) {
      PyDict_SetItem(d, PyString_FromString(a[i]), PyString_FromString(a[i]));
    }
    */

    while ((token = strsep(&localqs, "&")) != NULL) {
      //for (ta = token; (*ta = strsep(&token, "=")) != NULL;)
          //tokenb = strsep(&token, "=");
          //tokena = token;
          //running = strdupa (string);
          tokena = strsep(&token, "=");
          //tokenb = strsep(&token, "=");
          if (token == NULL)
            PyDict_SetItem(d, PyString_FromString(tokena), PyString_FromString(""));
          else {
            PyDict_SetItem(d, PyString_FromString(tokena), PyString_FromString(token));
          }

    }

    free(localqs);
    //PyDict_SetItem(d, PyString_FromString("var1"), PyString_FromString("val1"));
    return d;
}

static PyMethodDef QSMethods[] =
{
     {"say_hello", say_hello, METH_VARARGS, "Greet somebody."},
     {"parse_qs", parse_qs, METH_VARARGS, "Parse a string"},
     {NULL, NULL, 0, NULL}
};

PyMODINIT_FUNC
initqs_parse(void)
{
     (void) Py_InitModule("qs_parse", QSMethods);
}
