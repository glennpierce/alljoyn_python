#include "Python.h"

#include <stdint.h>
#include <stdio.h>

#include <alljoyn/Init.h>

static PyObject * python_alljoyn_routerinit(PyObject * self, PyObject * args)
{
  int status = AllJoynRouterInit();
  return Py_BuildValue("i", status);
}

static PyObject * python_alljoyn_routershutdown(PyObject * self, PyObject * args)
{ 
  int status = AllJoynRouterShutdown();
  return Py_BuildValue("i", status);
}

static PyMethodDef AlljoynRouterMethods[] = {
 { "RouterInit", python_alljoyn_routerinit, METH_VARARGS, "Initialise Router" },
 { "RouterShutdown", python_alljoyn_routershutdown, METH_VARARGS, "Shutdown Router" },
 { NULL, NULL, 0, NULL }
};


DL_EXPORT(void) initAlljoynRouter(void)
{
  Py_InitModule("AlljoynRouter", AlljoynRouterMethods);
}

