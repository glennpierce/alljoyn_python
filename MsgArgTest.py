#!/usr/bin/env python

import unittest

from AllJoynPy import AllJoyn, AboutListener, MsgArg, AboutData, \
    QStatusException, AboutObjectDescription, Session, \
    TransportMask, SessionListener, AboutProxy, ProxyBusObject, \
    Message, BusListener, BusAttachment, MsgArgHandle

from numpy.ctypeslib import ndpointer
import ctypes as C


class TestMsgArgMethods(unittest.TestCase):

    def setUp(self):
        self.alljoyn = AllJoyn()

    def test_basic(self):
        arg = MsgArg.MsgArg()
        intSet = C.c_int32(-9999)
        intResult = C.c_int32()

        try:
            arg.Set("i", [C.c_int32], [intSet])
            arg.Get("i", [C.POINTER(C.c_int32)], [intResult])
        except QStatusException:
            assert False

        self.assertEqual(intResult.value, -9999, 'wrong result')


# alljoyn_msgarg arg = alljoyn_msgarg_create();
#         status = alljoyn_msgarg_set(arg, "ay", sizeof(ay) / sizeof(ay[0]), ay);
#         EXPECT_EQ(ER_OK, status) << "  Actual Status: " << QCC_StatusText(status);
#         uint8_t* pay;
#         size_t lay;
#         status = alljoyn_msgarg_get(arg, "ay", &lay, &pay);
#         EXPECT_EQ(ER_OK, status) << "  Actual Status: " << QCC_StatusText(status);
#         EXPECT_EQ(sizeof(ay) / sizeof(ay[0]), lay);
#         for (size_t i = 0; i < lay; ++i) {
#             EXPECT_EQ(ay[i], pay[i]);
#         }
#         alljoyn_msgarg_destroy(arg);



    def test_array(self):
        # Test (sai)
        arg = MsgArg.MsgArg()
        stringSet = C.c_char_p("Hello")
        stringResult = C.c_char_p()

        l = [-8, -88, 888, 8888]
        num = C.c_size_t(len(l))
        ArrayType = C.c_int32 * len(l)
        array = ArrayType()
        array[:] = l

        resultArray = C.POINTER(C.c_int32)()  # defines the type AND create an instance of it
        returnNum = C.c_size_t()

        try:
            arg.Set("(sai)", [C.c_char_p, C.c_size_t, ArrayType], [stringSet, num, array])
        except QStatusException as ex:
            print str(ex)
            assert False

        try:
            arg.Get("(sai)", [C.POINTER(C.c_char_p), C.POINTER(C.c_size_t), C.POINTER(C.POINTER(C.c_int32))],
                    [C.byref(stringResult), C.byref(returnNum), C.byref(resultArray)])

            self.assertEqual(stringResult.value, "Hello", 'wrong result')
            self.assertEqual(returnNum.value, 4, 'wrong result')
            l2 = [resultArray[i] for i in range(4)]
            self.assertItemsEqual(l, l2, 'wrong result')

        except QStatusException as ex:
            print str(ex)
            assert False

    def test_array2(self):
        # Test (sai)
        arg = MsgArg.MsgArg()
        stringSet = C.c_char_p("Hello")
        stringResult = C.c_char_p()

        l = [-8, -88, 888, 8888]
        num = C.c_size_t(len(l))
        ArrayType = C.c_int32 * len(l)
        array = ArrayType()
        array[:] = l

        y = [2, 4, 8, 16]
        ynum = C.c_size_t(len(y))
        YArrayType = C.c_byte * len(y)
        byte_array = YArrayType()
        byte_array[:] = y

        resultArray = C.POINTER(C.c_int32)()  # defines the type AND create an instance of it
        returnNum = C.c_size_t()

        byteResultArray = C.POINTER(C.c_byte)()  # defines the type AND create an instance of it
        byteReturnNum = C.c_size_t()

        try:
            arg.Set("(saiay)", [C.c_char_p, C.c_size_t, ArrayType, C.c_size_t, YArrayType],
                               [stringSet, num, array, ynum, byte_array])
        except QStatusException as ex:
            print str(ex)
            assert False

        try:
            arg.Get("(saiay)", [C.POINTER(C.c_char_p), C.POINTER(C.c_size_t), C.POINTER(C.POINTER(C.c_int32)), C.POINTER(C.c_size_t), C.POINTER(C.POINTER(C.c_byte))],
                    [C.byref(stringResult), C.byref(returnNum), C.byref(resultArray), C.byref(byteReturnNum), C.byref(byteResultArray)])

            self.assertEqual(stringResult.value, "Hello", 'wrong result')
            self.assertEqual(returnNum.value, 4, 'wrong result')
            l2 = [resultArray[i] for i in range(4)]
            self.assertItemsEqual(l, l2, 'wrong result')
            self.assertEqual(byteReturnNum.value, 4, 'wrong result')
            y2 = [byteResultArray[i] for i in range(4)]
            self.assertItemsEqual(y, y2, 'wrong result')

        except QStatusException as ex:
            print str(ex)
            assert False

if __name__ == '__main__':
    unittest.main()
