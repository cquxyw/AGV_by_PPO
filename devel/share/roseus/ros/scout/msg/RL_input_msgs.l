;; Auto-generated. Do not edit!


(when (boundp 'scout::RL_input_msgs)
  (if (not (find-package "SCOUT"))
    (make-package "SCOUT"))
  (shadow 'RL_input_msgs (find-package "SCOUT")))
(unless (find-package "SCOUT::RL_INPUT_MSGS")
  (make-package "SCOUT::RL_INPUT_MSGS"))

(in-package "ROS")
;;//! \htmlinclude RL_input_msgs.msg.html
(if (not (find-package "STD_MSGS"))
  (ros::roseus-add-msgs "std_msgs"))


(defclass scout::RL_input_msgs
  :super ros::object
  :slots (_header _me_x _me_y _me_yaw _me_v _me_w ))

(defmethod scout::RL_input_msgs
  (:init
   (&key
    ((:header __header) (instance std_msgs::Header :init))
    ((:me_x __me_x) 0.0)
    ((:me_y __me_y) 0.0)
    ((:me_yaw __me_yaw) 0.0)
    ((:me_v __me_v) 0.0)
    ((:me_w __me_w) 0.0)
    )
   (send-super :init)
   (setq _header __header)
   (setq _me_x (float __me_x))
   (setq _me_y (float __me_y))
   (setq _me_yaw (float __me_yaw))
   (setq _me_v (float __me_v))
   (setq _me_w (float __me_w))
   self)
  (:header
   (&rest __header)
   (if (keywordp (car __header))
       (send* _header __header)
     (progn
       (if __header (setq _header (car __header)))
       _header)))
  (:me_x
   (&optional __me_x)
   (if __me_x (setq _me_x __me_x)) _me_x)
  (:me_y
   (&optional __me_y)
   (if __me_y (setq _me_y __me_y)) _me_y)
  (:me_yaw
   (&optional __me_yaw)
   (if __me_yaw (setq _me_yaw __me_yaw)) _me_yaw)
  (:me_v
   (&optional __me_v)
   (if __me_v (setq _me_v __me_v)) _me_v)
  (:me_w
   (&optional __me_w)
   (if __me_w (setq _me_w __me_w)) _me_w)
  (:serialization-length
   ()
   (+
    ;; std_msgs/Header _header
    (send _header :serialization-length)
    ;; float64 _me_x
    8
    ;; float64 _me_y
    8
    ;; float64 _me_yaw
    8
    ;; float64 _me_v
    8
    ;; float64 _me_w
    8
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; std_msgs/Header _header
       (send _header :serialize s)
     ;; float64 _me_x
       (sys::poke _me_x (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _me_y
       (sys::poke _me_y (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _me_yaw
       (sys::poke _me_yaw (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _me_v
       (sys::poke _me_v (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _me_w
       (sys::poke _me_w (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; std_msgs/Header _header
     (send _header :deserialize buf ptr-) (incf ptr- (send _header :serialization-length))
   ;; float64 _me_x
     (setq _me_x (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _me_y
     (setq _me_y (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _me_yaw
     (setq _me_yaw (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _me_v
     (setq _me_v (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _me_w
     (setq _me_w (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;;
   self)
  )

(setf (get scout::RL_input_msgs :md5sum-) "5f2ea7f125f21cbef73d64dd7a90ab98")
(setf (get scout::RL_input_msgs :datatype-) "scout/RL_input_msgs")
(setf (get scout::RL_input_msgs :definition-)
      "Header header
float64 me_x
float64 me_y
float64 me_yaw
float64 me_v
float64 me_w
================================================================================
MSG: std_msgs/Header
# Standard metadata for higher-level stamped data types.
# This is generally used to communicate timestamped data 
# in a particular coordinate frame.
# 
# sequence ID: consecutively increasing ID 
uint32 seq
#Two-integer timestamp that is expressed as:
# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')
# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')
# time-handling sugar is provided by the client library
time stamp
#Frame this data is associated with
# 0: no frame
# 1: global frame
string frame_id

")



(provide :scout/RL_input_msgs "5f2ea7f125f21cbef73d64dd7a90ab98")


