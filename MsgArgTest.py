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
        except QStatusException as ex:
            print str(ex)
            assert False

        self.assertEqual(intResult.value, -9999, 'wrong result')

    def test_basic2(self):
        """
        When dealing with non complete types we need to use the array functions
        """
        arg = MsgArg.MsgArg()
        param1Set = C.c_int32(10)
        param2Set = C.c_char_p("Hello")
        param3Set = C.c_char_p("World")
        param4Set = C.c_int32(20)

        try:
            arg.Set("issi", [C.c_int32, C.c_char_p, C.c_char_p, C.c_int32],
                            [param1Set, param2Set, param3Set, param4Set])
            #arg.Get("i", [C.POINTER(C.c_int32)], [intResult])
        except QStatusException as ex:
            print str(ex)
            assert False

        self.assertEqual(intResult.value, -9999, 'wrong result')


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

  





# TEST(MsgArgTest, alljoyn_msgarg_array_set_get) {
#     QStatus status = ER_OK;
#     alljoyn_msgarg arg;
#     arg = alljoyn_msgarg_array_create(4);
#     size_t numArgs = 4;
#     status = alljoyn_msgarg_array_set(arg, &numArgs, "issi", 1, "two", "three", 4);
#     EXPECT_EQ(ER_OK, status) << "  Actual Status: " << QCC_StatusText(status);

#     int32_t argvalue1;
#     char* argvalue2;
#     char* argvalue3;
#     int32_t argvalue4;
#     status = alljoyn_msgarg_get(alljoyn_msgarg_array_element(arg, 0), "i", &argvalue1);
#     EXPECT_EQ(ER_OK, status) << "  Actual Status: " << QCC_StatusText(status);
#     EXPECT_EQ(1, argvalue1);
#     status = alljoyn_msgarg_get(alljoyn_msgarg_array_element(arg, 1), "s", &argvalue2);
#     EXPECT_EQ(ER_OK, status) << "  Actual Status: " << QCC_StatusText(status);
#     EXPECT_STREQ("two", argvalue2);
#     status = alljoyn_msgarg_get(alljoyn_msgarg_array_element(arg, 2), "s", &argvalue3);
#     EXPECT_EQ(ER_OK, status) << "  Actual Status: " << QCC_StatusText(status);
#     EXPECT_STREQ("three", argvalue3);
#     status = alljoyn_msgarg_get(alljoyn_msgarg_array_element(arg, 3), "i", &argvalue4);
#     EXPECT_EQ(ER_OK, status) << "  Actual Status: " << QCC_StatusText(status);
#     EXPECT_EQ(4, argvalue4);

#     int32_t out1;
#     char* out2;
#     char* out3;
#     int32_t out4;
#     status = alljoyn_msgarg_array_get(arg, 4, "issi", &out1, &out2, &out3, &out4);
#     EXPECT_EQ(ER_OK, status) << "  Actual Status: " << QCC_StatusText(status);
#     EXPECT_EQ(1, out1);
#     EXPECT_STREQ("two", out2);
#     EXPECT_STREQ("three", out3);
#     EXPECT_EQ(4, out4);

#     alljoyn_msgarg_destroy(arg);
# }









if __name__ == '__main__':
    unittest.main()













#     QStatus status = ER_OK;
#     const char*keys[] = { "red", "green", "blue", "yellow" };
#     //size_t numEntries = sizeof(keys) / sizeof(keys[0]);
#     alljoyn_msgarg dictEntries = NULL;
#     alljoyn_msgarg values = NULL;
#     dictEntries = alljoyn_msgarg_array_create(sizeof(keys) / sizeof(keys[0]));
#     values = alljoyn_msgarg_array_create(sizeof(keys) / sizeof(keys[0]));
#     alljoyn_msgarg_set(alljoyn_msgarg_array_element(values, 0), "s", keys[0]);
#     alljoyn_msgarg_set(alljoyn_msgarg_array_element(values, 1), "(ss)", keys[1], "bean");
#     alljoyn_msgarg_set(alljoyn_msgarg_array_element(values, 2), "s", keys[2]);
#     alljoyn_msgarg_set(alljoyn_msgarg_array_element(values, 3), "(ss)", keys[3], "mellow");

#     status = alljoyn_msgarg_set(alljoyn_msgarg_array_element(dictEntries, 0), "{iv}", 1, alljoyn_msgarg_array_element(values, 0));
#     EXPECT_EQ(ER_OK, status) << "  Actual Status: " << QCC_StatusText(status);
#     status = alljoyn_msgarg_set(alljoyn_msgarg_array_element(dictEntries, 1), "{iv}", 1, alljoyn_msgarg_array_element(values, 1));
#     EXPECT_EQ(ER_OK, status) << "  Actual Status: " << QCC_StatusText(status);
#     status = alljoyn_msgarg_set(alljoyn_msgarg_array_element(dictEntries, 2), "{iv}", 1, alljoyn_msgarg_array_element(values, 2));
#     EXPECT_EQ(ER_OK, status) << "  Actual Status: " << QCC_StatusText(status);
#     status = alljoyn_msgarg_set(alljoyn_msgarg_array_element(dictEntries, 3), "{iv}", 1, alljoyn_msgarg_array_element(values, 3));
#     EXPECT_EQ(ER_OK, status) << "  Actual Status: " << QCC_StatusText(status);

#     alljoyn_msgarg dict = alljoyn_msgarg_create();
#     status = alljoyn_msgarg_set(dict, "a{iv}", sizeof(keys) / sizeof(keys[0]), dictEntries);
#     EXPECT_EQ(ER_OK, status) << "  Actual Status: " << QCC_StatusText(status);

#     alljoyn_msgarg entries;
#     size_t num;
#     status = alljoyn_msgarg_get(dict, "a{iv}", &num, &entries);
#     EXPECT_EQ(num, sizeof(keys) / sizeof(keys[0]));
#     EXPECT_EQ(ER_OK, status) << "  Actual Status: " << QCC_StatusText(status);
#     for (size_t i = 0; i < num; ++i) {
#         char* str1;
#         char* str2;
#         int32_t key;
#         status = alljoyn_msgarg_get(alljoyn_msgarg_array_element(entries, i), "{is}", &key, &str1);
#         if (status == ER_BUS_SIGNATURE_MISMATCH) {
#             status = alljoyn_msgarg_get(alljoyn_msgarg_array_element(entries, i), "{i(ss)}", &key, &str1, &str2);
#             EXPECT_EQ(1, key);
#             EXPECT_STREQ(keys[i], str1);
#             if (i == 1) {
#                 EXPECT_STREQ("bean", str2);
#             } else if (i == 3) {
#                 EXPECT_STREQ("mellow", str2);
#             }
#         } else if (status == ER_OK) {
#             EXPECT_EQ(1, key);
#             EXPECT_STREQ(keys[i], str1);
#         }
#         EXPECT_EQ(ER_OK, status) << "  Actual Status: " << QCC_StatusText(status);
#     }
#     alljoyn_msgarg_destroy(dictEntries);
#     alljoyn_msgarg_destroy(values);
#     alljoyn_msgarg_destroy(dict);
# }

