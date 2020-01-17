# cython: experimental_cpp_class_def=True, language_level=3
# distutils: language=c++

import cython
from libcpp cimport bool
from libcpp.string cimport string
import numpy as np
cimport numpy as np


cdef extern from "backpropcore/model/model.hpp" namespace "model":
    cdef cppclass CModel:
        void build(string) nogil except +


cdef class CyModel:

    cdef CModel* obj

    def __cinit__(self):
        self.obj = new CModel()

    def __dealloc__(self):
        #self.obj.release()
        del self.obj

    def build(self, ipt):
        self.obj.build(ipt)

