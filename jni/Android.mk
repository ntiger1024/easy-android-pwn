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
LOCAL_MODULE := 04-shellcode-static
LOCAL_SRC_FILES := src/04-shellcode-static.c
include $(BUILD_EXECUTABLE)

include $(CLEAR_VARS)
LOCAL_MODULE := 05-shellcode-dynamic
LOCAL_SRC_FILES := src/05-shellcode-dynamic.c
include $(BUILD_EXECUTABLE)

include $(CLEAR_VARS)
LOCAL_MODULE := 06-system-rop
LOCAL_SRC_FILES := src/06-system-rop.c
include $(BUILD_EXECUTABLE)

include $(CLEAR_VARS)
LOCAL_MODULE := 07-execve-rop
LOCAL_SRC_FILES := src/07-execve-rop.c
include $(BUILD_EXECUTABLE)

include $(CLEAR_VARS)
LOCAL_MODULE := 08-overwrite-global
LOCAL_SRC_FILES := src/08-overwrite-global.c
include $(BUILD_EXECUTABLE)
