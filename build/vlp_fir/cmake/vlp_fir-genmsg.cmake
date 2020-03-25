# generated from genmsg/cmake/pkg-genmsg.cmake.em

message(STATUS "vlp_fir: 1 messages, 0 services")

set(MSG_I_FLAGS "-Ivlp_fir:/home/xyw/BUAA/Graduation/src/vlp_fir/msg;-Istd_msgs:/opt/ros/kinetic/share/std_msgs/cmake/../msg")

# Find all generators
find_package(gencpp REQUIRED)
find_package(geneus REQUIRED)
find_package(genlisp REQUIRED)
find_package(gennodejs REQUIRED)
find_package(genpy REQUIRED)

add_custom_target(vlp_fir_generate_messages ALL)

# verify that message/service dependencies have not changed since configure



get_filename_component(_filename "/home/xyw/BUAA/Graduation/src/vlp_fir/msg/send_msgs.msg" NAME_WE)
add_custom_target(_vlp_fir_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "vlp_fir" "/home/xyw/BUAA/Graduation/src/vlp_fir/msg/send_msgs.msg" ""
)

#
#  langs = gencpp;geneus;genlisp;gennodejs;genpy
#

### Section generating for lang: gencpp
### Generating Messages
_generate_msg_cpp(vlp_fir
  "/home/xyw/BUAA/Graduation/src/vlp_fir/msg/send_msgs.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/vlp_fir
)

### Generating Services

### Generating Module File
_generate_module_cpp(vlp_fir
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/vlp_fir
  "${ALL_GEN_OUTPUT_FILES_cpp}"
)

add_custom_target(vlp_fir_generate_messages_cpp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_cpp}
)
add_dependencies(vlp_fir_generate_messages vlp_fir_generate_messages_cpp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/xyw/BUAA/Graduation/src/vlp_fir/msg/send_msgs.msg" NAME_WE)
add_dependencies(vlp_fir_generate_messages_cpp _vlp_fir_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(vlp_fir_gencpp)
add_dependencies(vlp_fir_gencpp vlp_fir_generate_messages_cpp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS vlp_fir_generate_messages_cpp)

### Section generating for lang: geneus
### Generating Messages
_generate_msg_eus(vlp_fir
  "/home/xyw/BUAA/Graduation/src/vlp_fir/msg/send_msgs.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/vlp_fir
)

### Generating Services

### Generating Module File
_generate_module_eus(vlp_fir
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/vlp_fir
  "${ALL_GEN_OUTPUT_FILES_eus}"
)

add_custom_target(vlp_fir_generate_messages_eus
  DEPENDS ${ALL_GEN_OUTPUT_FILES_eus}
)
add_dependencies(vlp_fir_generate_messages vlp_fir_generate_messages_eus)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/xyw/BUAA/Graduation/src/vlp_fir/msg/send_msgs.msg" NAME_WE)
add_dependencies(vlp_fir_generate_messages_eus _vlp_fir_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(vlp_fir_geneus)
add_dependencies(vlp_fir_geneus vlp_fir_generate_messages_eus)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS vlp_fir_generate_messages_eus)

### Section generating for lang: genlisp
### Generating Messages
_generate_msg_lisp(vlp_fir
  "/home/xyw/BUAA/Graduation/src/vlp_fir/msg/send_msgs.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/vlp_fir
)

### Generating Services

### Generating Module File
_generate_module_lisp(vlp_fir
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/vlp_fir
  "${ALL_GEN_OUTPUT_FILES_lisp}"
)

add_custom_target(vlp_fir_generate_messages_lisp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_lisp}
)
add_dependencies(vlp_fir_generate_messages vlp_fir_generate_messages_lisp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/xyw/BUAA/Graduation/src/vlp_fir/msg/send_msgs.msg" NAME_WE)
add_dependencies(vlp_fir_generate_messages_lisp _vlp_fir_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(vlp_fir_genlisp)
add_dependencies(vlp_fir_genlisp vlp_fir_generate_messages_lisp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS vlp_fir_generate_messages_lisp)

### Section generating for lang: gennodejs
### Generating Messages
_generate_msg_nodejs(vlp_fir
  "/home/xyw/BUAA/Graduation/src/vlp_fir/msg/send_msgs.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/vlp_fir
)

### Generating Services

### Generating Module File
_generate_module_nodejs(vlp_fir
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/vlp_fir
  "${ALL_GEN_OUTPUT_FILES_nodejs}"
)

add_custom_target(vlp_fir_generate_messages_nodejs
  DEPENDS ${ALL_GEN_OUTPUT_FILES_nodejs}
)
add_dependencies(vlp_fir_generate_messages vlp_fir_generate_messages_nodejs)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/xyw/BUAA/Graduation/src/vlp_fir/msg/send_msgs.msg" NAME_WE)
add_dependencies(vlp_fir_generate_messages_nodejs _vlp_fir_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(vlp_fir_gennodejs)
add_dependencies(vlp_fir_gennodejs vlp_fir_generate_messages_nodejs)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS vlp_fir_generate_messages_nodejs)

### Section generating for lang: genpy
### Generating Messages
_generate_msg_py(vlp_fir
  "/home/xyw/BUAA/Graduation/src/vlp_fir/msg/send_msgs.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/vlp_fir
)

### Generating Services

### Generating Module File
_generate_module_py(vlp_fir
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/vlp_fir
  "${ALL_GEN_OUTPUT_FILES_py}"
)

add_custom_target(vlp_fir_generate_messages_py
  DEPENDS ${ALL_GEN_OUTPUT_FILES_py}
)
add_dependencies(vlp_fir_generate_messages vlp_fir_generate_messages_py)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/xyw/BUAA/Graduation/src/vlp_fir/msg/send_msgs.msg" NAME_WE)
add_dependencies(vlp_fir_generate_messages_py _vlp_fir_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(vlp_fir_genpy)
add_dependencies(vlp_fir_genpy vlp_fir_generate_messages_py)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS vlp_fir_generate_messages_py)



if(gencpp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/vlp_fir)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/vlp_fir
    DESTINATION ${gencpp_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_cpp)
  add_dependencies(vlp_fir_generate_messages_cpp std_msgs_generate_messages_cpp)
endif()

if(geneus_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/vlp_fir)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/vlp_fir
    DESTINATION ${geneus_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_eus)
  add_dependencies(vlp_fir_generate_messages_eus std_msgs_generate_messages_eus)
endif()

if(genlisp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/vlp_fir)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/vlp_fir
    DESTINATION ${genlisp_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_lisp)
  add_dependencies(vlp_fir_generate_messages_lisp std_msgs_generate_messages_lisp)
endif()

if(gennodejs_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/vlp_fir)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/vlp_fir
    DESTINATION ${gennodejs_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_nodejs)
  add_dependencies(vlp_fir_generate_messages_nodejs std_msgs_generate_messages_nodejs)
endif()

if(genpy_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/vlp_fir)
  install(CODE "execute_process(COMMAND \"/home/xyw/.pyenv/shims/python2\" -m compileall \"${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/vlp_fir\")")
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/vlp_fir
    DESTINATION ${genpy_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_py)
  add_dependencies(vlp_fir_generate_messages_py std_msgs_generate_messages_py)
endif()
