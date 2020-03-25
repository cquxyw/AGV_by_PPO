; Auto-generated. Do not edit!


(cl:in-package scout-msg)


;//! \htmlinclude RL_input_msgs.msg.html

(cl:defclass <RL_input_msgs> (roslisp-msg-protocol:ros-message)
  ((header
    :reader header
    :initarg :header
    :type std_msgs-msg:Header
    :initform (cl:make-instance 'std_msgs-msg:Header))
   (me_x
    :reader me_x
    :initarg :me_x
    :type cl:float
    :initform 0.0)
   (me_y
    :reader me_y
    :initarg :me_y
    :type cl:float
    :initform 0.0)
   (me_yaw
    :reader me_yaw
    :initarg :me_yaw
    :type cl:float
    :initform 0.0)
   (me_v
    :reader me_v
    :initarg :me_v
    :type cl:float
    :initform 0.0)
   (me_w
    :reader me_w
    :initarg :me_w
    :type cl:float
    :initform 0.0))
)

(cl:defclass RL_input_msgs (<RL_input_msgs>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <RL_input_msgs>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'RL_input_msgs)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name scout-msg:<RL_input_msgs> is deprecated: use scout-msg:RL_input_msgs instead.")))

(cl:ensure-generic-function 'header-val :lambda-list '(m))
(cl:defmethod header-val ((m <RL_input_msgs>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader scout-msg:header-val is deprecated.  Use scout-msg:header instead.")
  (header m))

(cl:ensure-generic-function 'me_x-val :lambda-list '(m))
(cl:defmethod me_x-val ((m <RL_input_msgs>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader scout-msg:me_x-val is deprecated.  Use scout-msg:me_x instead.")
  (me_x m))

(cl:ensure-generic-function 'me_y-val :lambda-list '(m))
(cl:defmethod me_y-val ((m <RL_input_msgs>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader scout-msg:me_y-val is deprecated.  Use scout-msg:me_y instead.")
  (me_y m))

(cl:ensure-generic-function 'me_yaw-val :lambda-list '(m))
(cl:defmethod me_yaw-val ((m <RL_input_msgs>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader scout-msg:me_yaw-val is deprecated.  Use scout-msg:me_yaw instead.")
  (me_yaw m))

(cl:ensure-generic-function 'me_v-val :lambda-list '(m))
(cl:defmethod me_v-val ((m <RL_input_msgs>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader scout-msg:me_v-val is deprecated.  Use scout-msg:me_v instead.")
  (me_v m))

(cl:ensure-generic-function 'me_w-val :lambda-list '(m))
(cl:defmethod me_w-val ((m <RL_input_msgs>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader scout-msg:me_w-val is deprecated.  Use scout-msg:me_w instead.")
  (me_w m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <RL_input_msgs>) ostream)
  "Serializes a message object of type '<RL_input_msgs>"
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'header) ostream)
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'me_x))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'me_y))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'me_yaw))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'me_v))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'me_w))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <RL_input_msgs>) istream)
  "Deserializes a message object of type '<RL_input_msgs>"
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'header) istream)
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'me_x) (roslisp-utils:decode-double-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'me_y) (roslisp-utils:decode-double-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'me_yaw) (roslisp-utils:decode-double-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'me_v) (roslisp-utils:decode-double-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'me_w) (roslisp-utils:decode-double-float-bits bits)))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<RL_input_msgs>)))
  "Returns string type for a message object of type '<RL_input_msgs>"
  "scout/RL_input_msgs")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'RL_input_msgs)))
  "Returns string type for a message object of type 'RL_input_msgs"
  "scout/RL_input_msgs")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<RL_input_msgs>)))
  "Returns md5sum for a message object of type '<RL_input_msgs>"
  "5f2ea7f125f21cbef73d64dd7a90ab98")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'RL_input_msgs)))
  "Returns md5sum for a message object of type 'RL_input_msgs"
  "5f2ea7f125f21cbef73d64dd7a90ab98")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<RL_input_msgs>)))
  "Returns full string definition for message of type '<RL_input_msgs>"
  (cl:format cl:nil "Header header~%float64 me_x~%float64 me_y~%float64 me_yaw~%float64 me_v~%float64 me_w~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%# 0: no frame~%# 1: global frame~%string frame_id~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'RL_input_msgs)))
  "Returns full string definition for message of type 'RL_input_msgs"
  (cl:format cl:nil "Header header~%float64 me_x~%float64 me_y~%float64 me_yaw~%float64 me_v~%float64 me_w~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%# 0: no frame~%# 1: global frame~%string frame_id~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <RL_input_msgs>))
  (cl:+ 0
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'header))
     8
     8
     8
     8
     8
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <RL_input_msgs>))
  "Converts a ROS message object to a list"
  (cl:list 'RL_input_msgs
    (cl:cons ':header (header msg))
    (cl:cons ':me_x (me_x msg))
    (cl:cons ':me_y (me_y msg))
    (cl:cons ':me_yaw (me_yaw msg))
    (cl:cons ':me_v (me_v msg))
    (cl:cons ':me_w (me_w msg))
))
