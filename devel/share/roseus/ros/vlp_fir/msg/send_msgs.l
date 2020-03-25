;; Auto-generated. Do not edit!


(when (boundp 'vlp_fir::send_msgs)
  (if (not (find-package "VLP_FIR"))
    (make-package "VLP_FIR"))
  (shadow 'send_msgs (find-package "VLP_FIR")))
(unless (find-package "VLP_FIR::SEND_MSGS")
  (make-package "VLP_FIR::SEND_MSGS"))

(in-package "ROS")
;;//! \htmlinclude send_msgs.msg.html


(defclass vlp_fir::send_msgs
  :super ros::object
  :slots (_date _num _x _y _z _len _width _height ))

(defmethod vlp_fir::send_msgs
  (:init
   (&key
    ((:date __date) nil)
    ((:num __num) 0)
    ((:x __x) 0.0)
    ((:y __y) 0.0)
    ((:z __z) 0.0)
    ((:len __len) 0.0)
    ((:width __width) 0.0)
    ((:height __height) 0.0)
    )
   (send-super :init)
   (setq _date __date)
   (setq _num (round __num))
   (setq _x (float __x))
   (setq _y (float __y))
   (setq _z (float __z))
   (setq _len (float __len))
   (setq _width (float __width))
   (setq _height (float __height))
   self)
  (:date
   (&optional __date)
   (if __date (setq _date __date)) _date)
  (:num
   (&optional __num)
   (if __num (setq _num __num)) _num)
  (:x
   (&optional __x)
   (if __x (setq _x __x)) _x)
  (:y
   (&optional __y)
   (if __y (setq _y __y)) _y)
  (:z
   (&optional __z)
   (if __z (setq _z __z)) _z)
  (:len
   (&optional __len)
   (if __len (setq _len __len)) _len)
  (:width
   (&optional __width)
   (if __width (setq _width __width)) _width)
  (:height
   (&optional __height)
   (if __height (setq _height __height)) _height)
  (:serialization-length
   ()
   (+
    ;; bool _date
    1
    ;; int32 _num
    4
    ;; float64 _x
    8
    ;; float64 _y
    8
    ;; float64 _z
    8
    ;; float64 _len
    8
    ;; float64 _width
    8
    ;; float64 _height
    8
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; bool _date
       (if _date (write-byte -1 s) (write-byte 0 s))
     ;; int32 _num
       (write-long _num s)
     ;; float64 _x
       (sys::poke _x (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _y
       (sys::poke _y (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _z
       (sys::poke _z (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _len
       (sys::poke _len (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _width
       (sys::poke _width (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _height
       (sys::poke _height (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; bool _date
     (setq _date (not (= 0 (sys::peek buf ptr- :char)))) (incf ptr- 1)
   ;; int32 _num
     (setq _num (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;; float64 _x
     (setq _x (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _y
     (setq _y (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _z
     (setq _z (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _len
     (setq _len (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _width
     (setq _width (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _height
     (setq _height (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;;
   self)
  )

(setf (get vlp_fir::send_msgs :md5sum-) "bf460c9b2194df7c3ccef2b14e93b960")
(setf (get vlp_fir::send_msgs :datatype-) "vlp_fir/send_msgs")
(setf (get vlp_fir::send_msgs :definition-)
      "bool date
int32 num
float64 x
float64 y
float64 z
float64 len
float64 width
float64 height

")



(provide :vlp_fir/send_msgs "bf460c9b2194df7c3ccef2b14e93b960")


