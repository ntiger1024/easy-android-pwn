LOCAL_PATH := $(call my-dir)

include $(CLEAR_VARS)
LOCAL_MODULE := 01-local-overflow
LOCAL_SRC_FILES := src/01-local-overflow.c
include $(BUILD_EXECUTABLE)

include $(CLEAR_VARS)
LOCAL_MODULE := 02-overwrite-ret
LOCAL_SRC_FILES := src/02-overwrite-ret.c
include $(BUILD_EXECUTABLE)

include $(CLEAR_VARS)
LOCAL_MODULE := 03-one-gadget
LOCAL_SRC_FILES := src/03-one-gadget.c
include $(BUILD_EXECUTABLE)

include $(CLEAR_VARS)
LOCAL_MODULE := 04-shellcode-static
LOCAL_SRC_FILES := src/04-shellcode-static.c
LOCAL_CFLAGS := -z execstack -Wl,-z,execstack
include $(BUILD_EXECUTABLE)

include $(CLEAR_VARS)
LOCAL_MODULE := 06-system-rop
LOCAL_SRC_FILES := src/06-system-rop.c
include $(BUILD_EXECUTABLE)
